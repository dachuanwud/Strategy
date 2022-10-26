"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

选股使用的过滤的脚本
"""
# !!!


from Config import *
from Cnn_model import get_data
import pandas as pd

def simple_moving_average_signal(df):
    """
    简单的移动平均线策略。只能做多。
    当短期均线上穿长期均线的时候，做多，当短期均线下穿长期均线的时候，平仓
    :param df:
    :param para: ma_short, ma_long
    :return: 最终输出的df中，新增字段：signal，记录发出的交易信号
    """

    # ===策略参数
    ma_short = 10  # 短期均线。ma代表：moving_average
    ma_long = 20  # 长期均线

    # ===计算均线。所有的指标，都要使用复权价格进行计算。
    df['ma_short'] = df['收盘价_复权'].rolling(ma_short, min_periods=1).mean()
    df['ma_long'] = df['收盘价_复权'].rolling(ma_long, min_periods=1).mean()

    # ===找出做多信号
    condition1 = df['ma_short'] > df['ma_long']  # 短期均线 > 长期均线
    condition2 = df['ma_short'].shift(1) <= df['ma_long'].shift(1)  # 上一周期的短期均线 <= 长期均线

    df = df[condition1 & condition2]

    print(df[['交易日期', '股票名称']].tail(200))
    exit()
    factors_rank_dict = {  # 定义需要进行rank的因子
        '总市值': True,
    }
    merge_factor_list = []  # 定义合并需要的list
    for factor in factors_rank_dict:  # 遍历factors_rank_dict进行排序
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=factors_rank_dict[factor], method='first')
        merge_factor_list.append(factor + '_rank')  # 将计算好的因子rank添加到list中
    df['因子'] = df[merge_factor_list].mean(axis=1)  # 对量价因子进行等权合并，生成新的因子
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first')  # 对因子进行排名
    df = df[df['排名'] <= select_stock_num]  # 选取排名靠前的股票

    return df

def BIAS_signal(df):
    # 三个参数
    n1 = 10
    n2 = 20
    n3 = 30

    df = df[df['下日_是否交易'] == 1]
    df = df[df['下日_开盘涨停'] == False]
    df = df[df['下日_是否ST'] == False]
    df = df[df['下日_是否退市'] == False]
    # 计算均线
    df["ma_short"] = df["收盘价_复权"].rolling(n1).mean()
    df["ma_median"] = df["收盘价_复权"].rolling(n2).mean()
    df["ma_long"] = df["收盘价_复权"].rolling(n3).mean()
    # 计算bias
    df["bias_short"] = (df["收盘价_复权"] - df["ma_short"]) / df["ma_short"] * 100
    df["bias_median"] = (df["收盘价_复权"] - df["ma_median"]) / df["ma_median"] * 100
    df["bias_long"] = (df["收盘价_复权"] - df["ma_long"]) / df["ma_long"] * 100
    # 找到做多信号
    condition = (df["bias_short"] > 5) & (df["bias_median"] > 7) & (df["bias_long"] > 11)
    print(df[['交易日期','股票名称']].tail(200))
    exit()
    df = df[condition]

    factors_rank_dict = {  # 定义需要进行rank的因子
        '总市值': True,
    }
    merge_factor_list = []  # 定义合并需要的list
    for factor in factors_rank_dict:  # 遍历factors_rank_dict进行排序
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=factors_rank_dict[factor], method='first')
        merge_factor_list.append(factor + '_rank')  # 将计算好的因子rank添加到list中
    df['因子'] = df[merge_factor_list].mean(axis=1)  # 对量价因子进行等权合并，生成新的因子
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first')  # 对因子进行排名
    df = df[df['排名'] <= select_stock_num]  # 选取排名靠前的股票
    return df

def gugu_test(df):


    df = df[df['周五涨跌幅'] < 0.035]
    df = df[df['周五涨跌幅'] > -0.092]

    # ======根据各类条件对股票进行筛选

    condition = (df['5日累计涨跌幅'] < 0.1)
    condition &= (df['120日累计涨跌幅'] < 0.2)
    condition &= (df['250日累计涨跌幅'] < 0.2)
    condition &= (df['累计涨跌幅_10'] <= 0.15)
    condition &= (df['累计涨跌幅_10'] >= -0.16)

    condition = (df['收盘价_复权'] > df['250日均线'])
    condition &= (df['收盘价_复权'] < df['250日均线'] * 1.2)
    condition &= (df['收盘价_复权'] >= df['周均线_20'])
    condition &= (df['收盘价_复权'] <= df['周均线_20'] * 1.2)

    condition &= (df['macd'] > 0)
    condition &= (df['macd'] < 0.12)
    condition &= (df['周_macd'] > 0)
    condition &= (df['周_macd'] < 0.12)

    df = df[condition]
    print(df[['交易日期','股票名称','收盘价','收盘价_复权','250日均线','周均线_20','macd','周_macd']].tail(200))

    factors_rank_dict = {  # 定义需要进行rank的因子
        '总市值': True,
    }
    merge_factor_list = []  # 定义合并需要的list
    for factor in factors_rank_dict:  # 遍历factors_rank_dict进行排序
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=factors_rank_dict[factor], method='first')
        merge_factor_list.append(factor + '_rank')  # 将计算好的因子rank添加到list中
    df['因子'] = df[merge_factor_list].mean(axis=1)  # 对量价因子进行等权合并，生成新的因子
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first')  # 对因子进行排名
    df = df[df['排名'] <= select_stock_num]  # 选取排名靠前的股票
    # print(df)
    # exit()
    return df

def filter_and_rank(df):  # 通过财务因子设置过滤条件，进行选择和排序
    """
    通过财务因子设置过滤条件，进行选择和排序
    :param df: 原始数据
    :return: 返回 通过财务因子过滤并叠加量价因子的df
    """
    # ======根据各类条件对股票进行筛选
    df['总市值_分位数'] = df.groupby(['交易日期'])['总市值'].rank(ascending=True, pct=True)
    df['归母ROE比120_分位数'] = df.groupby(['交易日期'])['归母ROE比120'].rank(ascending=True, pct=True)
    df['BP_排名'] = df.groupby('交易日期')['BP'].rank(pct=True)
    df['归母EP(ttm)'] = 1 / df['归母PE(ttm)']
    df['归母EP(ttm)_二级行业分位数'] = df.groupby(['交易日期', '申万二级行业名称'])['归母EP(ttm)'].rank(ascending=True, pct=True)
    df['经营活动现金流入小计_分位数'] = df.groupby(['交易日期'])['经营活动现金流入小计'].rank(ascending=True, pct=True)
    df['成交额_排名'] = 10 * df.groupby('交易日期')['成交额'].rank(pct=True)
    df['price_bottom_排名'] = df.groupby(['交易日期'])['price_bottom'].rank(pct=True)
    df['vol_bottom_排名'] = df.groupby(['交易日期'])['vol_bottom'].rank(pct=True)

    # df['成交额std_5_排名'] = df.groupby('交易日期')['成交额std_5'].rank(ascending=True)
    # condition = (df['总市值_分位数'] >= 0.01)
    # condition &= (df['归母ROE比120_分位数'] <= 0.66)
    # condition &= (df['BP_排名'] <= 0.9)
    # condition &= (df['存货周转率'] <= 8.7) & (df['存货周转率'] >= 0.55)
    # condition &= (df['归母EP(ttm)_二级行业分位数'] >= 0.03)
    # condition &= (df['归母EP(ttm)_二级行业分位数'] <= 0.90)
    # condition &= (df['经营活动现金流入小计_分位数'] >= 0)
    # condition &= (df['经营活动现金流入小计_分位数'] <= 0.42)
    # df = df[df[['price_bottom']] >= 1]
    # print(df[['交易日期','股票名称','price_bottom', 'vol_bottom']])
    # exit()
    # ===== 根据技术指标进行筛选
    df = df[df['周五涨跌幅'] < 0.07]
    df = df[df['周五涨跌幅'] > -0.061]

    # df = df[(df['price_bottom'] >= 1) | (df['vol_bottom'] >= 1)]

    condition = (df['成交额_排名'] >= 0.15)
    condition = (df['5日累计涨跌幅'] < 0.075)
    condition &= (df['30日累计涨跌幅'] > -0.115)
    condition &= (df['30日累计涨跌幅'] <= 0.23)
    condition &= (df['10日累计涨跌幅'] > -0.29)
    condition &= (df['10日累计涨跌幅'] < 0.20)

    condition &= (df['收盘价_复权'] > df['30日均线'])
    condition &= (df['收盘价_复权'] < df['30日均线'] * 1.12)
    condition &= (df['收盘价_复权'] >= df['周均线_20'])
    condition &= (df['收盘价_复权'] <= df['周均线_20'] * 1.12)

    condition &= (df['macd'] > 0)
    condition &= (df['macd'] < 0.12)
    condition &= (df['周_macd'] > 0)
    condition &= (df['周_macd'] < 0.12)

    df = df[condition]  # 综上所有财务因子的过滤条件，选股
    factors_rank_dict = {  # 定义需要进行rank的因子
        '成交额_排名': True,
    }
    merge_factor_list = []  # 定义合并需要的list
    for factor in factors_rank_dict:  # 遍历factors_rank_dict进行排序
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=factors_rank_dict[factor], method='first')
        merge_factor_list.append(factor + '_rank')  # 将计算好的因子rank添加到list中
    df['因子'] = df[merge_factor_list].mean(axis=1)  # 对量价因子进行等权合并，生成新的因子
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first')  # 对因子进行排名
    df = df[df['排名'] <= select_stock_num]  # 选取排名靠前的股票
    # print(df[['交易日期','股票名称','price_bottom','下周期涨跌幅']].tail(200))
    # exit()
    return df

# !!!
