"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

财务数据选股专属代码

数据整理需要计算的因子脚本，可以在这里修改/添加别的因子计算
"""


# !!!
import pandas as pd
import talib as ta
import math

def price_bottom(df, para, window_v, extra_agg_dict):
    # 1.寻找第1个金叉，5 穿 10
    short = '均线_' + para[0]
    mid = '均线_' + para[1]
    long = '均线_' + para[2]
    window = window_v
    len = df.shape[0]

    # extra_agg_dict['signal_a'] = 'last'
    # extra_agg_dict['signal_b'] = 'last'
    # extra_agg_dict['signal_c'] = 'last'
    extra_agg_dict['price_bottom'] = 'sum'

    df['signal_a'] = 0
    df['signal_b'] = 0
    df['signal_c'] = 0
    df['price_bottom'] = 0
    df['test_a'] = 0
    df['test_b'] = 0
    df['test_c'] = 0

    condition1 = df[short] > df[mid]  # 短期均线 > 长期均线
    condition2 = df[short].shift(1) <= df[mid].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'signal_a'] = df.loc[condition1 & condition2, mid] # 将产生做多信号的那根K线的signal设置为1，1代表做多
    # 2.寻找第2个金叉，5 穿 20
    condition1 = df[short] > df[long]  # 短期均线 > 长期均线
    condition2 = df[short].shift(1) <= df[long].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'signal_b'] = df.loc[condition1 & condition2, long]  # 将产生做多信号的那根K线的signal设置为1，1代表做多
    # 3.寻找第3个金叉，10 穿 20
    condition1 = df[mid] > df[long]  # 短期均线 > 长期均线
    condition2 = df[mid].shift(1) <= df[long].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'signal_c'] = df.loc[condition1 & condition2, long]  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    for i in range(0, len, 1):
        a, b, c = -1, -1, -1
        if df.loc[i + df.index[0], 'signal_a'] != 0:
            # find a
            a = df.loc[i + df.index[0], 'signal_a']
            if (i + window) >= len:
                j_len = len
            else:
                j_len = i + window
            for j in range(i + 1, j_len, 1):
                # find b
                if df.loc[j + df.index[0], 'signal_b'] != 0:
                    b = df.loc[j + df.index[0], 'signal_b']
                    for k in range(j + 1, j_len, 1):
                        # find c
                        if df.loc[k + df.index[0], 'signal_c'] != 0:
                            c = df.loc[k + df.index[0], 'signal_c']
                            # 判断是不是价托 a,b,c有值，且 b > a
                            if a != -1 and b != -1 and c != -1 and b > a:
                                df.loc[k + df.index[0], 'price_bottom'] = 1
                                df.loc[k + df.index[0], 'test_a'] = a
                                df.loc[k + df.index[0], 'test_b'] = b
                                df.loc[k + df.index[0], 'test_c'] = c
                                a, b, c = -1, -1, -1

    return df

# 计算量托
def vol_bottom(df, para, window_v, extra_agg_dict):
    # 1.寻找第1个金叉，5 穿 10
    short = '成交额_' + para[0]
    mid = '成交额_' + para[1]
    long = '成交额_' + para[2]
    window = window_v
    len = df.shape[0]

    # extra_agg_dict['vol_a'] = 'last'
    # extra_agg_dict['vol_b'] = 'last'
    # extra_agg_dict['vol_c'] = 'last'
    extra_agg_dict['vol_bottom'] = 'sum'

    df['vol_a'] = 0
    df['vol_b'] = 0
    df['vol_c'] = 0
    df['vol_bottom'] = 0
    df['test_a'] = 0
    df['test_b'] = 0
    df['test_c'] = 0

    condition1 = df[short] > df[mid]  # 短期均线 > 长期均线
    condition2 = df[short].shift(1) <= df[mid].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'vol_a'] = df.loc[condition1 & condition2, mid] # 将产生做多信号的那根K线的vol设置为1，1代表做多
    # 2.寻找第2个金叉，5 穿 20
    condition1 = df[short] > df[long]  # 短期均线 > 长期均线
    condition2 = df[short].shift(1) <= df[long].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'vol_b'] = df.loc[condition1 & condition2, long]  # 将产生做多信号的那根K线的vol设置为1，1代表做多
    # 3.寻找第3个金叉，10 穿 20
    condition1 = df[mid] > df[long]  # 短期均线 > 长期均线
    condition2 = df[mid].shift(1) <= df[long].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'vol_c'] = df.loc[condition1 & condition2, long]  # 将产生做多信号的那根K线的vol设置为1，1代表做多

    for i in range(0, len, 1):
        a, b, c = -1, -1, -1
        if df.loc[i + df.index[0], 'vol_a'] != 0:
            # find a
            a = df.loc[i + df.index[0], 'vol_a']
            if (i + window) >= len:
                j_len = len
            else:
                j_len = i + window
            for j in range(i + 1, j_len, 1):
                # find b
                if df.loc[j + df.index[0], 'vol_b'] != 0:
                    b = df.loc[j + df.index[0], 'vol_b']
                    for k in range(j + 1, j_len, 1):
                        # find c
                        if df.loc[k + df.index[0], 'vol_c'] != 0:
                            c = df.loc[k + df.index[0], 'vol_c']
                            # 判断是不是价托 a,b,c有值，且 b > a
                            if a != -1 and b != -1 and c != -1 and b > a:
                                df.loc[k + df.index[0], 'vol_bottom'] = 1
                                a, b, c = -1, -1, -1

    return df

def cal_tech_factor(df, extra_agg_dict):
    """
    计算量价因子
    :param df:
    :param extra_agg_dict:
    :return:
    """

    extra_agg_dict['周期最后交易日'] = 'last'
    extra_agg_dict['股票代码'] = 'last'
    extra_agg_dict['股票名称'] = 'last'
    extra_agg_dict['是否交易'] = 'last'
    extra_agg_dict['开盘价'] = 'first'
    extra_agg_dict['最高价'] = 'max'
    extra_agg_dict['最低价'] = 'min'
    extra_agg_dict['收盘价'] = 'last'
    extra_agg_dict['前收盘价'] = 'last'
    extra_agg_dict['成交额'] = 'sum'
    extra_agg_dict['成交量'] = 'sum'

    # lsc 新加
    extra_agg_dict['收盘价_复权'] = 'last'

    #         # 因子列
    extra_agg_dict['总市值'] = 'last'
    extra_agg_dict['流通市值'] = 'last'
    extra_agg_dict['换手率'] = 'last'
    extra_agg_dict['量稳换手率变化率'] = 'last'
    extra_agg_dict['Illiquidity'] = 'last'
    extra_agg_dict['Illiquidity2'] = 'last'
    extra_agg_dict['L97'] = 'last'

    extra_agg_dict['DIF'] = 'last'
    extra_agg_dict['DEA'] = 'last'
    extra_agg_dict['MACD'] = 'last'
    extra_agg_dict['MACD_Hist'] = 'last'
    extra_agg_dict['RSV'] = 'last'
    extra_agg_dict['K'] = 'last'
    extra_agg_dict['D'] = 'last'
    extra_agg_dict['J'] = 'last'
    # extra_agg_dict['event_资金流'] = 'last'
    extra_agg_dict['中户资金净流入'] = 'last'
    extra_agg_dict['大户资金净流入'] = 'last'
    extra_agg_dict['散户资金净流入'] = 'last'
    extra_agg_dict['机构资金净流入'] = 'last'
    extra_agg_dict['mid_cash_ma3'] = 'last'
    extra_agg_dict['mid_cash_ma5'] = 'last'
    extra_agg_dict['mid_cash_ma10'] = 'last'
    extra_agg_dict['mid_cash_ma20'] = 'last'
    extra_agg_dict['big_cash_ma3'] = 'last'
    extra_agg_dict['big_cash_ma5'] = 'last'
    extra_agg_dict['big_cash_ma10'] = 'last'
    extra_agg_dict['big_cash_ma20'] = 'last'
    extra_agg_dict['small_cash_ma3'] = 'last'
    extra_agg_dict['small_cash_ma5'] = 'last'
    extra_agg_dict['small_cash_ma10'] = 'last'
    extra_agg_dict['small_cash_ma20'] = 'last'
    extra_agg_dict['super_cash_ma5'] = 'last'
    extra_agg_dict['super_cash_ma10'] = 'last'
    extra_agg_dict['cro_w'] = 'last'
    extra_agg_dict['cro_m'] = 'last'
    extra_agg_dict['cro_2m'] = 'last'
    extra_agg_dict['cro_3m'] = 'last'
    extra_agg_dict['cro_2w'] = 'last'
    extra_agg_dict['cro_3w'] = 'last'
    extra_agg_dict['上影线'] = 'last'
    extra_agg_dict['中户资金买入占比'] = 'last'
    extra_agg_dict['散户资金卖出占比'] = 'last'
    extra_agg_dict['大户资金买入占比'] = 'last'

    # # 计算必须额外数据
    # period_df['交易天数'] = df['是否交易'].resample(period_type).sum()
    # period_df['市场交易天数'] = df['股票代码'].resample(period_type).size()
    # # 月涨跌幅等于每天的涨跌幅的累乘，不能用（最后一天-第一天）/第一天
    # period_df['周期涨跌幅'] = df['涨跌幅'].resample(period_type).apply(lambda x: (x + 1.0).prod() - 1.0)
    # period_df = period_df[period_df['市场交易天数'] > 0]  # 有的时候整个周期不交易（例如春节、国庆假期），需要将这一周期删除
    # # 计算周期资金曲线
    # period_df['每天涨跌幅'] = df['涨跌幅'].resample(period_type).apply(lambda x: list(x))  # 是一个list，每天的涨跌幅
    # # 重新设定index
    # period_df.reset_index(inplace=True)
    # period_df['交易日期'] = period_df['周期最后交易日']
    # del period_df['周期最后交易日']
    #
    # return period_df
    # =计算下个交易的相关情况
    df['下日_是否交易'] = df['是否交易'].shift(-1)
    extra_agg_dict['下日_是否交易'] = 'last'

    df['下日_开盘涨停'] = df['开盘涨停'].shift(-1)
    extra_agg_dict['下日_开盘涨停'] = 'last'

    df['下日_是否ST'] = df['股票名称'].astype(str).str.contains('ST').shift(-1)
    extra_agg_dict['下日_是否ST'] = 'last'

    df['下日_是否退市'] = df['股票名称'].astype(str).str.contains('退').shift(-1)
    extra_agg_dict['下日_是否退市'] = 'last'

    df['下日_开盘买入涨跌幅'] = df['开盘买入涨跌幅'].shift(-1)
    extra_agg_dict['下日_开盘买入涨跌幅'] = 'last'

    df['下日_开盘跌停'] = df['开盘跌停'].shift(-1)
    extra_agg_dict['下日_开盘跌停'] = 'last'

    df['下日_一字涨停'] = df['一字涨停'].shift(-1)
    extra_agg_dict['下日_一字涨停'] = 'last'

    df['下日_开盘跌停'] = df['开盘跌停'].shift(-1)
    extra_agg_dict['下日_开盘跌停'] = 'last'

    # =计算均价
    df['VWAP'] = df['成交额'] / df['成交量']
    extra_agg_dict['VWAP'] = 'last'

    df['5VWAP'] = df['VWAP'].rolling(5).mean()
    extra_agg_dict['5VWAP'] = 'last'

    df['10VWAP'] = df['VWAP'].rolling(10).mean()
    extra_agg_dict['10VWAP'] = 'last'

    # # =计算换手率
    df['流通股本'] = df['流通市值'] / df['收盘价']
    df['换手率'] = df['成交量'] / df['流通股本']
    # df['换手率'] = df['成交额'] / df['流通市值']
    # extra_agg_dict['换手率'] = 'sum'
    #
    df['5日换手率'] = df['换手率'].rolling(5).mean()
    extra_agg_dict['5日换手率'] = 'last'

    df['10日换手率'] = df['换手率'].rolling(10).mean()
    extra_agg_dict['10日换手率'] = 'last'

    df['20日换手率'] = df['换手率'].rolling(20).mean()
    extra_agg_dict['20日换手率'] = 'last'

    # 计算均线_N:复权收盘价的N日均线，N可以取5，10，20。
    df['均线_5'] = df['收盘价_复权'].rolling(window=5).mean()
    extra_agg_dict['均线_5'] = 'last'

    df['均线_10'] = df['收盘价_复权'].rolling(window=10).mean()
    extra_agg_dict['均线_10'] = 'last'

    df['均线_20'] = df['收盘价_复权'].rolling(window=20).mean()
    extra_agg_dict['均线_20'] = 'last'

    df['均线_30'] = df['收盘价_复权'].rolling(window=30).mean()
    extra_agg_dict['均线_30'] = 'last'

    df['均线_31'] = df['收盘价_复权'].rolling(window=31).mean()
    extra_agg_dict['均线_31'] = 'last'

    df['均线_34'] = df['收盘价_复权'].rolling(window=34).mean()
    extra_agg_dict['均线_34'] = 'last'

    df['均线_40'] = df['收盘价_复权'].rolling(window=40).mean()

    df['均线_60'] = df['收盘价_复权'].rolling(60).mean()
    extra_agg_dict['均线_60'] = 'last'

    df['均线_120'] = df['收盘价_复权'].rolling(120).mean()
    extra_agg_dict['均线_120'] = 'last'

    df['均线_250'] = df['收盘价_复权'].rolling(250).mean()
    extra_agg_dict['均线_250'] = 'last'

    # 计算bias_N：当日复权收盘价相对于均线_N的涨跌幅，bias_N=(收盘价_复权/均线_N)-1，N可以取5，10，20。
    df['bias_5'] = (df['收盘价_复权'] - df['均线_5']) - 1
    extra_agg_dict['bias_5'] = 'last'

    df['bias_10'] = (df['收盘价_复权'] - df['均线_10']) - 1
    extra_agg_dict['bias_10'] = 'last'

    df['bias_20'] = (df['收盘价_复权'] - df['均线_20']) - 1
    extra_agg_dict['bias_20'] = 'last'

    df['bias_30'] = df['收盘价_复权'] / df['均线_30'] - 1
    extra_agg_dict['bias_30'] = 'last'

    df['bias_60'] = df['收盘价_复权'] / df['均线_60'] - 1
    extra_agg_dict['bias_60'] = 'last'

    df['bias_120'] = df['收盘价_复权'] / df['均线_120'] - 1
    extra_agg_dict['bias_120'] = 'last'

    # =计算价线率
    df['120日价线率'] = df['bias_120'].rolling(120).mean()
    extra_agg_dict['120日价线率'] = 'last'

    df['60日价线率'] = df['bias_60'].rolling(120).mean()
    extra_agg_dict['60日价线率'] = 'last'

    # =计算累计涨跌幅
    df['累计涨跌幅_5'] = df['收盘价_复权'].pct_change(5)
    extra_agg_dict['累计涨跌幅_5'] = 'last'

    df['5日累计涨跌幅20日标准差'] = df['累计涨跌幅_5'].rolling(20).std()
    extra_agg_dict['5日累计涨跌幅20日标准差'] = 'last'

    df['累计涨跌幅_10'] = df['收盘价_复权'].pct_change(10)
    extra_agg_dict['累计涨跌幅_10'] = 'last'

    df['10日累计涨跌幅20日标准差'] = df['累计涨跌幅_10'].rolling(20).std()
    extra_agg_dict['10日累计涨跌幅20日标准差'] = 'last'

    df['累计涨跌幅_20'] = df['收盘价_复权'].pct_change(20)
    extra_agg_dict['累计涨跌幅_20'] = 'last'

    df['20日累计涨跌幅20日标准差'] = df['累计涨跌幅_20'].rolling(20).std()
    extra_agg_dict['20日累计涨跌幅20日标准差'] = 'last'

    df['累计涨跌幅_30'] = df['收盘价_复权'].pct_change(30)
    extra_agg_dict['累计涨跌幅_30'] = 'last'

    df['30日累计涨跌幅20日标准差'] = df['累计涨跌幅_30'].rolling(20).std()
    extra_agg_dict['30日累计涨跌幅20日标准差'] = 'last'

    df['累计涨跌幅_50'] = df['收盘价_复权'].pct_change(50)
    extra_agg_dict['累计涨跌幅_50'] = 'last'

    df['累计涨跌幅_60'] = df['收盘价_复权'].pct_change(60)
    extra_agg_dict['累计涨跌幅_60'] = 'last'

    df['累计涨跌幅_120'] = df['收盘价_复权'].pct_change(120)
    extra_agg_dict['累计涨跌幅_120'] = 'last'

    df['累计涨跌幅_250'] = df['收盘价_复权'].pct_change(250)
    extra_agg_dict['累计涨跌幅_250'] = 'last'

    # 计算斜率
    df['MA34_斜率_5'] = df['均线_34'] / df['均线_34'].shift(5)
    df['MA34_斜率_5'] = df['MA34_斜率_5'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA34_斜率_5'] = 'last'

    df['MA34_斜率_10'] = df['均线_34'] / df['均线_34'].shift(10)
    df['MA34_斜率_10'] = df['MA34_斜率_10'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA34_斜率_10'] = 'last'

    df['MA34_斜率_20'] = df['均线_34'] / df['均线_34'].shift(20)
    df['MA34_斜率_20'] = df['MA34_斜率_20'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA34_斜率_20'] = 'last'

    df['MA5_斜率_5'] = df['均线_5'] / df['均线_5'].shift(5)
    df['MA5_斜率_5'] = df['MA5_斜率_5'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA5_斜率_5'] = 'last'

    df['MA5_斜率_10'] = df['均线_5'] / df['均线_5'].shift(10)
    df['MA5_斜率_10'] = df['MA5_斜率_10'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA5_斜率_10'] = 'last'

    df['MA5_斜率_20'] = df['均线_5'] / df['均线_5'].shift(20)
    df['MA5_斜率_20'] = df['MA5_斜率_20'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA5_斜率_20'] = 'last'

    df['MA60_斜率_5'] = df['均线_60'] / df['均线_60'].shift(5)
    df['MA60_斜率_5'] = df['MA60_斜率_5'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA60_斜率_5'] = 'last'

    df['MA60_斜率_10'] = df['均线_60'] / df['均线_60'].shift(10)
    df['MA60_斜率_10'] = df['MA60_斜率_10'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA60_斜率_10'] = 'last'

    df['MA60_斜率_20'] = df['均线_60'] / df['均线_60'].shift(20)
    df['MA60_斜率_20'] = df['MA60_斜率_20'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA60_斜率_20'] = 'last'

    df['MA250_斜率_5'] = df['均线_250'] / df['均线_250'].shift(5)
    df['MA250_斜率_5'] = df['MA250_斜率_5'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA250_斜率_5'] = 'last'

    df['MA250_斜率_10'] = df['均线_250'] / df['均线_250'].shift(10)
    df['MA250_斜率_10'] = df['MA250_斜率_10'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA250_斜率_10'] = 'last'

    df['MA250_斜率_20'] = df['均线_250'] / df['均线_250'].shift(20)
    df['MA250_斜率_20'] = df['MA250_斜率_20'].apply(lambda x: math.atan((x - 1) * 100) * 180 / 3.1415926)
    extra_agg_dict['MA250_斜率_20'] = 'last'



    # ===计算成交额均值
    df['成交额_5'] = df['成交额'].rolling(5).mean()
    extra_agg_dict['成交额_5'] = 'last'

    df['成交额_10'] = df['成交额'].rolling(10).mean()
    extra_agg_dict['成交额_10'] = 'last'

    df['成交额_20'] = df['成交额'].rolling(20).mean()
    extra_agg_dict['成交额_20'] = 'last'

    df['成交额_30'] = df['成交额'].rolling(30).mean()
    extra_agg_dict['成交额_30'] = 'last'

    df['成交额_60'] = df['成交额'].rolling(60).mean()
    extra_agg_dict['成交额_60'] = 'last'

    df['成交额_120'] = df['成交额'].rolling(120).mean()
    extra_agg_dict['成交额_120'] = 'last'

    # ===计算成交量均值
    df['成交量_5'] = df['成交量'].rolling(5).mean()
    extra_agg_dict['成交额_5'] = 'last'

    df['成交量_10'] = df['成交量'].rolling(10).mean()
    extra_agg_dict['成交量_10'] = 'last'

    df['成交量_20'] = df['成交量'].rolling(20).mean()
    extra_agg_dict['成交量_20'] = 'last'

    df['成交量_30'] = df['成交量'].rolling(30).mean()
    extra_agg_dict['成交量_30'] = 'last'

    df['成交量_60'] = df['成交量'].rolling(60).mean()
    extra_agg_dict['成交量_60'] = 'last'

    df['成交量_120'] = df['成交量'].rolling(120).mean()
    extra_agg_dict['成交量_120'] = 'last'

    # =计算累计涨跌幅
    df['5日累计涨跌幅'] = df['收盘价_复权'].pct_change(5)
    extra_agg_dict['5日累计涨跌幅'] = 'last'

    df['5日累计涨跌幅20日标准差'] = df['5日累计涨跌幅'].rolling(20).std()
    extra_agg_dict['5日累计涨跌幅20日标准差'] = 'last'

    df['10日累计涨跌幅'] = df['收盘价_复权'].pct_change(10)
    extra_agg_dict['10日累计涨跌幅'] = 'last'

    df['10日累计涨跌幅20日标准差'] = df['10日累计涨跌幅'].rolling(20).std()
    extra_agg_dict['10日累计涨跌幅20日标准差'] = 'last'

    df['20日累计涨跌幅'] = df['收盘价_复权'].pct_change(20)
    extra_agg_dict['20日累计涨跌幅'] = 'last'

    df['20日累计涨跌幅20日标准差'] = df['20日累计涨跌幅'].rolling(20).std()
    extra_agg_dict['20日累计涨跌幅20日标准差'] = 'last'

    df['30日累计涨跌幅'] = df['收盘价_复权'].pct_change(30)
    extra_agg_dict['30日累计涨跌幅'] = 'last'

    df['30日累计涨跌幅20日标准差'] = df['30日累计涨跌幅'].rolling(20).std()
    extra_agg_dict['30日累计涨跌幅20日标准差'] = 'last'

    df['50日累计涨跌幅'] = df['收盘价_复权'].pct_change(50)
    extra_agg_dict['50日累计涨跌幅'] = 'last'

    df['60日累计涨跌幅'] = df['收盘价_复权'].pct_change(60)
    extra_agg_dict['60日累计涨跌幅'] = 'last'

    df['120日累计涨跌幅'] = df['收盘价_复权'].pct_change(120)
    extra_agg_dict['120日累计涨跌幅'] = 'last'

    df['250日累计涨跌幅'] = df['收盘价_复权'].pct_change(250)
    extra_agg_dict['250日累计涨跌幅'] = 'last'

    # ===计算成交额标准差
    df['成交额std_3'] = df['成交额'].rolling(3, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_3'] = 'last'

    df['成交额std_5'] = df['成交额'].rolling(5, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_5'] = 'last'

    df['成交额std_10'] = df['成交额'].rolling(10, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_10'] = 'last'

    df['成交额std_20'] = df['成交额'].rolling(20, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_20'] = 'last'

    df['成交额std_30'] = df['成交额'].rolling(30, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_30'] = 'last'

    df['成交额std_60'] = df['成交额'].rolling(60, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_60'] = 'last'

    df['成交额std_120'] = df['成交额'].rolling(120, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_120'] = 'last'

    df['成交额std_250'] = df['成交额'].rolling(250, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额std_250'] = 'last'

    df['成交额_M50_std'] = df['成交额'].rolling(50, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额_M50_std'] = 'last'

    df['成交额_M60_std'] = df['成交额'].rolling(60, min_periods=1).std(ddof=0)
    extra_agg_dict['成交额_M60_std'] = 'last'
    # extra_agg_dict['总市值'] = 'last'
    # extra_agg_dict['成交额'] = 'sum'
    # extra_agg_dict['流通市值'] = 'last'
    df['复权因子'] = (df['收盘价'] / df['前收盘价']).cumprod()
    df['收盘价_复权'] = df['复权因子'] * (df.iloc[0]['收盘价'] / df.iloc[0]['复权因子'])
    df['开盘价_复权'] = df['开盘价'] / df['收盘价'] * df['收盘价_复权']
    df['最高价_复权'] = df['最高价'] / df['收盘价'] * df['收盘价_复权']
    df['最低价_复权'] = df['最低价'] / df['收盘价'] * df['收盘价_复权']


    # 差离值, 白线
    df['DIF'] = df['收盘价_复权'].ewm(alpha=2 / 13, adjust=False).mean() - df['收盘价_复权'].ewm(alpha=2 / 27,
                                                                                       adjust=False).mean()
    # 讯号线, 黄线
    df['DEA'] = df['DIF'].ewm(alpha=2 / 10, adjust=False).mean()
    df.loc[df['DIF'] / df['DEA'] > 1, '看涨'] = True
    df['MACD'] = 2 * (df['DIF'] - df['DEA'])
    df['MACD_Hist'] = abs(df['DEA'] - df['DIF'])
    df['L97'] = 2 * (df['DIF'] - df['DIF'].ewm(alpha=2 / 10, adjust=False).mean())
    # 计算N天最低价
    df['N_min'] = df['最低价_复权'].rolling(9, min_periods=9).min()
    df['N_min'].fillna(value=df['最低价_复权'].expanding().min(), inplace=True)
    # 计算N天最高价
    df['N_max'] = df['最高价_复权'].rolling(9, min_periods=9).min()
    df['N_max'].fillna(value=df['最高价_复权'].expanding().max(), inplace=True)
    # 计算RSV
    df['RSV'] = (df['收盘价_复权'] - df['N_min']) / (df['N_max'] - df['N_min']) * 100
    # 如果前边9天是NaN，填充为100
    df['RSV'].fillna(value=100, inplace=True)
    # 计算K、D、J的值
    df['K'] = df['RSV'].ewm(com=2, adjust=False).mean()
    df['D'] = df['K'].ewm(com=2, adjust=False).mean()
    df['J'] = 3 * df['K'] - 2 * df['D']
    # df = df[(df.中证500成分股 == 'Y')]
    # 删除上市的第一个周期
    df.drop([0], axis=0, inplace=True)  # 删除第一行数据
    # =计算涨跌幅
    df['涨跌幅'] = df['收盘价'] / df['前收盘价'] - 1
    df['周五涨跌幅'] = df['涨跌幅']
    extra_agg_dict['周五涨跌幅'] = 'last'  # 不买周五大涨的股票

    df['上影线'] = (df['最高价'] - df['收盘价']) / df['收盘价']
    df['涨跌幅_10'] = df['涨跌幅'].rolling(window=10).mean()
    df['涨跌幅_20'] = df['涨跌幅'].rolling(window=20).mean()
    df['开盘买入涨跌幅'] = df['收盘价'] / df['开盘价'] - 1  # 为之后开盘买入做好准备
    # 计算所需因子
    df['流通股本'] = df['流通市值'] / df['收盘价']
    df['换手率'] = df['成交量'] / df['流通股本']
    # df['量稳换手率变化率'] = df['换手率'].rolling(window=60).apply(lambda x: x[-20:].std() / x[:40].std() - 1)

    df['量稳换手率变化率'] = df['换手率'].rolling(window=60).apply(lambda x: x[-20:].std() / (x[:40].std()+float("1e-8")) - 1)


    df['量价相关性_10'] = df['收盘价_复权'].rolling(10).corr(df['换手率'])  # 求两列的相关性
    extra_agg_dict['量价相关性_10'] = 'last'

    df['量价相关性_30'] = df['收盘价_复权'].rolling(30).corr(df['换手率'])  # 求两列的相关性
    extra_agg_dict['量价相关性_30'] = 'last'

    df['量价相关性_60'] = df['收盘价_复权'].rolling(60).corr(df['换手率'])  # 求两列的相关性
    extra_agg_dict['量价相关性_60'] = 'last'

    df['Illiquidity'] = abs(df['涨跌幅_10']) / df['成交额_10'] * 100000000
    df['Illiquidity2'] = abs(df['涨跌幅_20']) / df['成交额_20'] * 100000000

    # 资金流筛选

    # 删除'中户资金买入额', '成交额'字段为空的行
    # df.dropna(subset=['中户资金买入额', '成交额', '散户资金卖出额', '总市值', '大户资金买入额', '收盘价', '开盘价', '前收盘价'], how='any', inplace=True, axis=0)

    # 中单
    df['中户资金净流入'] = df['中户资金买入额'] - df['中户资金卖出额']
    df['mid_cash_ma3'] = df['中户资金净流入'].rolling(3).mean()
    df['mid_cash_ma5'] = df['中户资金净流入'].rolling(5).mean()
    df['mid_cash_ma10'] = df['中户资金净流入'].rolling(10).mean()
    df['mid_cash_ma20'] = df['中户资金净流入'].rolling(20).mean()

    # 大单
    df['大户资金净流入'] = df['大户资金买入额'] - df['大户资金卖出额']
    df['big_cash_ma3'] = df['大户资金净流入'].rolling(3).mean()
    df['big_cash_ma5'] = df['大户资金净流入'].rolling(5).mean()
    df['big_cash_ma10'] = df['大户资金净流入'].rolling(10).mean()
    df['big_cash_ma20'] = df['大户资金净流入'].rolling(20).mean()

    # 小单
    df['散户资金净流入'] = df['散户资金买入额'] - df['散户资金卖出额']
    df['small_cash_ma3'] = df['散户资金净流入'].rolling(3).mean()
    df['small_cash_ma5'] = df['散户资金净流入'].rolling(5).mean()
    df['small_cash_ma10'] = df['散户资金净流入'].rolling(10).mean()
    df['small_cash_ma20'] = df['散户资金净流入'].rolling(20).mean()

    # 机构单
    df['机构资金净流入'] = df['机构资金买入额'] - df['机构资金卖出额']
    df['super_cash_ma5'] = df['机构资金净流入'].rolling(5).mean()
    df['super_cash_ma10'] = df['机构资金净流入'].rolling(10).mean()
    df['super_cash_ma20'] = df['机构资金净流入'].rolling(20).mean()

    # 资金占比
    df['中户资金买入额'] *= 10000
    df['散户资金卖出额'] *= 10000
    df['大户资金买入额'] *= 10000
    df['中户资金买入占比'] = df['中户资金买入额'] / df['成交额']  # 中户资金买入额占比
    df['散户资金卖出占比'] = df['散户资金卖出额'] / df['成交额']  # 散户资金卖入额占比
    df['大户资金买入占比'] = df['大户资金买入额'] / df['成交额']
    # 筛选事件
    # df['event_资金流'] = None
    # df.loc[(df['factor1'] >= 0.45) & (df['机构资金买入额'] > 0) &
    #        (df['factor2'] > 0.25) & (df['factor3'] > 0.4) & (df['收盘价'] > df['开盘价'] * 0.95), 'event_资金流'] = 1

    # =计算交易天数
    df['上市至今交易天数'] = df.index + 1
    df = df[df['上市至今交易天数'] > 120]

    df['cro_2w'] = df['涨跌幅'].rolling(10).corr(df['上市至今交易天数'])
    df['cro_3w'] = df['涨跌幅'].rolling(15).corr(df['上市至今交易天数'])
    df['cro_w'] = df['涨跌幅'].rolling(5).corr(df['上市至今交易天数'])
    df['cro_m'] = df['涨跌幅'].rolling(20).corr(df['上市至今交易天数'])
    df['cro_2m'] = df['涨跌幅'].rolling(40).corr(df['上市至今交易天数'])
    df['cro_3m'] = df['涨跌幅'].rolling(60).corr(df['上市至今交易天数'])

    # =将股票和上证指数合并，补全停牌的日期，新增数据"是否交易"、"指数涨跌幅"
    # df = merge_with_index_data(df, index_data)
    #
    # # =计算涨跌停价格
    # df = cal_if_zhangting_with_st(df)

    # 计算价托
    para = ['5', '10', '20']
    window = 5

    df = price_bottom(df, para, window, extra_agg_dict)
    df = vol_bottom(df, para, window, extra_agg_dict)
    # cal_rsi(df, 14, extra_agg_dict)
    # cal_obv(df, extra_agg_dict)

    # n_list = [5, 10, 20, 31, 60, 120, 250, ]
    # for n in n_list:
    #     # ===计算成交额标准差
    #     df['成交额std_%d' % n] = df['成交额'].rolling(n, min_periods=1).std(ddof=0)
    #
    #     # =计算累计涨跌幅
    #     df['累计涨跌幅_%s' % n] = df['收盘价_复权'].pct_change(n)
    #
    #     # ===计算涨跌幅标准差
    #     df['涨跌幅std_%s' % n] = df['涨跌幅'].rolling(n, min_periods=1).std()
    #
    #     # ===计算换手率均值
    #     df['换手率mean_%d' % n] = df['换手率'].rolling(n, min_periods=1).mean()
    #
    #     # ===计算5日与60日成交额
    #     df['成交额_%d' % n] = df['成交额'].rolling(n, min_periods=1).mean()
    #
    #     # ===计算振幅
    #     df['振幅_%d' % n] = df['最高价_复权'].rolling(n, min_periods=1).max() / df['最低价_复权'].rolling(n,min_periods=1).min()
    #
    #     # 计算换手
    #     df['换手率_%s_avg' % n] = df['换手率'].rolling(n).mean()
    #
    #     # =计算量价相关因子---新版本的pandas换写法了。https://bbs.quantclass.cn/thread/6821
    #     # df['量价相关系数_%d' % n] = df['复权因子'].rolling(n).corr(df['换手率'])
    #
    #     for i in ['成交额std_%d', '累计涨跌幅_%s', '涨跌幅std_%d',
    #               '换手率mean_%d', '成交额_%d', '振幅_%d', '换手率_%s_avg', ]:
    #         extra_agg_dict[i % n] = 'last'

    return df


def calc_fin_factor(df, extra_agg_dict):
    """
    计算财务因子
    :param df:              原始数据
    :param extra_agg_dict:  resample需要用到的
    :return:
    """

    # ====计算常规的财务指标
    # 计算归母PE
    # 归母PE = 总市值 / 归母净利润(ttm)
    df['归母PE(ttm)'] = df['总市值'] / df['R_np_atoopc@xbx_ttm']
    extra_agg_dict['归母PE(ttm)'] = 'last'

    df['归母EP(ttm)'] = 1 / df['归母PE(ttm)']
    extra_agg_dict['归母EP(ttm)'] = 'last'

    df['归母PE(ttm)比120'] = df['归母PE(ttm)'] / df['均线_120']
    extra_agg_dict['归母PE(ttm)比120'] = 'last'

    # 计算归母净利润率
    df['归母净利润率(ttm)'] = df['R_np_atoopc@xbx_ttm'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['归母净利润率(ttm)'] = 'last'

    # 计算归母ROE
    # 归母ROE(ttm) = 归母净利润(ttm) / 归属于母公司股东权益合计
    df['归母ROE(ttm)'] = df['R_np_atoopc@xbx_ttm'] / df['B_total_equity_atoopc@xbx']
    extra_agg_dict['归母ROE(ttm)'] = 'last'

    # 新增ROE历史平均
    df['ROE_AVG'] = df['归母ROE(ttm)'].rolling(600).mean()
    df['ROE_R'] = df['归母ROE(ttm)'] / df['ROE_AVG']
    extra_agg_dict['ROE_R'] = 'last'

    df['归母ROE比120'] = df['归母ROE(ttm)'] / df['均线_120']
    extra_agg_dict['归母ROE比120'] = 'last'

    # df['归母ROE比120'] = df['归母ROE(ttm)'] / df['120日均线']
    # extra_agg_dict['归母ROE比120'] = 'last'

    df['归母净利润单季环比'] = df['R_np_atoopc@xbx_单季环比']
    extra_agg_dict['归母净利润单季环比'] = 'last'

    # 计算毛利率ttm
    # 毛利率(ttm) = ( 营业总收入_ttm - 营业总成本_ttm ) / 营业总收入_ttm
    df['毛利率(ttm)'] = 1 - df['R_operating_total_cost@xbx_ttm'] / df['R_operating_total_revenue@xbx_ttm']
    extra_agg_dict['毛利率(ttm)'] = 'last'

    # 计算企业倍数指标
    """
    EV2 = 总市值+有息负债-货币资金, 
    EBITDA = 营业总收入-营业税金及附加-营业成本+利息支出+手续费及佣金支出+销售费用+管理费用+研发费用+坏账损失+存货跌价损失+固定资产折旧、油气资产折耗、生产性生物资产折旧+无形资产摊销+长期待摊费用摊销+其他收益
    """
    # 计算EBIT（息税前利润）=归母净利润+利息费用+所得税


    # 计算EBITDA
    # 坏账损失 字段无法直接从财报中获取，暂去除不计
    df['EBITDA'] = df[[
        # 营业总收入 负债应付利息 应付手续费及佣金
        'R_operating_total_revenue@xbx', 'B_interest_payable@xbx', 'B_charge_and_commi_payable@xbx',
        # 销售费用 管理费用 研发费用 资产减值损失
        'R_sales_fee@xbx', 'R_manage_fee@xbx', 'R_rad_cost_sum@xbx', 'R_asset_impairment_loss@xbx',
        # 固定资产折旧、油气资产折耗、生产性生物资产折旧 无形资产摊销 长期待摊费用摊销
        'C_depreciation_etc@xbx', 'C_intangible_assets_amortized@xbx', 'C_lt_deferred_expenses_amrtzt@xbx',
        # 其他综合利益 流动负债合计 非流动负债合计
        'R_other_compre_income@xbx', 'B_total_current_liab@xbx', 'B_total_noncurrent_liab@xbx'
    ]].sum(axis=1) - df[
                       # 税金及附加 营业成本
                       ['R_operating_taxes_and_surcharge@xbx', 'R_operating_cost@xbx']
                   ].sum(axis=1)

    df['有息负债'] = df[['B_st_borrow@xbx', 'B_lt_loan@xbx', 'B_bond_payable@xbx', 'B_noncurrent_liab_due_in1y@xbx']].sum(
        axis=1)

    df['EBIT'] = df['R_np_atoopc@xbx'] + df['R_interest_fee@xbx'] + df['R_income_tax_cost@xbx']

    # 计算EV(企业价值)= 总市值 + 其他权益工具 + 少数股东权益+ 带息负债
    df['EV'] = df['总市值'] + df['B_other_equity_instruments@xbx'].fillna(0) + df['B_minority_equity@xbx'] + df['有息负债']

    # 计算EY(股票收益率）= 息税前利润 / 企业价值
    df['EY'] = df['EBIT'] / df['EV']

    # 有息负债 = 短期借款 + 长期借款 + 应付债券 + 一年内到期的非流动负债


    # 计算EV2
    df['EV2'] = df['总市值'] + df['有息负债'] - df['B_currency_fund@xbx'].fillna(0)

    # 计算企业倍数
    df['企业倍数'] = df['EV2'] / df['EBITDA']
    extra_agg_dict['企业倍数'] = 'last'

    # ROC总资产收益率= 息税前利润 / （净营运资本 + 固定资产）
    #   净营运资本 = 应收账款 + 其他应收款* + 预付账款 + 存货 + 长期股权投资 + 投资性房地产 - 无息流动负债(应付账款 + 预收帐款 + 应付职工薪酬 + 应付税费 + 其他应付款* + (预提费用) + 递延收益流动负债 + 其他流动负债)
    df['净营运资本'] = df[['B_account_receivable@xbx',
                      'B_other_receivables@xbx',
                      'B_prepays@xbx', 'B_inventory@xbx',
                      'B_lt_equity_invest@xbx',
                      'B_invest_property@xbx'
                      ]].sum(axis=1) - df[['B_accounts_payable@xbx',
                                           'B_advance_payment@xbx',
                                           'B_payroll_payable@xbx',
                                           'B_tax_payable@xbx',
                                           'B_other_payables_sum@xbx',
                                           'B_differed_incomencl@xbx',
                                           'B_other_current_liab@xbx'
                                           ]].sum(axis=1)
    df['ROC'] = df['EY'] / (df['净营运资本'] + df['B_fixed_asset@xbx'])
    extra_agg_dict['ROC'] = 'last'

    # 计算现金流负债比
    # 现金流负债比 = 现金流量净额(经营活动) / 总负债(流动负债合计 + 非流动负债合计)
    df['现金流负债比'] = df['C_ncf_from_oa@xbx'] / (df['B_total_current_liab@xbx'] + df['B_total_noncurrent_liab@xbx'])
    extra_agg_dict['现金流负债比'] = 'last'

    #  #资产负债率
    df['净资产负债率'] = df['B_total_liab@xbx'] / df['B_total_equity_atoopc@xbx']
    extra_agg_dict['净资产负债率'] = 'last'

    df['资产负债率'] = df['总负债'] / df['总资产'] * 100
    extra_agg_dict['资产负债率'] = 'last'

    # =计算总负债比
    df['总负债比'] = df['总负债'] / df['总资产']
    extra_agg_dict['总负债比'] = 'last'

    #  现金流入值
    df['经营活动现金流入小计'] = df['C_sub_total_of_ci_from_oa@xbx']
    extra_agg_dict['经营活动现金流入小计'] = 'last'

    #  现金流出值
    df['经营活动现金流出小计'] = df['C_sub_total_of_cos_from_oa@xbx']
    extra_agg_dict['经营活动现金流出小计'] = 'last'

    df['经营活动现金流比率'] = df['C_sub_total_of_ci_from_oa@xbx'] / df['C_sub_total_of_cos_from_oa@xbx']
    extra_agg_dict['经营活动现金流比率'] = 'last'

    df['经营现金流量总负债比'] = df['C_ncf_from_oa@xbx'] / df['B_total_liab@xbx']
    extra_agg_dict['经营现金流量总负债比'] = 'last'

    #  计算流动比率
    #  流动比率 = 流动资产 / 流动负债
    df['流动比率'] = df['B_total_current_assets@xbx'] / df['B_total_current_liab@xbx']
    extra_agg_dict['流动比率'] = 'last'

    # 新增速动比率
    df['速动比率'] = (df['B_total_current_assets@xbx'] - df['B_inventory@xbx']) / df['B_total_current_liab@xbx']
    extra_agg_dict['速动比率'] = 'last'

    # 计算偿债能力
    # 现金流量比率 = 经营活动现金流量÷流动负债；与行业平均水平相比进行分析
    df['现金流量比率'] = df['C_ncf_from_oa@xbx'] / df['B_total_current_liab@xbx']
    extra_agg_dict['现金流量比率'] = 'last'

    #  存货周转率 = 营业成本 / 存货 高 false
    df['存货周转'] = 365 * df['B_inventory@xbx'] / (df['R_operating_total_cost@xbx'] - df['R_asset_impairment_loss@xbx'])
    extra_agg_dict['存货周转'] = 'last'

    df['存货周转率'] = df['R_operating_cost@xbx'] / df['B_inventory@xbx']
    extra_agg_dict['存货周转率'] = 'last'

    # 基本每股收益 true 要小
    df['基本每股收益'] = df['R_basic_eps@xbx']
    extra_agg_dict['基本每股收益'] = 'last'

    # 计算经营安全边际率
    df['经营安全边际率'] = df['归母净利润率(ttm)'] / df['毛利率(ttm)']
    extra_agg_dict['经营安全边际率'] = 'last'

    # 计算经营活动产生的现金流量净额
    df['经营活动产生的现金流量净额'] = df['C_ncf_from_oa@xbx']
    extra_agg_dict['经营活动产生的现金流量净额'] = 'last'

    df['净利润_TTM同比'] = df['R_np@xbx_ttm同比']
    extra_agg_dict['净利润_TTM同比'] = 'last'

    # 计算市净率倒数
    df['BP'] = df['B_total_equity_atoopc@xbx'] / df['总市值']
    extra_agg_dict['BP'] = 'last'

    # 计算市销率
    # 市销率=总市值 / 主营业务收入
    df['ps_ttm'] = df['总市值'] / df['R_revenue@xbx_ttm']
    extra_agg_dict['ps_ttm'] = 'last'

    # 计算净利润TTM同比
    df['净利润_TTM同比'] = df['R_np@xbx_ttm同比']
    extra_agg_dict['净利润_TTM同比'] = 'last'

    # 计算净利润现金含量
    df['T'] = df['R_income_tax_cost@xbx'] / df['R_total_profit@xbx']
    df['净利润现金含量'] = df['C_ncf_from_oa_im@xbx'] * (1 - df['T']) / df['R_np@xbx_ttm']
    extra_agg_dict['净利润现金含量'] = 'last'

    # 投资占比:投资支出/营总收
    df['投资占比'] = df['C_invest_paid_cash@xbx'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['投资占比'] = 'last'

    # 营收含金量：经营净现金流/营总收
    df['营收含金量'] = df['C_ncf_from_oa@xbx'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['营收含金量'] = 'last'

    # #营业收入同比增长率 = 当期营业收入/上期营业收入 -1
    df['营业收入同比增加（ttm）'] = df['R_operating_total_revenue@xbx'] / df['R_operating_total_revenue@xbx'].shift() - 1
    extra_agg_dict['营业收入同比增加（ttm）'] = 'last'

    # 投资占比:投资支出/营总收
    df['投资占比'] = df['C_invest_paid_cash@xbx'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['投资占比'] = 'last'


    return df


def cal_rsi(df, time, extra_agg_dict):
    df["rsi"] = ta.RSI(df['收盘价_复权'], timeperiod = time)
    extra_agg_dict['rsi'] = 'last'
    return df

def cal_boll(df, extra_agg_dict):
    df['boll_upper'], df['boll_middle'], df['boll_lower'] = ta.BBANDS(
        df['收盘价_复权'],
        timeperiod=20,
        # number of non-biased standard deviations from the mean
        nbdevup=2,
        nbdevdn=2,
        # Moving average type: simple moving average here
        matype=0)
    extra_agg_dict['boll_upper'], extra_agg_dict['boll_middle'], extra_agg_dict['boll_lower'] = 'last', 'last', 'last'
    return df

def cal_obv(df, extra_agg_dict):
    df['obv'] = ta.OBV(df['收盘价_复权'], df['成交量'])
    extra_agg_dict['obv'] = 'last'
    return df

# !!!
