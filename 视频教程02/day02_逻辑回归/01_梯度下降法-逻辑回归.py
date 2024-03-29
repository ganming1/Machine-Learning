import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import classification_report
from sklearn import preprocessing

# 数据是否需要标准化
scale = False

# 一、载入数据
def get_data():
    data = np.genfromtxt("LR-testSet.csv", delimiter=",")
    x_data = data[:, :-1]
    y_data = data[:, -1]

    return x_data, y_data

# 二、散点图显示数据
def date_show():
    x_data, y_data = get_data()
    print(y_data[0])
    x0 = []
    x1 = []
    y0 = []
    y1 = []
    # 切分不同类别的数据
    for i in range(len(x_data)):
        if y_data[i] == 0:
            x0.append(x_data[i, 0])
            y0.append(x_data[i, 1])
        else:
            x1.append(x_data[i, 0])
            y1.append(x_data[i, 1])

    # 画图
    scatter0 = plt.scatter(x0, y0, c='b', marker='o')
    scatter1 = plt.scatter(x1, y1, c='r', marker='x')
    # 画图例
    plt.legend(handles=[scatter0, scatter1], labels=['label0', 'label1'], loc='best')
    # plt.show()


# 三、数据处理，添加偏置项
def data_process():
    data = np.genfromtxt("LR-testSet.csv", delimiter=",")
    x_data = data[:, :-1]
    y_data = data[:, -1, np.newaxis]

    # print(np.mat(x_data).shape)
    # print(np.mat(y_data).shape)

    # 给样本添加偏置项
    X_data = np.concatenate((np.ones((100, 1)), x_data), axis=1)
    # print(X_data.shape)
    return X_data, y_data


# 四、定义 sigmoid 函数
def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


# 五、计算误差平均值
def cost(xMat, yMat, ws):
    left = np.multiply(yMat, np.log(sigmoid(xMat * ws)))
    right = np.multiply(1 - yMat, np.log(1 - sigmoid(xMat * ws)))
    return np.sum(left + right) / -(len(xMat))


# 六、手写得到权值系数
def gradAscent(xArr, yArr):
    if scale == True:
        xArr = preprocessing.scale(xArr)
    xMat = np.mat(xArr)
    yMat = np.mat(yArr)

    lr = 0.001
    epochs = 10000
    costList = []
    # 计算数据行列数
    # 行代表数据个数，列代表权值个数
    m, n = np.shape(xMat)
    # 初始化权值
    ws = np.mat(np.ones((n, 1)))

    for i in range(epochs + 1):
        # xMat和weights矩阵相乘
        h = sigmoid(xMat * ws)
        # 计算梯度，调整权值
        ws_grad = xMat.T * (h - yMat) / m
        ws = ws - lr * ws_grad

        if i % 50 == 0:
            costList.append(cost(xMat, yMat, ws))
    return ws, costList


# 七、得到模型，画图
def xianshi_demo():
    x_data, y_data = data_process()
    # 训练模型，得到权值和cost值的变化
    ws, costList = gradAscent(x_data, y_data)
    print(ws)

    if scale == False:
        # 画图决策边界
        date_show()    # 画散点
        x_test = [[-4], [3]]    # 表示 x1
        # 根据 w0 + x1 * w1 + x2 * w2 = 0 求得 y_test 即 x2 .
        y_test = (-ws[0] - x_test * ws[1]) / ws[2]   # 表示 x2
        plt.plot(x_test, y_test, 'k')
        plt.show()

    # 画图 loss值的变化
    x = np.linspace(0, 10000, 201)
    plt.plot(x, costList, c='r')
    plt.title('Train')
    plt.xlabel('Epochs')
    plt.ylabel('Cost')
    plt.show()


# 八、预测函数
def predict(x_data, ws):
    if scale == True:
        x_data = preprocessing.scale(x_data)
    xMat = np.mat(x_data)
    ws = np.mat(ws)
    # y_predictions = []
    # for x in sigmoid(xMat * ws):
    #     if x >= 0.5:
    #         y_predictions.append(1)
    #     else:
    #         y_predictions.append(0)
    # return y_predictions
    return [1 if x >= 0.5 else 0 for x in sigmoid(xMat * ws)]


# 九、测试函数
def try_demo():
    x_data, y_data = data_process()
    ws, costList = gradAscent(x_data, y_data)
    predictions = predict(x_data, ws)
    print(classification_report(y_data, predictions))


if __name__ == '__main__':
    # 代码1：

    # 代码2：
    date_show()

    # 代码7：得到模型，画图
    # xianshi_demo()

    # 代码9：测试函数
    # try_demo()

