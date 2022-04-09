from process_data import load_and_process_data
from evaluation import get_macro_F1,get_micro_F1,get_acc
import numpy as np
import numpy.linalg as lg

# 实现线性回归的类
class LinearClassification:

    '''参数初始化 
    lr: 梯度更新的学习率
    Lambda: L2范数的系数
    epochs: 更新迭代的次数
    '''
    def __init__(self,lr=0.05,Lambda= 0.001,epochs = 1000):
        self.lr=lr
        self.Lambda=Lambda
        self.epochs =epochs

        self.Omega = None

    '''根据训练数据train_features,train_labels计算梯度更新参数W'''
    def fit(self,train_features,train_labels):
        ''''
        需要你实现的部分
        '''
        #print(train_features)
        #print(train_labels)

        feature_rows = train_features.shape[0]
        feature_lines = train_features.shape[1]

        X = np.empty([feature_rows, feature_lines + 1], dtype = float)
        for i in range(0, feature_rows): # 0 <= i < feature_rows
            X[i][feature_lines] = 1
            for j in range(0,feature_lines):
                X[i][j] = train_features[i][j]
        #print(X)

        self.Omega = np.empty([feature_lines + 1 , 1],dtype = float)
        #print(self.Omega)

        I = np.eye(feature_lines + 1)
        #print(I)
        #print(X.transpose().dot(X))
        self.Omega = lg.inv((X.transpose().dot(X) + (self.Lambda/2)*I)).dot(X.transpose()).dot(train_labels)
        print('omega:',self.Omega)



    '''根据训练好的参数对测试数据test_features进行预测，返回预测结果
    预测结果的数据类型应为np数组，shape=(test_num,1) test_num为测试数据的数目'''
    def predict(self,test_features):
        ''''
        需要你实现的部分
        '''
        feature_rows = test_features.shape[0]
        feature_lines = test_features.shape[1]
        #print(feature_rows)
        pred = np.empty([feature_rows,1],dtype = float)

        X = np.empty([feature_rows, feature_lines + 1], dtype = float)
        for i in range(0, feature_rows): # 0 <= i < feature_rows
            X[i][feature_lines] = 1
            for j in range(0,feature_lines):
                X[i][j] = test_features[i][j]
        #print(X)

        pred = X.dot(self.Omega)

        pred_int = np.empty([feature_rows,1],dtype = int)

        for i in range(0,feature_rows):
            pred_int[i][0] = round(pred[i][0])
        #print(pred_int)

        return pred_int



def main():
    # 加载训练集和测试集
    train_data,train_label,test_data,test_label=load_and_process_data()
    lR=LinearClassification()
    lR.fit(train_data,train_label) # 训练模型
    pred=lR.predict(test_data) # 得到测试集上的预测结果

    # 计算准确率Acc及多分类的F1-score
    print("Acc: "+str(get_acc(test_label,pred)))
    print("macro-F1: "+str(get_macro_F1(test_label,pred)))
    print("micro-F1: "+str(get_micro_F1(test_label,pred)))

    # omega =  train_label[0] * train_data[0]
    # omega = omega + (train_label[1] * train_data[1])
    # #for irows in range(1,2):
    #        # omega = omega + train_label[irows] * train_data[irows]
    # omega = np.array(omega)
    # #omega = omega.transpose()
    # #omega = omega.reshape([train_data.shape[1],1])
    # print(omega)
    # print(type(omega))
    # print(omega.shape)


    # print(train_data[0])
    # print(type(train_data[0]))
    # print(train_data[0].shape)
    # a = train_data[0].dot(train_data[1].transpose())
    # print(a)



main()

