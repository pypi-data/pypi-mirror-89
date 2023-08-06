#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argh
import argparse
# import energetic_materials_nn as EM_nn
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
from sklearn.linear_model import LinearRegression, Lasso, Ridge, BayesianRidge
from sklearn.metrics import mean_squared_error, r2_score, make_scorer
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
from sklearn.gaussian_process.kernels import WhiteKernel, ExpSineSquared
import xgboost as xgb
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV, cross_validate
import pprint


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join('./', fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def scale_features(X):
    # 对输入数据进行缩放
    X = np.divide(X, normalizeFactor)
    # print(X.head())
    return X.values


def display_scores(scores, model=None):
    print('********* {} *************'.format(model))
    print("Scores:", scores)
    print("Mean:", scores.mean())
    print("Standard deviation:", scores.std())
    print('\n')


def fit_model_print_error(EMs_prepared, EMs_labels, model=None):
    # 拟合 并打印误差
    model.fit(EMs_prepared, EMs_labels)
    EMs_predictions = model.predict(EMs_prepared)
    mse = mean_squared_error(EMs_labels, EMs_predictions)
    rmse = np.sqrt(mse)
    print('{}: mse  {}  rmse  {}'.format(model, mse, rmse))


def cross_val_fit_print_error(EMs_prepared, EMs_labels, model=None,
                              scoring="neg_mean_squared_error", cv=5):
    # 交叉验证 并 输出误差
    scores = cross_val_score(model, EMs_prepared, EMs_labels, scoring=scoring, cv=cv)
    rmse_scores = np.sqrt(-scores)
    display_scores(rmse_scores, model=model)


def plot_out_scatter(plot_out_scatter_para, fig_name='pre_lable_scatter.png'):
    # 绘制训练 验证 与测试集的输出 和 真实值
    # 获得数据的边界值 来绘制直线
    plt_data = plot_out_scatter_para['data']
    plt_lable = plot_out_scatter_para['label']
    plt_c = plot_out_scatter_para['c']
    data_all = []
    for value_pair in plt_data:
        data_all.append(np.array(value_pair[0]).tolist())
        data_all.append(np.array(value_pair[1]).tolist())
    edge_min = max(map(max, data_all))
    edge_max = min(map(min, data_all))
    # print(edge_min, edge_max)

    plt.figure()
    plt.title(fig_name, fontsize=20, fontproperties='SimHei')
    plt.xlabel('Lable')
    plt.ylabel('Prediction')

    for index, value in enumerate(plt_data):
        plt.scatter(value[0], value[1],
                    label=plt_lable[index],
                    c=plt_c[index], alpha=0.6)
    # 简单理解就是：先写x的取值范围，再写y的取值范围
    plt.plot([edge_min, edge_max], [edge_min, edge_max], c='black', alpha=0.6)
    plt.legend()
    plt.savefig(fig_name)
    # plt.show()


def my_custom_score_func(lable, prediction):
    # 计算真实值和预测值相关系数
    lable = np.array(lable).tolist()
    prediction = np.array(prediction).tolist()
    pair = np.array([lable, prediction])
    coeff = np.corrcoef(pair)
    # print(coeff, coeff[0][1])
    return coeff[0][1]


def get_data(excel_name, skiprows):
    # 获得训练数据及测试数据
    IO = os.getcwd() + '/{}'.format(excel_name)
    # skiprows=excel中column名称对应的行号-1
    dataset = pd.read_excel(io=IO, skiprows=skiprows, index_col=2)
    # print(dataset.columns)
    return dataset


def extrat_columns(dataset, column_list=None, delNull=True):
    # 提取需要的列的数据 并删除含有空值的行
    dataset = dataset[column_list]
    # print(dataset.shape)
    # print(dataset.isna().sum())  # 统计空白数据
    if delNull: dataset = dataset.dropna()  # 删除含有空数据的整行
    # print(dataset.shape)
    return dataset


def Merge2number(dtClmns, column_list):
    # 几列对勾形式整合成一列序号形式
    dtClmns = dtClmns[column_list]
    # print(dtClmns.iloc[0, 0])
    indx = dtClmns.shape[0]
    clmn = dtClmns.shape[1]
    # ndarray 装数字
    mrgdata = np.zeros(indx)
   # 取得数字
    for i in range(indx):  # index 循环
        for c in range(clmn):  # column 循环
            if dtClmns.iloc[i, c] == '√': mrgdata[i] = c+1
    # 插入dtClmns
    dtClmns.insert(0, 'merge_number', mrgdata)
    # print(dtClmns)
    return dtClmns


def merge_columns(EMs, column_list, column_name='New_column'):
    # 合并含对勾的列为数字 并在EMs最后添加列
    Packing_type = Merge2number(EMs, column_list)
    EMs[column_name] = Packing_type['merge_number']
    return EMs


def correlation_coefficient(lable, prediction):
    # 计算真实值和预测值相关系数
    lable = np.array(lable).tolist()
    prediction = np.array(prediction).tolist()
    pair = np.array([lable, prediction])
    coeff = np.corrcoef(pair)
    # print(coeff, coeff[0][1])
    return coeff[0][1]


def plot_output_errorbar(y_pred, y_lables, fig_name='auto.png'):
    # 绘制结束时 训练与测试集的 输出值差异
    y = np.array(y_lables.values)
    # print(y)
    X = list(range(len(y)))

    plt.figure()
    plt.title(fig_name, fontsize=20, fontproperties='SimHei')
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
    # plt.show()


def get_relative_error(y_pred, y_lables):
    # 计算 预测值和真实值相对误差  百分制
    y_pred = np.around(np.array(y_pred),4)
    y = np.array(y_lables.values)
    # 百分制
    relative_error = np.around(np.abs(np.array((y_pred - y)/y))*100, 4)
    # relative_error = np.abs(np.around(np.array((y_pred-y)/y),4))*100
    error_results = y_lables.reset_index(name='y_lables')
    error_results['y_pred'] = y_pred
    error_results['relative error (%)'] = relative_error
    # print(results)
    return error_results


def write_error(error_results, filename='error.csv'):
    # 将误差写入文件
    path = os.getcwd()
    error_results.to_csv('{}/{}'.format(path,filename), index=False, header=True, encoding="utf_8_sig")


def show_results(model,train_inputs,train_labels,title="Random Forest Regression"):
    y = model.predict(train_inputs)
    mse_ = np.mean(np.square(y-train_labels))
    score= model.score(train_inputs,train_labels)
    print(' * mse: ', mse_)
    print(' * score: ', score)
    
    n = len(train_labels)
    x = np.linspace(0,n,n)
    # Plot the results
    plt.figure()
    plt.scatter(x,train_labels, c="k", label="samples")
    # plt.plot(x,y, c="g", label="RandomForestRegression", linewidth=2)
    err = y - train_labels
    plt.errorbar(x,y,yerr=err,
                 fmt='s',ecolor='r',color='r',ms=6,markerfacecolor='none',mec='r',
                 elinewidth=2,capsize=2,label='Prediction')
    plt.xlabel("data")
    plt.ylabel("target")
    plt.title(title)
    plt.legend()
    plt.savefig('Results-%s.svg' %title,transparent=True)


def get_data_le():
    excel_name = 'Parameters-v7-20200910-LCY.xlsx'
    skiprows = 24  # skiprows=excel中column名称对应的行号-1
    normalizeFactor = [2.5, 100.0, 1.0, 100.0]
    scale = False  # 是否对输入输出归一化
    # 获取表格数据
    EMs = get_data(excel_name, skiprows)
    # print(' * head \n',EMs.head())
    # print(' * columns \n',EMs.columns)
    # 合并含对勾的列为数字 并在EMs最后添加列
    # 合并Packing type
    column_list = ['Packing_type1', 'Packing_type2', 'Packing_type3', 'Packing_type4']
    EMs = merge_columns(EMs, column_list, column_name='Packing_type')
    # print(EMs.head())

    # 合并Molecular_backbone
    column_list = ['Molecular_backbone1', 'Molecular_backbone2', 'Molecular_backbone3',
                   'Molecular_backbone4', 'Molecular_backbone5', 'Molecular_backbone6']
    EMs = merge_columns(EMs, column_list, column_name='Molecular_backbone')

    # ############################################################
    # Vd_Cal
    # 所有可以输入的特征
    column_list = ['density', 'PC', 'densityN', 'OB', 'Packing_type',
                   'mixed_molecule1', 'mixed_molecule2', 'mixed_molecule3', 'mixed_molecule4', 'mixed_molecule5',
                   'HB_amount', 'strongest_HB_length', 'strongest_HB_strength', 'MW', 'Molecular_backbone',
                   'Functional_group1', 'Functional_group2', 'Functional_group3', 'Functional_group4',
                   'Functional_group5', 'Detonation_product1', 'Detonation_product2', 'Detonation_product3',
                   'Detonation_product4', 'Detonation_product5', 'Detonation_product6',
                   '1st_weakest_bond_strength',
                   'LE']

    column_lables = 'LE'
    dataset_use = extrat_columns(EMs, column_list=column_list)

    # 创建测试集  分层采样
    # 新添加一列 编号分层
    dataset_use["density_cat"] = pd.cut(dataset_use["density"], bins=[0., 1.7, 1.8, 1.9, np.inf], labels=[1, 2, 3, 4])
    # print(dataset_use.head())
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    # seed = 7
    # test_size = 0.33
    # X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=test_size, random_state=seed)
    # accuracy = accuracy_score(y_test, predictions)
    for train_index, test_index in split.split(dataset_use, dataset_use["density_cat"]):
        strat_train_set = dataset_use.iloc[train_index]
        strat_test_set = dataset_use.iloc[test_index]

    # 删除income_cat属性，使数据回到初始状态
    for set in (strat_train_set, strat_test_set):
        set.drop(["density_cat"], axis=1, inplace=True)
    # print(strat_test_set.head())

    # 为机器学习准备数据
    train_inputs = strat_train_set.drop(column_lables, axis=1)  # 输入
    train_labels = strat_train_set[column_lables].copy()        # 输出

    test_inputs = strat_test_set.drop(column_lables, axis=1)  # 输入
    test_labels = strat_test_set[column_lables].copy()        # 输出
    # print(len(train_labels))
    # print(len(test_labels))
    if scale:
       train_inputs = scale_features(train_inputs)
       train_labels = np.divide(train_labels, 10)
       test_inputs = scale_features(test_inputs)
       test_labels = np.divide(test_labels, 10)
    return train_inputs,train_labels,test_inputs,test_labels,column_list


def mlp():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    mlr = MLPRegressor((32, 32), max_iter=20000)
    mlr.fit(train_inputs, train_labels)
    score = mlr.score(train_inputs, train_labels)
    print(' * train set score: ',score)
    score = mlr.score(test_inputs, test_labels)
    print(' * test set score: ',score)
    # print('feature importances:',mlr.feature_importances_)
    show_results(mlr,train_inputs,train_labels,title="Multi-layer Perceptron regressor (train set)")
    show_results(mlr,test_inputs,test_labels,title="Multi-layer Perceptron regressor (test set)")

def xg():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    xgr = xgb.XGBRegressor(reg_lambda=3,max_depth=6)
    xgr.fit(train_inputs, train_labels)
    score = xgr.score(train_inputs, train_labels)
    print(' * train set score: ',score)
    score = xgr.score(test_inputs, test_labels)
    print(' * test set score: ',score)
    feature_importances = xgr.feature_importances_

    print(' * feature importances: \n')
    for i in range(len(column_list)-1):
        print(column_list[i],feature_importances[i])
    # pprint.pprint(sorted(zip(feature_importances, column_list), reverse=True))

    show_results(xgr,train_inputs,train_labels,title="XGBoost Regression (train set)")
    show_results(xgr,test_inputs,test_labels,title="XGBoost Regression (test set)")

def rfgs():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    # --------------------调参--------------------------------------------------------
    # 随机森林
    param_grid  = [{'n_estimators': [490,500, 510,520,530],  #
                    'min_weight_fraction_leaf': [0, 0.1, 0.3,0.5]}  #
                  ]
    model_reg   = RandomForestRegressor(random_state=42, oob_score=True)

    # train
    grid_search = GridSearchCV(model_reg, param_grid, cv=5,
                               scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(train_inputs, train_labels)
    print('best params: ', grid_search.best_params_)
    cvres = grid_search.cv_results_
    # 找出best_params_位置 在结果中的位置
    best_index = grid_search.best_index_
    # 最佳模型 交叉验证的 mean_train_rmse mean_test_rmse
    mean_train_rmse = np.sqrt(-cvres["mean_train_score"][best_index])
    mean_test_rmse = np.sqrt(-cvres["mean_test_score"][best_index])

    print('- '*20, '\nbest model cross:\n',
                   'mean train rmse: {:<.4f}, mean test rmse: {:<.4f}'.format(mean_train_rmse, mean_test_rmse))
    # 每种参数的score
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #     print(np.sqrt(-mean_score), params)
    # 特征重要性
    feature_importances = grid_search.best_estimator_.feature_importances_
    # print(feature_importances)
    print(' * feature importances: \n')
    pprint.pprint(sorted(zip(feature_importances, column_list), reverse=True))

    # 模型
    final_model = grid_search.best_estimator_
    show_results(final_model,train_inputs,train_labels,title="Random Forest Regression")


def rf():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    # --------------------调参--------------------------------------------------------
    # 随机森林
    rfr   = RandomForestRegressor(random_state=37, n_estimators=300,
                                  min_weight_fraction_leaf=0.0,
                                  oob_score=True)
    # train
    rfr.fit(train_inputs, train_labels)
    score = rfr.score(train_inputs, train_labels)
    print(' * train set score: ',score)
    feature_importances = rfr.feature_importances_
    score = rfr.score(test_inputs, test_labels)
    print(' * test set score: ',score)

    print(' * feature importances: \n')
    # print(feature_importances)
    for i in range(len(column_list)-1):
        print(column_list[i],feature_importances[i])
    # pprint.pprint(sorted(zip(feature_importances, column_list), reverse=True))

    show_results(rfr,train_inputs,train_labels,title="Random Forest Regression (train set)")
    show_results(rfr,test_inputs,test_labels,title="Random Forest Regression (test set)")

def ada():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    adar = AdaBoostRegressor(DecisionTreeRegressor(max_depth=5),
                             n_estimators=500, random_state=37,
                             learning_rate=0.5)
    # train
    adar.fit(train_inputs, train_labels)
    feature_importances = adar.feature_importances_
    print(' * feature importances: \n')
    for i in range(len(column_list)-1):
        print(column_list[i],feature_importances[i])
    # pprint.pprint(sorted(zip(feature_importances, column_list), reverse=True))
    show_results(adar,train_inputs,train_labels,title="AdaBoosted Regression")
    show_results(adar,test_inputs,test_labels,title="AdaBoost Regression (test set)")


def gb():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    gbr = GradientBoostingRegressor(n_estimators=200, random_state=42)
    # train
    gbr.fit(train_inputs, train_labels)
    score = gbr.score(train_inputs, train_labels)
    print(' * train set score: ',score)
    score = gbr.score(test_inputs, test_labels)
    print(' * test set score: ',score)
    # print('feature importances:',gbr.feature_importances_)
    show_results(ada,train_inputs,train_labels,title="Gradient Boosting Regressor")


def sv():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    svr = SVR(kernel="rbf")
    # train
    svr.fit(train_inputs, train_labels)
    score = svr.score(train_inputs, train_labels)
    print(' * train set score: ',score)
    score = svr.score(test_inputs, test_labels)
    print(' * test set score: ',score)
    show_results(svr,train_inputs,train_labels,title="Support Vector Methine Regression")

def svgs():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    svr = GridSearchCV(SVR(kernel='rbf', gamma=0.1), cv=5,
                       param_grid={"C": [1e0, 1e1, 1e2, 1e3],
                               "gamma": np.logspace(-2, 2, 5)})
    svr.fit(train_inputs, train_labels)
    score = svr.score(train_inputs, train_labels)
    print(' * score: ',score)
    show_results(svr,train_inputs,train_labels,title="Support Vector Methine Regression")

def krgs():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    # param_grid = {"alpha": [1e0, 1e-1, 1e-2, 1e-3],
    #              "kernel": [ExpSineSquared(l, p)
    #                     for l in np.logspace(-2, 2, 10)
    #                     for p in np.logspace(0, 2, 10)]}
    # kr = GridSearchCV(KernelRidge(), param_grid=param_grid) 
    kr = GridSearchCV(KernelRidge(kernel='linear', gamma=0.1), cv=5,
                      param_grid={"alpha": [1e0, 0.1, 1e-2, 1e-3],
                                  "gamma": np.logspace(-2, 2, 5)})
    kr.fit(train_inputs,train_labels)
    print('best params: ',kr.best_params_)
    score = kr.score(train_inputs,train_labels)
    print(' * train set score: ',score)
    score = kr.score(test_inputs,test_labels)
    print(' * test set score: ',score)
    show_results(kr,train_inputs,train_labels,title="Kernel Ridge Regression")

def kr():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    kr = KernelRidge(kernel='linear',
                     alpha=0.01,gamma=0.01)
    kr.fit(train_inputs, train_labels)
    score = kr.score(train_inputs, train_labels)
    print(' * train set score: ',score)
    score = kr.score(test_inputs, test_labels)
    print(' * test set score: ',score)
    # print('feature importances:',kr.feature_importances_)
    show_results(kr,train_inputs,train_labels,title="Kernel Ridge Regression")


def knn():
    train_inputs,train_labels,test_inputs,test_labels,column_list = get_data_le()
    kr = KNeighborsRegressor(n_neighbors=2)
    kr.fit(train_inputs, train_labels)
    score = kr.score(train_inputs, train_labels)
    print(' * train set score: ',score)
    score = kr.score(test_inputs, test_labels)
    print(' * test set score: ',score)
    # print('feature importances:',kr.feature_importances_)
    show_results(kr,train_inputs,train_labels,title="K-Neighbors Regressor (train set)")
    show_results(kr,test_inputs,test_labels,title="K-Neighbors Regressor (test set)")


if __name__ == '__main__':
   ''' use commond like ./em-sklearn.py [rf,ada,sv,kr,xg,mlp,knn,gb] to run it'''
   parser = argparse.ArgumentParser()
   argh.add_commands(parser, [rf,ada,rfgs,sv,svgs,krgs,kr,xg,mlp,knn,gb])
   argh.dispatch(parser)


