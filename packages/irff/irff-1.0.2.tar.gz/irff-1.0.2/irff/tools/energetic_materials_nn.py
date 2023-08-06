#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals
import pathlib
import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import initializers
from tensorflow.keras import layers, losses

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # 只显示warning 和 error
print(tf.__version__)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def extrat_columns(dataset, column_list=[]):
    # 提取需要的列的数据 并删除含有空值的行
    dataset = dataset[column_list]
    # print(dataset.shape)
    # print(dataset.isna().sum())  # 统计空白数据
    dataset = dataset.dropna()  # 删除含有空数据的整行
    # print(dataset.shape)
    return dataset


class Network(keras.Model):
    # 回归网络
    def __init__(self):
        super(Network, self).__init__()
        # 创建3个全连接层
        # bias_initializer = initializers.Zeros()
        # activation='relu'  'sigmoid'
        # 3个隐藏层 3*25 拟合25000步 效果不错  1.9889899492263794 1.5650410652160645
        # 2个隐藏层 2*36 拟合50000步 效果不错  1.8222154378890991 1.8216800689697266
        self.fc1 = layers.Dense(36, activation='relu',
                                kernel_initializer=initializers.RandomNormal(stddev=0.2),
                                bias_initializer=initializers.RandomNormal(stddev=0.2))
        self.fc2 = layers.Dense(36, activation='relu',
                                kernel_initializer=initializers.RandomNormal(stddev=0.2),
                                bias_initializer=initializers.RandomNormal(stddev=0.2))

        self.fc3 = layers.Dense(1)

    def call(self, inputs, training=None, mask=None):
        # 依次通过3个全连接层
        x = self.fc1(inputs)
        x = self.fc2(x)
        x = self.fc3(x)

        return x


def get_data(excel_name, skiprows, column_list):
    # 获得训练数据及测试数据
    IO = os.getcwd() + '/{}'.format(excel_name)
    # skiprows=excel中column名称对应的行号-1
    dataset = pd.read_excel(io=IO, skiprows=skiprows, index_col=0)
    print(dataset.columns)
    # 提取 nn 输入输出数据 并删除带有空值的行
    dataset = extrat_columns(dataset, column_list=column_list)
    return dataset


def pairplot(dataset):
    # 获得 统计数据 图
    plot = sns.pairplot(dataset, diag_kind="kde")
    plot.savefig('pairplot')


def training_test(dataset, normalizeFactor, column_list, input_feathre_No, learning_rate, epoch_No, batch,
                  train_frac):
    # 训练及测试
    # 切分为训练集和测试集
    train_dataset = dataset.sample(frac=train_frac, random_state=0)  # random_state: 设定随机种子
    test_dataset = dataset.drop(train_dataset.index)

    # 标准化数据
    # print(train_dataset.head())
    normed_train_data = np.divide(train_dataset, normalizeFactor)
    # print(normed_train_data.head())
    normed_test_data = np.divide(test_dataset, normalizeFactor)

    # 设定真实标签Y
    normed_train_labels = normed_train_data.pop(column_list[-1])
    normed_test_labels = normed_test_data.pop(column_list[-1])

    model = Network()
    # 通过调用类的 build 方法并指定输入大小，即可自动创建所有层的内部张量。
    model.build(input_shape=(None, input_feathre_No))  #
    # 通过 summary()函数可以方便打印出网络结构和参数量，就必须先把网络所有内部结构都定下来
    model.summary()  # 打印出模型概述信息

    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    if batch[0]:
        # 构建Dataset 对象
        train_db = tf.data.Dataset.from_tensor_slices((normed_train_data.values, normed_train_labels.values))
        # 随机打散，批量化
        train_db = train_db.shuffle(100).batch(batch_size=batch[1])

    train_mse_losses = []
    test_mse_losses = []

    for epoch in range(epoch_No):
        if batch[0]:
            # ------ with batch --------------
            for step, (x, y) in enumerate(train_db):
                # print(y.shape)
                with tf.GradientTape() as tape:
                    out = tf.squeeze(model(x))*normalizeFactor[-1]
                    y = y*normalizeFactor[-1]
                    # y = tf.cast(y, tf.float32)  # 与out保持一致
                    # print(y)
                    # loss = tf.reduce_mean(losses.MSE(y, out))  # 均方根误差（MSE）
                    loss = tf.nn.l2_loss(out-y, name='loss')  # sum(t**2)/2
            # ------ with batch --------------
        if not batch[0]:
            # ------ without batch --------------
            with tf.GradientTape() as tape:
                # print(normed_train_data.values.shape)
                out = tf.squeeze(model(normed_train_data.values))*normalizeFactor[-1]
                y = normed_train_labels.values*normalizeFactor[-1]
                # print(out, normed_train_labels.values)
                # 均方根误差（MSE）
                # loss = tf.reduce_mean(losses.MSE(y, out))
                loss = tf.nn.l2_loss(out-y, name='loss')  # sum(t**2)/2
            # ------ without batch --------------

        grads = tape.gradient(loss, model.trainable_variables)
        optimizer.apply_gradients(zip(grads, model.trainable_variables))

        train_mse_losses.append(float(loss))
        out = tf.squeeze(model(tf.constant(normed_test_data.values)))  # 测试集模型预测输出
        # 测试集 mse
        # print((out-normed_test_labels).shape)
        test_mse_losses.append(float(tf.nn.l2_loss(out*normalizeFactor[-1]-normed_test_labels*normalizeFactor[-1], name='loss')))
        # test_mse_losses.append(float(tf.reduce_mean(losses.MSE(normed_test_labels*normalizeFactor[-1], out*normalizeFactor[-1]))))

        if epoch % 100 == 0:
            print(epoch, float(loss), test_mse_losses[-1])

    train_out = tf.squeeze(model(normed_train_data.values)*normalizeFactor[-1])
    test_out = tf.squeeze(model(tf.constant(normed_test_data.values))*normalizeFactor[-1])

    return train_mse_losses, test_mse_losses, train_out, test_out, \
           normed_train_labels*normalizeFactor[-1], normed_test_labels*normalizeFactor[-1]


def plot_loss(train_mse_losses, test_mse_losses, fig_name='loss.png'):
    # 绘制每个epoch时的train_mse_losses, test_mse_losses
    train_mse_losses = train_mse_losses[500:]
    test_mse_losses = test_mse_losses[500:]
    # print(train_mse_losses)
    plt.figure()
    plt.xlabel('Epoch')
    plt.ylabel('MSE')
    plt.plot(train_mse_losses, label='Train')

    plt.plot(test_mse_losses, label='Test')
    plt.legend()

    plt.legend()
    plt.savefig(fig_name)
    plt.show()


def plot_output_errorbar(y_pred, y_lables, fig_name='auto.png'):
    # 绘制结束时 训练与测试集的 输出值差异
    y = np.array(y_lables.values)
    # print(y)
    X = list(range(len(y)))
    
    plt.figure()
    plt.scatter(X, y, c='none', edgecolors='blue', linewidths=1,
                marker='o', s=32, label='Detonation velocity',
                alpha=1.0)
    yp = y_pred
    err = y - yp
    # print(err)
    plt.errorbar(X, yp, yerr=err,
                 fmt='s', ecolor='r', color='r', ms=6, markerfacecolor='none', mec='r',
                 elinewidth=2, capsize=2, label='Prediction')
    plt.legend(loc='best', edgecolor='yellowgreen')
    plt.savefig(fig_name)
    plt.show()


def run():
    # 需要调节参数
    # ------------------- parametrs-------------------
    excel_name = 'Characteristics of energetic materials_2020.6.18_LCY.xlsx'
    skiprows = 26  # skiprows=excel中column名称对应的行号-1
    """
    # Vd_Cal
    column_list = ['rou', 'PC ', 'N_rou', 'OB',  # input parameters
                   'Vd_Cal']  # output
    normalizeFactor = [3.0, 100.0, 1.0, 100.0, 10]
    """
    # Hd_Cal
    column_list = ['rou', 'PC ', 'N_rou', 'OB',  # input parameters
                   'Hd_Cal']  # output
    normalizeFactor = [3.0, 100.0, 1.0, 100.0, 10]

    input_feathre_No = 4
    learning_rate = 0.0005
    epoch_No = 50000
    batch = [False, 200]
    train_frac = 0.8
    # ------------------- parametrs-------------------

    # 读取 获取输入输出数据 删除带有空值的行
    dataset = get_data(excel_name, skiprows, column_list)

    # 获得 统计数据 图
    # pairplot(dataset[column_list])

    # training
    train_mse_losses, test_mse_losses, train_out, test_out, train_labels, test_labels = training_test\
        (dataset, normalizeFactor, column_list, input_feathre_No, learning_rate, epoch_No, batch, train_frac)
    # 创建会话
    # 绘制每个epoch时的train_mse_losses, test_mse_losses
    # print(train_mse_losses, test_mse_losses)
    plot_loss(train_mse_losses, test_mse_losses, fig_name='loss.png')

    # 绘制结束时 训练与测试集的 输出值差异
    plot_output_errorbar(train_out, train_labels, fig_name='train_err.png')
    plot_output_errorbar(test_out, test_labels, fig_name='test_err.png')


if __name__ == '__main__':
    run()