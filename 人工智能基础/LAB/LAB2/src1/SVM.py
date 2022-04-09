import numpy as np
import cvxopt as cp  #用于求解线性规划
from process_data import load_and_process_data
from evaluation import get_micro_F1,get_macro_F1,get_acc


#根据指定类别main_class生成1/-1标签
def svm_label(labels,main_class):
    new_label=[]
    for i in range(len(labels)):
        if labels[i]==main_class:
            new_label.append(1)
        else:
            new_label.append(-1)
    return np.array(new_label)

# 实现线性回归
class SupportVectorMachine:

    '''参数初始化 
    lr: 梯度更新的学习率
    Lambda: L2范数的系数
    epochs: 更新迭代的次数
    '''
    def __init__(self,kernel,C,Epsilon):
        self.kernel=kernel
        self.C = C
        self.Epsilon=Epsilon

    '''KERNEL用于计算两个样本x1,x2的核函数'''
    def KERNEL(self, x1, x2, kernel='Linear', d=2, sigma=1):
        #d是多项式核的次数,sigma为Gauss核的参数
        K = 0
        if kernel == 'Gauss':
            K = np.exp(-(np.sum((x1 - x2) ** 2)) / (2 * sigma ** 2))
        elif kernel == 'Linear':
            K = np.dot(x1,x2)
        elif kernel == 'Poly':
            K = np.dot(x1,x2) ** d
        else:
            print('No support for this kernel')
        return K

    '''
    根据训练数据train_data,train_label（均为np数组）求解svm,并对test_data进行预测,返回预测分数，即svm使用符号函数sign之前的值
    train_data的shape=(train_num,train_dim),train_label的shape=(train_num,) train_num为训练数据的数目，train_dim为样本维度
    预测结果的数据类型应为np数组，shape=(test_num,1) test_num为测试数据的数目
    '''
    def fit(self,train_data,train_label,test_data):#train_label已经将所有需要分为当前标签的数据置为1，其他为-1
        '''
        需要你实现的部分
        '''
        #print(train_data[0])
        #k = self.KERNEL(train_data[0],train_data[1])
        #print(k)
        feature_rows = train_data.shape[0]
        feature_lines = train_data.shape[1]
        train_label = train_label.reshape([train_label.shape[0],1])

        Q = cp.matrix(-np.ones([feature_rows, 1],dtype = float, order ='F'))#全为-1
        P = np.empty([feature_rows, feature_rows], dtype = float, order ='F')
        #遍历P矩阵对每个元素赋值
        for irowsP in range(0,feature_rows):
            for ilinesP in range(0,feature_rows):
                P[irowsP][ilinesP] = train_label[irowsP][0] * train_label[ilinesP][0] * self.KERNEL(train_data[irowsP],train_data[ilinesP])
        P = cp.matrix(P)

        A = np.empty([1,feature_rows],dtype = float, order ='C')
        for irows in range(0,feature_rows):
            A[0][irows] = train_label[irows]
        A = cp.matrix(A)
        B = cp.matrix(np.zeros([1,1],dtype = float, order ='C'))
        G = np.zeros([2*feature_rows, feature_rows],dtype = float, order ='C')
        for irows in range(0, 2*feature_rows):
            for ilines in range(0,feature_rows):
                if irows < feature_rows:
                    if irows == ilines:
                        G[irows][ilines] = -1
                else:
                    if irows - feature_rows == ilines:
                        G[irows][ilines] = 1
        G = cp.matrix(G)
        H = np.zeros([2*feature_rows, 1],dtype = float, order ='C')
        for irows in range(feature_rows, 2*feature_rows):
            H[irows][0] = self.C
        H = cp.matrix(H)

        result = cp.solvers.qp(P, Q, G, H, A, B)
        alpha = result['x']
        alpha = np.array(alpha)
        #小于阈值直接置0
        for i in range(0,alpha.shape[0]):
            if alpha[i][0] < self.Epsilon:
                alpha[i][0] = 0
        print('alpha:')
        print(alpha)
        print(type(alpha))
        print(np.array(alpha).shape)

        #求偏移量b
        b = 1.0
        sCount = 0
        for s in range(0,alpha.shape[0]):
            if alpha[s][0] != 0:
                b = b + train_label[s]
                sCount = sCount + 1
                for i in range(0,alpha.shape[0]):
                    if alpha[i][0] != 0:
                        b = b - train_label[i][0] * alpha[i][0] * self.KERNEL(train_data[i],train_data[s])
        b = b / sCount
        print(b)
        print(type(b))
        #求omega
        omega = alpha[0][0] * train_label[0] * train_data[0]
        for irows in range(1,alpha.shape[0]):
            omega = omega + alpha[irows][0] * train_label[irows] * train_data[irows]
        omega = np.array(omega)
        omega = omega.transpose()
        omega = omega.reshape([feature_lines,1])

        print('omega:')
        print(omega)
        print(omega.shape)
        print(type(omega))

        #求预测分数
        #score = np.empty([feature_rows,1])
        score = test_data.dot(omega) + b
        #print(score)
        return score


def main():
    # 加载训练集和测试集
    Train_data,Train_label,Test_data,Test_label=load_and_process_data()
    Train_label=[label[0] for label in Train_label]
    Test_label=[label[0] for label in Test_label]
    train_data=np.array(Train_data)
    test_data=np.array(Test_data)
    test_label=np.array(Test_label).reshape(-1,1)
    #类别个数
    num_class=len(set(Train_label))


    #kernel为核函数类型，可能的类型有'Linear'/'Poly'/'Gauss'
    #C为软间隔参数；
    #Epsilon为拉格朗日乘子阈值，低于此阈值时将该乘子设置为0
    kernel='Linear' 
    C = 1
    Epsilon=10e-5
    #生成SVM分类器
    SVM=SupportVectorMachine(kernel,C,Epsilon)

    predictions = []
    #one-vs-all方法训练num_class个二分类器
    for k in range(1,num_class+1):
        #将第k类样本label置为1，其余类别置为-1
        train_label=svm_label(Train_label,k)
        # 训练模型，并得到测试集上的预测结果
        prediction=SVM.fit(train_data,train_label,test_data)
        predictions.append(prediction)
    predictions=np.array(predictions)

    print(predictions)
    print(type(predictions))

    #one-vs-all, 最终分类结果选择最大score对应的类别
    pred = np.argmax(predictions,axis=0)+1
    pred = np.array(pred)

    print(pred)
    print(type(pred))
    print(pred.shape)

    # 计算准确率Acc及多分类的F1-score
    print("Acc: "+str(get_acc(test_label,pred)))
    print("macro-F1: "+str(get_macro_F1(test_label,pred)))
    print("micro-F1: "+str(get_micro_F1(test_label,pred)))


main()
