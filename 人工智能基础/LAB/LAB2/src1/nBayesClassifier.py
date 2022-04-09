import numpy as np
import math
from collections import Counter
from process_data import load_and_process_data
from evaluation import get_micro_F1,get_macro_F1,get_acc

def continuous_fun(sigma2,mu,x):#计算连续型属性的条件概率，输入sigma，mu，x返回 p
    s1 = 1/(math.sqrt(2*np.pi*sigma2)) #系数
    s2 = -pow(x-mu,2)/(2*sigma2)  #e指数
    return s1*pow(np.e,s2)


class NaiveBayes:
    '''参数初始化
    Pc: P(c) 每个类别c的概率分布
    Pxc: P(c|x) 每个特征的条件概率
    '''
    def __init__(self):
        self.Pc={}
        self.Pxc={}#离散值键由元组构成：(标签，属性序号/列数，值); 连续值键由元组构成：(标签，属性序号)，值也为元组(sigma2，mu)

    '''
    通过训练集计算先验概率分布p(c)和条件概率分布p(x|c)
    建议全部取log，避免相乘为0
    '''
    def fit(self,traindata,trainlabel,featuretype):
        '''
        需要你实现的部分
        '''
        feature_rows = traindata.shape[0]
        feature_lines = traindata.shape[1]

        #计算先验概率分布Pc
        PcCount = {}
        for i in range(0,feature_rows):
            if PcCount.get(trainlabel[i][0]) == None:
                PcCount[trainlabel[i][0]] = 1
            else:
                PcCount.update({trainlabel[i][0]:PcCount[trainlabel[i][0]]+1})
        #print(PcCount)

        for key in PcCount.keys():
            self.Pc.update({key:(PcCount[key]+1)/(feature_rows+len(PcCount))})
        #print(self.Pc)


        #计算条件概率，连续型数据需要求均值与方差估计分布参数
        for ilines in range(0,len(featuretype)):#遍历每一个属性
            if featuretype[ilines] == 0:#离散型数据处理
                NCount = {}
                for irows in range(0,feature_rows): #遍历每一条记录，生成这个离散型属性的可能取值数与样本数
                    if NCount.get(traindata[irows][ilines]) == None:
                        NCount[traindata[irows][ilines]] = 1
                    else:
                        NCount.update({traindata[irows][ilines]:NCount[traindata[irows][ilines]]+1})
                #print(NCount)

                Dcx = {}  #键由元组构成  (标签，此离散列的取值)
                for irows in range(0,feature_rows):
                    if Dcx.get((trainlabel[irows][0],traindata[irows][ilines])) == None:
                        Dcx[(trainlabel[irows][0],traindata[irows][ilines])] = 1
                    else:
                        Dcx.update({(trainlabel[irows][0],traindata[irows][ilines]):Dcx[(trainlabel[irows][0],traindata[irows][ilines])]+1})
                #print(Dcx)

                for key in Dcx.keys():
                    value = (Dcx[key] + 1)/(PcCount[key[0]]+len(NCount))
                    self.Pxc.update({(key[0],ilines,key[1]):value})

            else:#连续型数据处理，用高斯分布估计条件概率
                #sigma2 = VarLines[ilines]
                #mu = AvgLines[ilines]
                #截取当前列
                currentLineValue = np.empty([feature_rows,2])
                for i in range(0,feature_rows):
                    currentLineValue[i][0] = traindata[i][ilines]
                    currentLineValue[i][1] = trainlabel[i][0]
                #print(currentLineValue)

                #将测试数据这一列按标签分类
                for key in PcCount.keys():
                    curcurrentLineValue_L = np.empty([PcCount[key],1])
                    i = 0
                    for irows in range(0,feature_rows):
                        if trainlabel[irows][0] == key:
                            curcurrentLineValue_L[i][0] = traindata[irows][ilines]
                            i = i + 1
                    #print(curcurrentLineValue_L)
                    mu_cline = np.mean(curcurrentLineValue_L, axis = 0)
                    #print((AvgLines))
                    sigma2_cline = np.var(curcurrentLineValue_L, axis = 0)
                    #print(VarLines)
                    self.Pxc.update({(key,ilines):(sigma2_cline[0],mu_cline[0])})

        #print(self.Pxc)



    '''
    根据先验概率分布p(c)和条件概率分布p(x|c)对新样本进行预测
    返回预测结果,预测结果的数据类型应为np数组，shape=(test_num,1) test_num为测试数据的数目
    feature_type为0-1数组，表示特征的数据类型，0表示离散型，1表示连续型
    '''
    def predict(self,features,featuretype):
        '''
        需要你实现的部分
        '''       
        feature_rows = features.shape[0]
        feature_lines = features.shape[1]

        pred_int = np.empty([feature_rows,1],dtype = int)

        #print(self.Pc)

        for irow in range(0,feature_rows): #对每一行做预测
            max = -float('inf')
            maxc = None
            for key in self.Pc:
                value = self.Pc[key]
                for iline in range(0,feature_lines):
                    if featuretype[iline] == 0: #离散型
                        value = value * self.Pxc[(key,iline,features[irow][iline])]
                    else:
                        sigma2 = self.Pxc[(key,iline)][0]
                        mu = self.Pxc[(key,iline)][1]
                        value = value * continuous_fun(sigma2,mu,features[irow][iline])
                #print(value)
                if value > max:
                    max = value
                    maxc = key
            pred_int[irow][0] = maxc
        return pred_int

def main():
    # 加载训练集和测试集
    train_data,train_label,test_data,test_label=load_and_process_data()
    feature_type=[0,1,1,1,1,1,1,1] #表示特征的数据类型，0表示离散型，1表示连续型

    Nayes=NaiveBayes()
    Nayes.fit(train_data,train_label,feature_type) # 在训练集上计算先验概率和条件概率

    pred=Nayes.predict(test_data,feature_type)  # 得到测试集上的预测结果

    # 计算准确率Acc及多分类的F1-score
    print("Acc: "+str(get_acc(test_label,pred)))
    print("macro-F1: "+str(get_macro_F1(test_label,pred)))
    print("micro-F1: "+str(get_micro_F1(test_label,pred)))

main()
