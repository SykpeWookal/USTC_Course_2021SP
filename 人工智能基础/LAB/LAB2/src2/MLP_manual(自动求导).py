import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt

# Hyper-parameters 定义迭代次数， 学习率以及模型形状的超参数
input_size = 5
output_size = 5
num_epochs = 10000
learning_rate = 0.001


x_train = np.random.random((100, 5))
y_train = np.random.randint(0, output_size, size=(100, 1))
y_train = y_train.astype(np.float32)
x_train = x_train.astype(np.float32)
# Linear regression model  2. 定义网络结构 y=w*x+b 其中w的size [1,1], b的size[1,]
model = nn.Linear(input_size, output_size)

# Loss and optimizer 3.定义损失函数， 使用的是最小平方误差函数
criterion = nn.MSELoss()
# 4.定义迭代优化算法， 使用的是随机梯度下降算法
optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
loss_dict = []
# Train the model 5. 迭代训练
for epoch in range(num_epochs):
    # Convert numpy arrays to torch tensors  5.1 准备tensor的训练数据和标签

    inputs = torch.from_numpy(x_train)
    targets = torch.from_numpy(y_train)

    # Forward pass  5.2 前向传播计算网络结构的输出结果
    outputs = model(inputs)
    # 5.3 计算损失函数
    loss = criterion(outputs, targets)

    # Backward and optimize 5.4 反向传播更新参数
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

    # 可选 5.5 打印训练信息和保存loss
    loss_dict.append(loss.item())
    if (epoch + 1) % 5 == 0:
        print('Epoch [{}/{}], Loss: {:.4f}'.format(epoch + 1, num_epochs, loss.item()))

# Plot the graph 画出原y与x的曲线与网络结构拟合后的曲线
predicted = model(torch.from_numpy(x_train)).detach().numpy()
plt.plot(x_train, y_train, 'ro', label='Original data')
plt.plot(x_train, predicted, label='Fitted line')
plt.legend()
plt.show()

# 画loss在迭代过程中的变化情况
plt.plot(loss_dict, label='loss for every epoch')
plt.legend()
plt.show()
