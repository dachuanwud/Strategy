import numpy
import pandas as pd
import matplotlib as mpl
import time
import keras
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import matplotlib.pyplot as plt
from keras.models import load_model
from keras.callbacks import TensorBoard
from keras.utils import np_utils
from sklearn.model_selection import cross_val_predict
from sklearn import datasets, linear_model
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing
from sklearn import metrics
from keras.layers import Dense,Activation,Convolution2D,MaxPooling2D,Flatten,Reshape,Dropout

def mae(predictions, targets):
    return metrics.mean_absolute_error(targets, predictions)
def rmse(predictions, targets):
    return numpy.sqrt(((predictions - targets) ** 2).mean())

def test1(x):
    if x >= 0:
        x = 5
    if x < 0:
        x = -5
    return x

def get_data(df):
    #1. 数据处理
    df['下周期总涨跌幅'] = df['下周期每天涨跌幅'].apply(lambda x: sum(x))
    temp_df = df[['总市值', '换手率','换手率_5avg','换手率_20avg','中户买入占比_5avg','中户买入占比_20avg','散户卖出占比','散户卖出占比_5avg','散户卖出占比_20avg','rsi', '5日均线', 'bias', '5日累计涨跌幅', '申万一级行业名称',
             '归母ROE(ttm)', '归母EP(ttm)', '现金流负债比','总市值_分位数','归母ROE比120_分位数', 'BP_排名','存货周转率',
             '归母EP(ttm)_二级行业分位数','经营活动现金流入小计_分位数','10VWAP','成交额_排名','10日累计涨跌幅','120日累计涨跌幅','250日累计涨跌幅','下周期总涨跌幅']]

    temp_df["申万一级行业代码"] = pd.factorize(df["申万一级行业名称"])[0].astype(int)

    temp_df['涨跌幅分类'] = df['下周期总涨跌幅'].apply(lambda x: test1(x))
    temp_df.drop(['申万一级行业名称', '下周期总涨跌幅'], axis=1, inplace=True)
    # na值统一填充成-1
    temp_df.fillna(value=-1, inplace=True)
    temp_df.to_csv('/Users/lishechuan/python/coincock/data/模型数据/input.csv', index=False)
    time.sleep(10)
    tempdf = model()
    print(tempdf)
    return tempdf

def model():
    DataX = []
    DataY = []

    data_csv = pd.read_csv('/Users/lishechuan/python/coincock/data/模型数据/input.csv')
    y_csv1 = data_csv.values

    data_row = data_csv.shape[0]
    data_col = data_csv.shape[1]
    print(data_row, data_col)

    normalized_train_data = (y_csv1 - numpy.mean(y_csv1, axis=0)) / numpy.std(y_csv1, axis=0)
    Y = normalized_train_data[range(data_row)].reshape(data_row * data_col, )

    for xiaoli in range(0, data_row * data_col, data_col):
        xxx = Y[xiaoli: xiaoli + data_col - 1]
        yyy = Y[xiaoli + data_col - 1]
        DataX.append([char for char in xxx])
        DataY.append(yyy)
        print(xxx, '->', yyy)

    y1 = numpy.array(DataY).reshape(len(DataY), 1)

    #X_train, X_test, y_train, y_test = train_test_split(DataX, y1, random_state=0)
    X_train = numpy.reshape(DataX, (len(DataX), 1, data_col - 1, 1))
    y_train = DataY

    model = load_model('/Users/lishechuan/python/coincock/program/_财务数据选股策略_小组专用代码/data/cnn_model/my_model.h5_09_04')

    model.get_weights()
    print(model.get_weights())

    prediction = model.predict(X_train, verbose=0)
    prediction = prediction * numpy.std(y_csv1, axis=0)[data_col - 1] + numpy.mean(y_csv1, axis=0)[data_col - 1]

    temp_df = pd.DataFrame(prediction)
    def test2(x):
        if x >= 0:
            x = 5
        else:
            x = -5
        return x
    temp_df[0] = temp_df[0].apply(lambda x: test2(x))
    print(temp_df.tail(500))
    return temp_df








