#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import os
from sklearn.model_selection import StratifiedShuffleSplit
import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
from sklearn.linear_model import LinearRegression, Lasso, Ridge, BayesianRidge
from sklearn.metrics import mean_squared_error, r2_score, make_scorer
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.svm import SVR
from sklearn.kernel_ridge import KernelRidge
import xgboost as xgb
from sklearn.neighbors import KNeighborsRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import GridSearchCV, cross_validate
import pprint
import re


def save_fig(fig_id, tight_layout=True, fig_extension="png", resolution=300):
    path = os.path.join('./', fig_id + "." + fig_extension)
    print("Saving figure", fig_id)
    if tight_layout:
        plt.tight_layout()
    plt.savefig(path, format=fig_extension, dpi=resolution)


def scale_features(X, scale_factors=None):
    # 对输入数据进行缩放
    X = np.divide(X, scale_factors)
    # print(X.head())
    return X


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


def several_models(EMs_prepared, EMs_labels, models):
    # 尝试几种模型
    for model in models:
        if model == 'Linear':
            # 线性模型
            lin_reg = LinearRegression()
            fit_model_print_error(EMs_prepared, EMs_labels, model=lin_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=lin_reg)
        if model == 'DecisionTree':
            # decision tree 回归模型
            tree_reg = DecisionTreeRegressor(random_state=42)
            fit_model_print_error(EMs_prepared, EMs_labels, model=tree_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=tree_reg)
        if model == 'RandomForest':
            # 随机森林
            forest_reg = RandomForestRegressor(random_state=42)
            fit_model_print_error(EMs_prepared, EMs_labels, model=forest_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=forest_reg)
        if model == 'SVR':
            # SVR 支持向量机用于分类
            svm_reg = SVR(kernel="rbf")
            fit_model_print_error(EMs_prepared, EMs_labels, model=svm_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=svm_reg)
        if model == 'KernelRidge':
            # kernel ridge regression
            krr_reg = KernelRidge(kernel='rbf')
            fit_model_print_error(EMs_prepared, EMs_labels, model=krr_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=krr_reg)
        if model == 'xbg':
            # xgboost
            xgb_reg = xgb.XGBRegressor()
            fit_model_print_error(EMs_prepared, EMs_labels, model=xgb_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=xgb_reg)
        if model == 'KNeighbors':
            # KNN
            knn_reg = KNeighborsRegressor()
            fit_model_print_error(EMs_prepared, EMs_labels, model=knn_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=knn_reg)
        if model == 'Lasso':
            # Lasso
            lasso_reg = Lasso(max_iter=1500)
            fit_model_print_error(EMs_prepared, EMs_labels, model=lasso_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=lasso_reg)
        if model == 'Ridge':
            # Ridge
            ridge_reg = Ridge()
            fit_model_print_error(EMs_prepared, EMs_labels, model=ridge_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=ridge_reg)
        if model == 'polynomial':
            # Polynomial Regression
            poly_reg = Pipeline([('polynomial', PolynomialFeatures()), ('clf', LinearRegression())])
            fit_model_print_error(EMs_prepared, EMs_labels, model=poly_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=poly_reg)
        if model == 'BayesianRidge':
            # BayesianRidge
            bayes_reg = BayesianRidge(tol=1e-6, fit_intercept=False, compute_score=True)
            fit_model_print_error(EMs_prepared, EMs_labels, model=bayes_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=bayes_reg)
        if model == 'MLP':
            # Multi-layer Perceptron (MLP) 多层感知机
            MLP_reg = MLPRegressor((16, 16), max_iter=2000)
            fit_model_print_error(EMs_prepared, EMs_labels, model=MLP_reg)
            cross_val_fit_print_error(EMs_prepared, EMs_labels, model=MLP_reg)


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
    plt.title(fig_name, fontsize=20) # , fontproperties='SimHei'
    plt.xlabel('true')
    plt.ylabel('prediction')

    for index, value in enumerate(plt_data):
        plt.scatter(value[0], value[1],
                    label=plt_lable[index],
                    c=plt_c[index], alpha=0.6)
    # 简单理解就是：先写x的取值范围，再写y的取值范围
    plt.plot([edge_min, edge_max], [edge_min, edge_max], c='black', alpha=0.6)
    plt.legend()
    plt.savefig(fig_name)
    # plt.show()


def plot_out_scatter_residuals(plot_out_scatter_para, fig_name='pre_lable_residuals_scatter.png'):
    # 绘制残差图
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
    plt.title(fig_name, fontsize=20) # , fontproperties='SimHei'
    plt.xlabel('true')
    plt.ylabel('residual (prediction-true)')

    for index, value in enumerate(plt_data):
        plt.scatter(value[0], value[1]-value[0],
                    label=plt_lable[index],
                    c=plt_c[index], alpha=0.6)
    # 简单理解就是：先写x的取值范围，再写y的取值范围
    plt.plot([edge_min, edge_max], [0, 0], c='black', alpha=0.6)
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
    plt.title(fig_name, fontsize=20) # , fontproperties='SimHei'
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
    y_pred = np.array(y_pred)
    y = np.array(y_lables.values)

    # 百分制
    relative_error = ((y_pred - y)/y)*100
    error_results = y_lables.reset_index(name='y_lables')
    error_results['y_pred'] = y_pred
    error_results['residuals'] = y_pred - y
    error_results['relative error (%)'] = relative_error
    # print(results)
    return error_results


def write_error(error_results, filename='error.csv'):
    # 将误差写入文件
    path = os.getcwd()
    error_results.to_csv('{}/{}'.format(path,filename), index=False, header=True, encoding="utf_8_sig")


def standard_data(dataset_use):
    # 将表格里 '-' 及 '--' 改为 None  删除(**) 及 <
    for index, row in dataset_use.iteritems():  # index 列名
        for row_index, row_value in row.items():
            if row_value == '-':
                dataset_use[index][row_index] = np.nan
            elif row_value == '--':
                dataset_use[index][row_index] = np.nan
            elif isinstance(row_value, str):
                if '(' in row_value: dataset_use[index][row_index] = float(re.sub('\(.*?\)', '', row_value))
                if '<' in row_value: dataset_use[index][row_index] = float(re.sub('\<', '', row_value))
    return dataset_use


def get_datasets():
    # 获得训练和测试集
    excel_name = 'Parameters-v9-20201014-Train-LCY-data.xlsx'
    skiprows = 24  # skiprows=excel中column名称对应的行号-1

    # 获取表格数据
    EMs = get_data(excel_name, skiprows)
    # print(EMs.columns)

    # 合并含对勾的列为数字 并在EMs最后添加列
    # 合并Packing type
    column_list = ['Packing_type1', 'Packing_type2']
    EMs = merge_columns(EMs, column_list, column_name='Packing_type')
    # print(EMs.head())

    # 合并Molecular_backbone
    column_list = ['Molecular_backbone1', 'Molecular_backbone2', 'Molecular_backbone3', 'Molecular_backbone4']
    EMs = merge_columns(EMs, column_list, column_name='Molecular_backbone')
    # print(EMs.head())
    # print(EMs.columns)

    # 合并weakest bonds type
    column_list = ['C-C', 'O-C', 'N-N', 'N-C', 'O-N']
    EMs = merge_columns(EMs, column_list, column_name='weakest_bond_type')
    # print(EMs['weakest_bond_type'])
    # print(EMs.columns)


    # ############################################################
    # 所有可以输入的特征
    column_list = ['density', 'PC', 'densityN', 'OB',
                   'Nm', 'Number', 'Crystal_family', 'Packing_type',
                   'mixed_molecule1', 'mixed_molecule2',
                   'HB_amount', 'strongest_HB_length', 'strongest_HB_strength',
                   'MW', 'Molecular_backbone',
                   'FG_NO2', 'FG_N3', 'FG_NH2', 'FG_OH', 'FG_CH3',
                   'weakest_bond_type', 'Length ', '1st_weakest_bond_strength',
                   'LE']
    column_list_inputs = ['density', 'PC', 'densityN', 'OB',
                          'Nm', 'Number', 'Crystal_family', 'Packing_type',
                          'mixed_molecule1', 'mixed_molecule2',
                          'HB_amount', 'strongest_HB_length', 'strongest_HB_strength',
                          'MW', 'Molecular_backbone',
                          'FG_NO2', 'FG_N3', 'FG_NH2', 'FG_OH', 'FG_CH3',
                          'weakest_bond_type', 'Length ', '1st_weakest_bond_strength']

    column_lables = 'LE'
    dataset_use = extrat_columns(EMs, column_list=column_list)
    # dataset_use.to_csv('data_927.csv')
    # # 使用corr()方法计算出每对属性间的标准相关系数（也称作皮尔逊相关系数）
    # corr_matrix = dataset_use.corr()
    # # print(corr_matrix)
    # corr_matrix.to_csv('corr_matrix.csv', index=True, header=True, encoding="utf_8_sig")

    # # 绘相关性图
    # import pandas as pd
    # import numpy as np
    # import matplotlib.pyplot as plt
    # import seaborn as sns
    # def correlation_heatmap(train):
    #     correlations = train.corr()
    #     fig, ax = plt.subplots(figsize=(10, 10))
    #     sns.heatmap(correlations, vmax=1.0, center=0, fmt='.2f',
    #                 square=True, linewidths=.5, annot=True, cbar_kws={"shrink": .70})
    #     plt.show()
    # correlation_heatmap(dataset_use)

    # 创建测试集
    # 随机采样
    # strat_train_set, strat_test_set = train_test_split(dataset_use, test_size=0.2, random_state=42)
    # ***********分层采样
    # 新添加一列 编号分层
    # 'OB' [-140, -100, -50, 0, 50]
    # "density", [0., 1.7, 1.8, 1.9, np.inf]
    # "DT"   [120, 200, 280, 350, 410]
    # "1st_weakest_bond_strength"   [60., 100., 150., 200.]
    # 'MW' [60, 300, 500, 700, 900]
    # 'LE' [0., 50., 100., 150., 200.]  [0., 25., 40., 60., 200.]
    print(min(dataset_use['strongest_HB_strength']), max(dataset_use['strongest_HB_strength']))
    # dataset_use["density_cat"] = pd.cut(dataset_use['OB'], bins=[-140, -100, -50, 0, 50], labels=[1, 2, 3, 4])
    # dataset_use["density_cat"] = pd.cut(dataset_use["LE"], bins=[0., 20., 40., 60.], labels=[1, 2, 3])
    dataset_use["density_cat"] = pd.cut(dataset_use["density"], bins=[0., 1.7, 1.8, 1.9, np.inf], labels=[1, 2, 3, 4])
    # dataset_use["density_cat"] = pd.cut(dataset_use["strongest_HB_strength"], bins=[-0.1, 10., 20., 30., 40.0], labels=[1, 2, 3, 4])
    # dataset_use["density_cat"] = pd.cut(dataset_use["MW"], bins=[60, 300, 500, 700, 900], labels=[1, 2, 3, 4])
    # dataset_use["density_cat"] = pd.cut(dataset_use["1st_weakest_bond_strength"], bins=[0., 60., 100., 200., np.inf], labels=[1, 2, 3, 4])

    # print(dataset_use.head())
    split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)
    for train_index, test_index in split.split(dataset_use, dataset_use["density_cat"]):
        strat_train_set = dataset_use.iloc[train_index]
        strat_test_set = dataset_use.iloc[test_index]
    # print(dataset_use["density_cat"].value_counts() / len(dataset_use))
    # print(strat_test_set["density_cat"].value_counts() / len(strat_test_set))
    # print(strat_train_set.shape, strat_test_set.shape)
    # 删除income_cat属性，使数据回到初始状态
    for set in (strat_train_set, strat_test_set):
        set.drop(["density_cat"], axis=1, inplace=True)
    # print(strat_test_set.head())
    # ***********分层采样
    print('train set number: {}, test set number: {}'.format(strat_train_set.shape, strat_test_set.shape))

    # # 绘图观察数据
    # fig = plt.figure(1)
    # x = list(range(len(dataset_use['DT'])))
    # plt.scatter(x, dataset_use['DT'], alpha=0.5, marker='o')
    # save_fig("DT_scatterplot")

    # 为机器学习准备数据
    all_inputs = dataset_use[column_list_inputs].copy()
    all_lables = dataset_use[column_lables].copy()
    train_inputs = strat_train_set.drop(column_lables, axis=1)  # 输入
    train_labels = strat_train_set[column_lables].copy()  # 输出
    X_test = strat_test_set.drop(column_lables, axis=1)
    y_test = strat_test_set[column_lables].copy()
    # print(train_labels.head())

    return all_inputs, all_lables, train_inputs, train_labels, X_test, y_test, column_list


def RandomForest_GridSearchCV():
    # 随机森林 调参
    _, _, train_inputs, train_labels, X_test, y_test, column_list = get_datasets()
    param_grid = {'n_estimators': [10],  # list(range(650,750,10))
                  'min_weight_fraction_leaf': [0],  # [0, 0.1, 0.3, 0.5]
                  'max_depth': [8]
                  }
    model_reg = RandomForestRegressor(random_state=37)  # oob_score=True
    # train  'scoring='neg_mean_squared_error' 或者 'r2'
    grid_search = GridSearchCV(model_reg, param_grid, cv=5,
                               scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(train_inputs, train_labels)
    print('best params: ', grid_search.best_params_)
    cvres = grid_search.cv_results_
    # 找出best_params_位置 在结果中的位置
    best_index = grid_search.best_index_
    # 最佳模型 neg_mean_squared_error 交叉验证的 mean_train_rmse mean_test_rmse
    mean_train_rmse = np.sqrt(-cvres["mean_train_score"][best_index])
    mean_test_rmse = np.sqrt(-cvres["mean_test_score"][best_index])
    print('- ' * 20, '\nbest model cross:\n',
          'mean train rmse: {:<.4f}, mean test r2: {:<.4f}'.format(mean_train_rmse, mean_test_rmse))
    # 以 r2为score
    # mean_train_r2 = cvres["mean_train_score"][best_index]
    # mean_test_r2 = cvres["mean_test_score"][best_index]
    # print('- ' * 20, '\nbest model cross:\n',
    #       'mean train r2: {:<.4f}, mean test r2: {:<.4f}'.format(mean_train_r2, mean_test_r2))

    # 每种参数的score
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #     print(np.sqrt(-mean_score), params)
    # 特征重要性
    feature_importances = grid_search.best_estimator_.feature_importances_
    # print(feature_importances)
    print('- ' * 20, '\n', 'feature importances:')
    feature_import = sorted(zip(feature_importances, column_list), reverse=True)
    pprint.pprint(feature_import)
    write_feature_import(feature_import)
    # 模型
    final_model = grid_search.best_estimator_
    return final_model


def AdaBoost_GridSearchCV():
    # AdaBoost 调参
    _, _, train_inputs, train_labels, X_test, y_test, column_list = get_datasets()
    param_grid = {'n_estimators': [30],  # list(range(130,140,1))
                  # 'learning_rate': [0.3, 0.6, 0.9, 1, 1.3, 1.6, 1.9],  # 0-1范围 前两个一起调 [0.001, 0.01, 0.1, 1, 10]
                  'loss' : ['linear', 'square'],  # ['linear', 'square', 'exponential']
                  'random_state': [42]
                  }

    model_reg = AdaBoostRegressor(DecisionTreeRegressor(max_depth=4))
    # train  'scoring='neg_mean_squared_error' 或者 'r2'
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
    print('- ' * 20, '\nbest model cross:\n',
          'mean train rmse: {:<.4f}, mean test rmse: {:<.4f}'.format(mean_train_rmse, mean_test_rmse))
    # 以 r2为score
    # mean_train_r2 = cvres["mean_train_score"][best_index]
    # mean_test_r2 = cvres["mean_test_score"][best_index]
    # print('- ' * 20, '\nbest model cross:\n',
    #       'mean train r2: {:<.4f}, mean test r2: {:<.4f}'.format(mean_train_r2, mean_test_r2))

    # 每种参数的score
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #     print(np.sqrt(-mean_score), params)
    # 特征重要性
    feature_importances = grid_search.best_estimator_.feature_importances_
    # print(feature_importances)
    print('- ' * 20, '\n', 'feature importances:')
    feature_import = sorted(zip(feature_importances, column_list), reverse=True)
    # pprint.pprint(feature_import)
    write_feature_import(feature_import)

    # 模型
    final_model = grid_search.best_estimator_
    return final_model


def XGBoost_GridSearchCV():
    # XGBoost 调参
    _, _, train_inputs, train_labels, X_test, y_test, column_list = get_datasets()
    # xgr = xgb.XGBRegressor(reg_lambda=3, max_depth=6)
    # param_grid = {'reg_lambda': 3, 'max_depth': 6}
    param_grid = {'n_estimators': [20],  # list(range(100,600,100))
                  'max_depth': [3],  # list(range(3,10,2))
                  'min_child_weight': [1],  # list(range(1,6,2))  1.先调前三个
                  'gamma': [0],  # 2. 调gamma
                  # 'subsample': [0.5, 0.6, 0.7, 0.8, 0.9],  # [0.5, 0.6, 0.7, 0.8, 0.9]
                  # 'colsample_bytree': [0.5, 0.6, 0.7, 0.8, 0.9],  # 3. 调 sub和col
                  # 'reg_alpha': [1.8],  # [0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5]
                  # 'reg_lambda': [3],
                  # 'learning_rate': [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11],  # [0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11]
                  'booster': ['dart'],
                  }  #
    model_reg = xgb.XGBRegressor()  # booster='gbtree'
    # train  'scoring='neg_mean_squared_error' 或者 'r2'
    grid_search = GridSearchCV(model_reg, param_grid, cv=5,
                               scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(train_inputs, train_labels)
    print('best params: ', grid_search.best_params_)
    cvres = grid_search.cv_results_
    # 找出best_params_位置 在结果中的位置
    best_index = grid_search.best_index_

    # 每种参数的score
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #     print(np.sqrt(-mean_score), params)
    # 特征重要性
    feature_importances = grid_search.best_estimator_.feature_importances_
    # print(feature_importances)
    print('- ' * 20, '\n', 'feature importances:')
    feature_import = sorted(zip(feature_importances, column_list), reverse=True)
    pprint.pprint(feature_import)
    write_feature_import(feature_import)
    # 最佳模型 neg_mean_squared_error 交叉验证的 mean_train_rmse mean_test_rmse
    mean_train_rmse = np.sqrt(-cvres["mean_train_score"][best_index])
    mean_test_rmse = np.sqrt(-cvres["mean_test_score"][best_index])
    print('- ' * 20, '\nbest model cross:\n',
          'mean train rmse: {:<.4f}, mean test rmse: {:<.4f}'.format(mean_train_rmse, mean_test_rmse))

    # 以 r2为score
    # mean_train_r2 = cvres["mean_train_score"][best_index]
    # mean_test_r2 = cvres["mean_test_score"][best_index]
    # print('- ' * 20, '\nbest model cross:\n',
    #       'mean train r2: {:<.4f}, mean test r2: {:<.4f}'.format(mean_train_r2, mean_test_r2))
    # 模型
    final_model = grid_search.best_estimator_
    return final_model


def write_feature_import(feature_import):
    # 将特征重要性写入文件
    write_file = os.getcwd() + '/features_import.txt'
    with open(write_file, 'w') as fw:
        for feature in feature_import:
            fw.write('{},{}\n'.format(feature[1], feature[0]))


def mlp_GridSearchCV():
    # mlp 调参
    _, _, train_inputs, train_labels, X_test, y_test, column_list = get_datasets()
    param_grid = {
                  #'alpha': [0.01],
                  'hidden_layer_sizes': [(3,3)],
                  'activation': ['relu'],
                  'solver': ['adam'],
                  'random_state': [23]
                  }
    model_reg = MLPRegressor(max_iter=10000)
    # train  'scoring='neg_mean_squared_error' 或者 'r2'
    grid_search = GridSearchCV(model_reg, param_grid, cv=5,
                               scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(train_inputs, train_labels)
    print('best params: ', grid_search.best_params_)
    cvres = grid_search.cv_results_
    # 找出best_params_位置 在结果中的位置
    best_index = grid_search.best_index_
    # 最佳模型 neg_mean_squared_error 交叉验证的 mean_train_rmse mean_test_rmse
    mean_train_rmse = np.sqrt(-cvres["mean_train_score"][best_index])
    mean_test_rmse = np.sqrt(-cvres["mean_test_score"][best_index])
    print('- ' * 20, '\nbest model cross:\n',
          'mean train rmse: {:<.4f}, mean test rmse: {:<.4f}'.format(mean_train_rmse, mean_test_rmse))
    # 以 r2为score
    # mean_train_r2 = cvres["mean_train_score"][best_index]
    # mean_test_r2 = cvres["mean_test_score"][best_index]
    # print('- ' * 20, '\nbest model cross:\n',
    #       'mean train r2: {:<.4f}, mean test r2: {:<.4f}'.format(mean_train_r2, mean_test_r2))

    # 每种参数的score
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #     print(np.sqrt(-mean_score), params)
    # 特征重要性
    # feature_importances = grid_search.best_estimator_.feature_importances_
    # # print(feature_importances)
    # print('- ' * 20, '\n', 'feature importances:')
    # pprint.pprint(sorted(zip(feature_importances, column_list), reverse=True))

    # 模型
    final_model = grid_search.best_estimator_
    return final_model


def krr_GridSearchCV():
    # mlp 调参
    _, _, train_inputs, train_labels, X_test, y_test, column_list = get_datasets()
    param_grid = {# "alpha": [0],  # [1e0, 0.1, 1e-2, 1e-3]
                  "gamma": [0.01],
                  'kernel': ['polynomial', 'linear'],
                  'degree': [1, 2, 3]
                  }
    model_reg = KernelRidge()
    # train  'scoring='neg_mean_squared_error' 或者 'r2'
    grid_search = GridSearchCV(model_reg, param_grid, cv=5,
                               scoring='neg_mean_squared_error', return_train_score=True)
    grid_search.fit(train_inputs, train_labels)
    print('best params: ', grid_search.best_params_)
    cvres = grid_search.cv_results_
    # 找出best_params_位置 在结果中的位置
    best_index = grid_search.best_index_
    # # 最佳模型 neg_mean_squared_error 交叉验证的 mean_train_rmse mean_test_rmse
    mean_train_rmse = np.sqrt(-cvres["mean_train_score"][best_index])
    mean_test_rmse = np.sqrt(-cvres["mean_test_score"][best_index])
    print('- ' * 20, '\nbest model cross:\n',
          'mean train rmse: {:<.4f}, mean test rmse: {:<.4f}'.format(mean_train_rmse, mean_test_rmse))
    # 以 r2为score
    # mean_train_r2 = cvres["mean_train_score"][best_index]
    # mean_test_r2 = cvres["mean_test_score"][best_index]
    # print('- ' * 20, '\nbest model cross:\n',
    #       'mean train r2: {:<.4f}, mean test r2: {:<.4f}'.format(mean_train_r2, mean_test_r2))

    # 每种参数的score
    # for mean_score, params in zip(cvres["mean_test_score"], cvres["params"]):
    #     print(np.sqrt(-mean_score), params)
    # 特征重要性
    # feature_importances = grid_search.best_estimator_.feature_importances_
    # # print(feature_importances)
    # print('- ' * 20, '\n', 'feature importances:')
    # pprint.pprint(sorted(zip(feature_importances, column_list), reverse=True))

    # 模型
    final_model = grid_search.best_estimator_
    return final_model


def normfun(x, mu, sigma):
    pdf = np.exp(-((x - mu) ** 2) / (2 * sigma ** 2)) / (sigma * np.sqrt(2 * np.pi))
    return pdf


def plot_bar_curve(all_error_results, final_model):
    # 正态分布的概率密度函数
    # x      数据集中的某一具体测量值
    # mu     数据集的平均值，反映测量值分布的集中趋势
    # sigma  数据集的标准差，反映测量值分布的分散程度
    residuals = all_error_results['residuals']
    # print(residuals)
    mean = residuals.mean()
    std = residuals.std()
    minv = residuals.min()
    maxv = residuals.max()
    x = np.arange(minv, maxv, 0.1)
    # 设定Y轴，载入刚才定义的正态分布函数
    y = normfun(x, mean, std)
    # 绘制数据集的正态分布曲线
    plt.figure()
    plt.plot(x, y)
    # 绘制数据集的直方图
    probability, bin_residuals, _ = plt.hist(residuals, bins=30, rwidth=0.9, density=True)

    plt.title('residuals distribution\n{}'.format(type(final_model)))
    plt.xlabel('residuals')
    plt.ylabel('Probability')
    # plt.tight_layout()
    plt.savefig('ferq.png')

    # 将数据写入excel
    bin_residuals_m = []
    for bi in range(len(bin_residuals)-1):
        bin_residuals_m.append((bin_residuals[bi]+bin_residuals[bi+1])/2)
    data_pdf = {'pdf_x': x, 'pdf_y': y}
    data_residual = {'bin_residuals': bin_residuals_m, 'probability': probability}
    # print(len(probability), len(bin_residuals_m))

    data_pdf = pd.DataFrame(data_pdf)
    data_residual = pd.DataFrame(data_residual)
    data_pdf.to_csv('data_pdf.csv', index=False)
    data_residual.to_csv('data_residual.csv', index=False)


def results(final_model):
    # 由得到的模型 获得训练及测试的结果
    all_inputs, all_lables, train_inputs, train_labels, X_test, y_test, column_list = get_datasets()
    # # 交叉验证训练集结果
    scoring = {'r2': 'r2', 'nmse': 'neg_mean_squared_error', 'r': make_scorer(my_custom_score_func)}
    cross_score = cross_validate(final_model, train_inputs, train_labels, scoring=scoring,
                                 return_train_score=True, n_jobs=-1, verbose=0)
    # r
    cross_train_r = np.mean(cross_score['train_r'])
    cross_train_r_std = np.std(cross_score['train_r'])
    cross_test_r = np.mean(cross_score['test_r'])
    cross_test_r_std = np.std(cross_score['test_r'])
    # R2
    cross_train_r2 = np.mean(cross_score['train_r2'])
    cross_train_r2_std = np.std(cross_score['train_r2'])
    cross_test_r2 = np.mean(cross_score['test_r2'])
    cross_test_r2_std = np.std(cross_score['test_r2'])
    # rmse
    cross_train_rmse = np.mean(np.sqrt(-cross_score['train_nmse']))
    cross_train_rmse_std = np.std(np.sqrt(-cross_score['train_nmse']))
    cross_test_rmse = np.mean(np.sqrt(-cross_score['test_nmse']))
    cross_test_rmse_std = np.std(np.sqrt(-cross_score['test_nmse']))
    # print('cross train rmse: {}±{}, cross test rmse {}±{}'.format(cross_train_rmse, cross_train_rmse_std,
    #                                                               cross_test_rmse, cross_test_rmse_std))

    # pprint.pprint(cross_score)
    # 所有数据结果
    all_predictions = final_model.predict(all_inputs)

    # 训练集结果
    train_predictions = final_model.predict(train_inputs)
    train_mse = mean_squared_error(train_labels, train_predictions)
    train_rmse = np.sqrt(train_mse)
    train_r = correlation_coefficient(train_labels, train_predictions)
    train_R2 = r2_score(train_labels, train_predictions)

    # 测试集结果
    # print(y_test)
    test_predictions = final_model.predict(X_test)
    test_mse = mean_squared_error(y_test, test_predictions)
    test_rmse = np.sqrt(test_mse)
    print('- ' * 20, '\nbest model test:\n', 'train rmse: {:<.4f}, test rmse: {:<.4f}'.format(train_rmse, test_rmse))
    # 预测和真实值线性关系
    test_r = correlation_coefficient(y_test, test_predictions)
    test_R_square = r2_score(y_test, test_predictions)
    print('- ' * 20, '\n', ' train: r: {:<.4f} R square: {:<.4f}'.format(train_r, train_R2))
    print('- ' * 20, '\n', ' test: r: {:<.4f} R square: {:<.4f}'.format(test_r, test_R_square))
    # 绘图
    plot_out_scatter_para = {'data': [[train_labels, train_predictions], [y_test, test_predictions]],
                             'label': ['train: $R^2$={:.2f} r={:.2f}'.format(train_R2, train_r),
                                       ' test: $R^2$={:.2f} r={:.2f}'.format(test_R_square, test_r)],
                             'c': ['red', 'blue']}
    plot_out_scatter_para_residuals = {'data': [[train_labels, train_predictions], [y_test, test_predictions]],
                             'label': ['train: $R^2$={:.2f} r={:.2f}'.format(train_R2, train_r),
                                       ' test: $R^2$={:.2f} r={:.2f}'.format(test_R_square, test_r)],
                             'c': ['red', 'blue']}
    plot_out_scatter(plot_out_scatter_para, fig_name='pre_lable_scatter.png')
    plot_out_scatter_residuals(plot_out_scatter_para_residuals, fig_name='pre_lable_scatter_residuals.png')
    plot_output_errorbar(train_predictions, train_labels, fig_name='train_err.png')
    plot_output_errorbar(test_predictions, y_test, fig_name='test_err.png')

    # 计算 预测值和真实值相对误差 将误差写入文件
    all_error_results = get_relative_error(all_predictions, all_lables)
    # 绘制直方图和正态分布图
    plot_bar_curve(all_error_results, final_model)
    # print(all_error_results)
    # nbins = 30
    # minv = all_error_results['residuals'].min()
    # maxv = all_error_results['residuals'].max()
    # # maxv = -all_error_results['residuals'].min()
    # bins_list = [minv-1e-3]
    # for i in range(1, nbins): bins_list.append(minv+i*(maxv-minv)/nbins)
    # bins_list.append(maxv + 1e-3)
    # cats1 = pd.cut(all_error_results['residuals'].values, bins=bins_list)
    # freq = cats1.value_counts()
    # freq_df = pd.DataFrame(freq, columns=['freq_No'])
    # # freq_df['freq_1'] = freq_df / freq_df['freq_No'].sum()
    # print(freq_df)
    # freq_df.plot(kind='bar')
    # # plt.show()
    # plt.tight_layout()
    # plt.savefig('ferq.png')

    train_error_results = get_relative_error(train_predictions, train_labels)
    write_error(train_error_results, filename='train_error.csv')
    test_error_results = get_relative_error(test_predictions, y_test)
    write_error(test_error_results, filename='test_error.csv')
    scores = {'cross_train_rmse': cross_train_rmse,
              'cross_train_rmse_std': cross_train_rmse_std,
              'cross_test_rmse': cross_test_rmse,
              'cross_test_rmse_std': cross_test_rmse_std,
              'cross_train_r': cross_train_r,
              'cross_train_r_std': cross_train_r_std,
              'cross_train_r2': cross_train_r2,
              'cross_train_r2_std': cross_train_r2_std,
              'cross_test_r': cross_test_r,
              'cross_test_r_std': cross_test_r_std,
              'cross_test_r2': cross_test_r2,
              'cross_test_r2_std': cross_test_r2_std,
              'train_rmse': train_rmse,
              'train_r': train_r,
              'train_r2': train_R2,
              'test_rmse': test_rmse,
              'test_r': test_r,
              'test_r2': test_R_square
              }
    write_score(scores, final_model)


def write_score(scores, final_model):
    # 将score信息写入文件
    write_file = os.getcwd() + '/score.txt'
    with open(write_file, 'w') as fw:
        fw.write('the score of:\n{}\n'.format(final_model))
        fw.write('CV train rmse: {:.4f} ± {:.4f}\n'.format(scores['cross_train_rmse'], scores['cross_train_rmse_std']))
        fw.write('CV test rmse: {:.4f} ± {:.4f}\n'.format(scores['cross_test_rmse'], scores['cross_test_rmse_std']))
        fw.write('CV train r: {:.4f} ± {:.4f}\n'.format(scores['cross_train_r'], scores['cross_train_r_std']))
        fw.write('CV train R2: {:.4f} ± {:.4f}\n'.format(scores['cross_train_r2'], scores['cross_train_r2_std']))
        fw.write('CV test r: {:.4f} ± {:.4f}\n'.format(scores['cross_test_r'], scores['cross_test_r_std']))
        fw.write('CV test R2: {:.4f} ± {:.4f}\n'.format(scores['cross_test_r2'], scores['cross_test_r2_std']))
        fw.write('train rmse: {:.4f}\n'.format(scores['train_rmse']))
        fw.write('train r: {:.4f}\n'.format(scores['train_r']))
        fw.write('train R2: {:.4f}\n'.format(scores['train_r2']))
        fw.write('test rmse: {:.4f}\n'.format(scores['test_rmse']))
        fw.write('test r: {:.4f}\n'.format(scores['test_r']))
        fw.write('test R2: {:.4f}\n'.format(scores['test_r2']))


if __name__ == '__main__':
    # XGBoost_GridSearchCV
    # AdaBoost_GridSearchCV
    # RandomForest_GridSearchCV
    # mlp_GridSearchCV
    # krr_GridSearchCV
    final_model = XGBoost_GridSearchCV()
    # print('-------------getting results...---------------------')
    results(final_model)
    # train_inputs, train_labels, X_test, y_test, column_list = get_datasets()
























































