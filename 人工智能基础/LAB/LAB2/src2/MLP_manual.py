import numpy as np
import random
import matplotlib.pyplot as plt


#sigmoid激活函数
def sigmoid(x):
    return 1/(1 + pow(np.e,-x))

#归一化函数
def softmax(x, axis=1):
    # 计算每行的最大值
    row_max = x.max(axis=axis)
    # 每行元素都需要减去对应的最大值，否则求exp(x)会溢出，导致inf情况
    row_max=row_max.reshape(-1, 1)
    x = x - row_max
    # 计算e的指数次幂
    x_exp = np.exp(x)
    x_sum = np.sum(x_exp, axis=axis, keepdims=True)
    s = x_exp / x_sum
    return s


class HiddenLayer(object):
    def __init__(self, rng, input, n_in, n_out, W = None, b = None, activation = sigmoid):
        #输入。隐层的输入即 input，输出即隐藏层的神经元个数。输入层与隐层是全连接
        self.activation = activation
        self.input = input

        #print(n_in,n_out)
        #如果W未初始化，则根据以下方法初始化。
        if W is None:
            W_values = np.asarray(
                rng.uniform(
                    low = -np.sqrt(6.0 / (n_in + n_out)),
                    high = np.sqrt(6.0 / (n_in + n_out)),
                    size = (n_out, n_in)
                ),
            )
            W_values = W_values * 4
            W = W_values

            #print('w:')
            #print(W)
            #print(W.shape)

        if b is None:
            #b_values = np.zeros((n_out,), dtype=theano.config.floatX)
            b = np.zeros((n_out,1))
            #b = theano.shared(value=b_values, name='b', borrow=True)

        #用上面定义的W、b来初始化类HiddenLayer的W、b
        self.W = W
        #self.b = b

        #print(type(input))
        #print(type(W))
        #print(type(b))

        #print(input.shape)
        #print(W.shape)
        #print(b.shape)
        self.run()

    def run(self):
        #隐含层的输出
        self.lin_output = self.W.dot(self.input) #+ self.b.transpose()
        self.output = (
            self.lin_output if self.activation is None
            else self.activation(self.lin_output)
        )
        #print(self.output)
        #print(self.output.shape)

        #隐含层的参数
        self.params = [self.W]#, self.b]


    def updateW(self,NewW):
        self.W = NewW
        self.run()



#参数说明：
#input，大小就是(n_example,n_in)，其中n_example是一个batch的大小，
#因为我们训练时用的是Minibatch SGD，因此input这样定义
#n_in,即上一层(隐含层)的输出
#n_out,输出的类别数
class LogisticRegression(object):
    def __init__(self, input, n_in, n_out):
        #W大小是n_in行n_out列，b为n_out维向量。即：每个输出对应W的一列以及b的一个元素。
        self.W = np.zeros((n_out, n_in), dtype = float)
        #self.b = np.zeros((n_out,1),dtype = float)
        self.input = input

        #input是(n_example,n_in)，W是（n_in,n_out）,点乘得到(n_example,n_out)，加上偏置b，
        #再作为T.nnet.softmax的输入，得到p_y_given_x
        #故p_y_given_x每一行代表每一个样本被估计为各类别的概率
        #PS：b是n_out维向量，与(n_example,n_out)矩阵相加，内部其实是先复制n_example个b，
        #然后(n_example,n_out)矩阵的每一行都加b

        #print(input)
        #print(self.W)
        #print(self.b)
        self.run(self.input)

    def run(self,input):
        # print("info:")
        # print(self.W.shape)
        # print(input.shape)
        # print('input:',input)
        #print('W3:',self.W)
        self.p_y_given_x = softmax(self.W.dot(input).transpose()) #+ self.b.transpose())
        #print("info:",self.p_y_given_x)
        #argmax返回最大值下标，因为本例数据集是MNIST，下标刚好就是类别。axis=1表示按行操作。
        self.y_pred = np.argmax(self.p_y_given_x, axis = 1) + 1

        #params，LogisticRegression的参数
        self.params = [self.W]#, self.b]

    def updateW(self,NewW):
        self.W = NewW
        self.run(self.input)

#3层的MLP
class MLP(object):
    def __init__(self, rng, input, n_in, n_hidden, n_out):
        self.hiddenLayer1 = HiddenLayer(
            rng = rng,
            input = input,
            n_in = n_in,
            n_out = n_hidden,
            activation = sigmoid
        )

        self.hiddenLayer2 = HiddenLayer(
            rng = rng,
            input = self.hiddenLayer1.output,
            n_in = n_hidden,
            n_out = n_hidden,
            activation = sigmoid
        )

        #将隐含层hiddenLayer的输出作为分类层logRegressionLayer的输入，这样就把它们连接了
        self.logRegressionLayer = LogisticRegression(
            input = self.hiddenLayer2.output,
            n_in = n_hidden,
            n_out = n_out
        )

        #以上已经定义好MLP的基本结构，下面是MLP模型的其他参数或者函数

        # #规则化项：常见的L1、L2_sqr
        # self.L1 = (
        #     abs(self.hiddenLayer.W).sum()
        #     + abs(self.logRegressionLayer.W).sum()
        # )
        #
        # self.L2_sqr = (
        #     (self.hiddenLayer.W ** 2).sum()
        #     + (self.logRegressionLayer.W ** 2).sum()
        # )


        # #损失函数Nll（也叫代价函数）
        # self.negative_log_likelihood = (
        #     self.logRegressionLayer.negative_log_likelihood
        # )
        #
        # #误差
        # self.errors = self.logRegressionLayer.errors

        # #MLP的参数
        # self.params = self.hiddenLayer.params + self.logRegressionLayer.params
        # # end-snippet-3


def main(learning_rate=0.0001, L1_reg=0.00, L2_reg=0.0001, n_epochs=10,
         dataset='mnist.pkl.gz', batch_size=20, n_hidden=4):
        # learning_rate学习速率，梯度前的系数。
        # L1_reg、L2_reg：正则化项前的系数，权衡正则化项与Nll项的比重
        # 代价函数=Nll+L1_reg*L1或者L2_reg*L2_sqr
        # n_epochs：迭代的最大次数（即训练步数），用于结束优化过程
        # dataset：训练数据的路径
        # n_hidden:隐藏层神经元个数
        # batch_size=20，即每训练完20个样本才计算梯度并更新参数
    rng = np.random.RandomState(1234)
    #随机生成测试样例以及标签
    train_data = np.empty([100,5],dtype = float)
    for irows in range(0,100):
        for ilines in range(0,5):
            train_data[irows][ilines] = random.random() * 10
    train_data = train_data.transpose()
    #print(train_data)
    train_label = np.empty([100,1],dtype = int)
    for irows in range(0,100):
        train_label[irows][0] = random.randint(1,3)
    #print(train_label)
    feature_rows = train_data.shape[0]
    feature_lines = train_data.shape[1]

    initValue = np.empty([5,1])
    for i in range(0,5):
        initValue[i][0] = train_data[i][0]


    #生成一个MLP，命名为classifier
    classifier = MLP(
        rng = rng,
        input = initValue,
        n_in = 5,
        n_hidden = n_hidden,
        n_out = 3
    )

    #print(classifier.logRegressionLayer.p_y_given_x)
    #print(classifier.logRegressionLayer.y_pred)

    #print(classifier.hiddenLayer1.W.shape)
    #print(classifier.hiddenLayer1.output.shape)
    #print(h2.shape)

    #绘图参数
    label_L = []
    label_n = []

    n_epochs = 1000#迭代次数
    # for train_times in range(0,n_epochs):
    #     print('times:',train_times)
    #     #训练次数
    #
    #     h1 = classifier.hiddenLayer1.output
    #     h2 = classifier.hiddenLayer2.output
    #     yHat = classifier.logRegressionLayer.p_y_given_x
    #
    #     ls3 = np.empty([3 , feature_lines])
    #     for ilines in range(0,feature_lines):
    #         for irows in range(0,3):
    #             if irows + 1 == train_label[ilines][0]:
    #                 ls3[irows][ilines] = classifier.logRegressionLayer.p_y_given_x[ilines][irows] - 1
    #             else:
    #                 ls3[irows][ilines] = classifier.logRegressionLayer.p_y_given_x[ilines][irows]
    #     #print(ls3.shape)
    #     #print(ls3)
    #     dLW3 = ls3.dot(h2.transpose())
    #     #print(dLW3)
    #     #print(dLW3.shape)
    #     #print(classifier.logRegressionLayer.W.shape)
    #
    #     ds2 = np.empty([4,100])
    #     w2h1 = classifier.hiddenLayer2.lin_output
    #     for irows in range(0,4):
    #         for ilines in range(0,100):
    #             ds2[irows][ilines] = sigmoid(w2h1[irows][ilines]) * (1 - sigmoid(w2h1[irows][ilines]))
    #     dLW2 =  ((classifier.logRegressionLayer.W.transpose().dot(ls3))*ds2).dot(h1.transpose())
    #     #print(dLW2)
    #     #print(dLW2.shape)
    #
    #     ds1 = np.empty([4,100])
    #     w1h1 = classifier.hiddenLayer1.lin_output
    #     for irows in range(0,4):
    #         for ilines in range(0,100):
    #             ds1[irows][ilines] = sigmoid(w1h1[irows][ilines]) * (1 - sigmoid(w1h1[irows][ilines]))
    #     dLW1 = ((classifier.hiddenLayer2.W.transpose().dot(classifier.logRegressionLayer.W.transpose().dot(ls3) * ds2))*ds1).dot(train_data.transpose())
    #     #print(dLW1)
    #     #print(dLW1.shape)
    #
    #     classifier.logRegressionLayer.input = classifier.hiddenLayer2.output
    #     newW3 = classifier.logRegressionLayer.W - learning_rate * dLW3
    #     classifier.logRegressionLayer.updateW(newW3)
    #
    #     classifier.hiddenLayer2.input = classifier.hiddenLayer1.output
    #     newW2 = classifier.hiddenLayer2.W - learning_rate * dLW2
    #     classifier.hiddenLayer2.updateW(newW2)
    #
    #     newW1 = classifier.hiddenLayer1.W - learning_rate * dLW1
    #     classifier.hiddenLayer1.updateW(newW1)
    #
    #
    #     #统计损失函数
    #     L = 0
    #     for i in range(0,100):
    #         L = L - np.log(classifier.logRegressionLayer.p_y_given_x[i][train_label[i][0] - 1])
    #     print('L:',L)
    #     #print(classifier.logRegressionLayer.p_y_given_x.shape)


    for train_times in range(0,n_epochs):
        print('times:',train_times)
        #训练次数
        for itrainN in range(0,100):
            #每行更新一次
            print('times_row:',itrainN)
            h1 = classifier.hiddenLayer1.output
            h2 = classifier.hiddenLayer2.output
            yHat = classifier.logRegressionLayer.p_y_given_x
            x = np.empty([5,1])
            for i in range(0,5):
                x[i][0] = train_data[i][itrainN]

            ls3 = np.empty([3 , 1])
            for irows in range(0,3):
                if irows + 1 == train_label[itrainN][0]:
                    ls3[irows][0] = classifier.logRegressionLayer.p_y_given_x[0][irows] - 1
                else:
                    ls3[irows][0] = classifier.logRegressionLayer.p_y_given_x[0][irows]
            # print(ls3.shape)
            # print(ls3)
            dLW3 = ls3.dot(h2.transpose())
            #print(dLW3)
            #print(dLW3.shape)
            #print(classifier.logRegressionLayer.W.shape)

            ds2 = np.empty([4,1])
            w2h1 = classifier.hiddenLayer2.lin_output
            for irows in range(0,4):
                for ilines in range(0,1):
                    ds2[irows][ilines] = sigmoid(w2h1[irows][ilines]) * (1 - sigmoid(w2h1[irows][ilines]))
            dLW2 =  ((classifier.logRegressionLayer.W.transpose().dot(ls3))*ds2).dot(h1.transpose())
            #print(dLW2)
            #print(dLW2.shape)

            ds1 = np.empty([4,1])
            w1h1 = classifier.hiddenLayer1.lin_output
            for irows in range(0,4):
                for ilines in range(0,1):
                    ds1[irows][ilines] = sigmoid(w1h1[irows][ilines]) * (1 - sigmoid(w1h1[irows][ilines]))
            dLW1 = ((classifier.hiddenLayer2.W.transpose().dot(classifier.logRegressionLayer.W.transpose().dot(ls3) * ds2))*ds1).dot(x.transpose())
            #print(dLW1)
            #print(dLW1.shape)

            # print('dw1',dLW1)
            # print('dw2',dLW2)
            # print('dw3',dLW3)

            classifier.logRegressionLayer.input = classifier.hiddenLayer2.output
            newW3 = classifier.logRegressionLayer.W - learning_rate * dLW3
            classifier.logRegressionLayer.updateW(newW3)

            classifier.hiddenLayer2.input = classifier.hiddenLayer1.output
            newW2 = classifier.hiddenLayer2.W - learning_rate * dLW2
            classifier.hiddenLayer2.updateW(newW2)

            newW1 = classifier.hiddenLayer1.W - learning_rate * dLW1
            classifier.hiddenLayer1.updateW(newW1)

            #统计损失函数
            L = 0
            for i in range(0,1):
                L = L - np.log(classifier.logRegressionLayer.p_y_given_x[i][train_label[i][0] - 1])
            print('L:',L)
            #print(classifier.logRegressionLayer.p_y_given_x.shape)

        label_n.append(train_times)
        label_L.append(L)

        # print('预测分数：')
        # print(classifier.logRegressionLayer.p_y_given_x)

    plt.plot(label_n, label_L,label=u'L')
    plt.legend()  # 让图例生效
    plt.show()

    print('W')
    print(classifier.hiddenLayer1.W)
    print(classifier.hiddenLayer2.W)
    print(classifier.logRegressionLayer.W)

    print('true label:',train_label.transpose())

    #得到三个w矩阵，将整个train_data直接运算
    h1 = sigmoid(classifier.hiddenLayer1.W.dot(train_data))
    h2 = sigmoid(classifier.hiddenLayer2.W.dot(h1))
    yHat = softmax(classifier.logRegressionLayer.W.dot(h2))
    y_pred = np.argmax(yHat.transpose(), axis = 1) + 1
    print('pred:',y_pred)

    #统计结果正确的个数
    AccCount = 0
    count1 = 0
    for i in range(0,100):
        if y_pred[i] == train_label[i]:
            AccCount += 1
        if train_label[i] == 1:
            count1 += 1
    Acc = AccCount / 100
    print('Acc:',Acc)
    print('1:',count1)



main()
