"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

财务数据选股专属代码

整理股票数据，为之后的选股进行准备
"""
import platform
from datetime import datetime
from multiprocessing import Pool, freeze_support, cpu_count
from Signals import *

from Config import *
# import sys
# sys.path.append("E:\Quantcalss\财务数据选股策略\香农\program")
from CalcFactor import *
from Function_fin import *
from Functions import *
from Config import *
import pandas as pd
import time

import warnings
warnings.filterwarnings('ignore')

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
# pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数

# ===读取准备数据
# 读取所有股票代码的列表
# stock_code_list = get_stock_code_list_in_one_dir(r'E:\Quantcalss\data-api\data\stock-trading-data-pro')
stock_code_list = get_stock_code_list_in_one_dir(stock_data_path)
print('股票数量：', len(stock_code_list))

# 导入上证指数，保证指数数据和股票数据在同一天结束，不然会出现问题。
# index_data = import_index_data(r'E:\Quantcalss\data-api\data\index\sh000300.csv', back_trader_end=date_end)
index_data = import_index_data(index_path, back_trader_end=date_end)
# index_data_CY = import_index_data(index_path + '\sz399006.csv', back_trader_end=date_end)


# 计算n日布林下轨
def Boll_lower(df, n, col='high'):
    # 布林优化
    b = df[col].rolling(n, min_periods=1).mean()

    df['median'] = b
    df['std'] = df[col].rolling(n, min_periods=1).std(ddof=0)
    df['z_score'] = abs(df[col] - df['median']) / df['std']
    df['m'] = df['z_score'].rolling(window=n).max().shift()
    # df['upper'] = df[f'median_{n}'] + df['std'] * df['m']
    df['lower'] = df['median'] - df['std'] * df['m']
    # df[f'{col}_lower'] = df[f'median_{n}'] - df[f'std_{n}'] * df[f'm_{n}']
    df.drop(['median', 'std', 'z_score', 'm'], axis=1, inplace=True)
    return df
Boll_lower(index_data, 34, 'high')
# Boll_lower(index_data_CY, 46, 'high')


# ===循环读取并且合并
def calculate_by_stock(code):
    """
    整理数据核心函数
    :param code: 股票代码
    :return: 一个包含该股票所有历史数据的DataFrame
    """
    print(code, '开始计算')
    # =读入股票数据
    # path = r'E:\Quantcalss\data-api\data\stock-trading-data-pro' + '/%s.csv' % code
    path = stock_data_path + '/%s.csv' % code
    df = pd.read_csv(path, encoding='gbk', skiprows=1, parse_dates=['交易日期'])
    # df['净利润TTM'] = (df['净利润TTM'].fillna(method='ffill'))  # 向上寻找最近的一个非空值
    # df['现金流TTM'] = (df['现金流TTM'].fillna(method='ffill'))  # 向上寻找最近的一个非空值
    # df["净资产"] = (df["净资产"].fillna(method='ffill'))  # 向上寻找最近的一个非空值
    # df['总资产'] = (df['总资产'].fillna(method='ffill'))  # 向上寻找最近的一个非空值
    # df['总负债'] = (df['总负债'].fillna(method='ffill'))  # 向上寻找最近的一个非空值
    # df['净利润(当季)'] = (df['净利润(当季)'].fillna(method='ffill'))  # 向上寻找最近的一个非空值

    # =计算涨跌幅
    df['涨跌幅'] = df['收盘价'] / df['前收盘价'] - 1
    df['开盘买入涨跌幅'] = df['收盘价'] / df['开盘价'] - 1  # 为之后开盘买入做好准备

    # =计算复权价：计算所有因子当中用到的价格，都使用复权价
    df = cal_fuquan_price(df, fuquan_type)
    # =计算涨跌停价格
    df = cal_zdt_price(df)
    # =计算交易天数
    df['上市至今交易天数'] = df.index + 1
     

    extra_agg_dict = {}  # 在转换周期时使用
    # =计算量价选股因子：这个函数需要大家根据需要自行修改
    df = cal_tech_factor(df, extra_agg_dict)
    
    # 指数布林带过滤
    df = pd.merge(df, index_data, on=['交易日期'], how='left')
    df['指数趋势良好'] = df['low'] > df['lower']
    df['指数趋势良好'] = df['指数趋势良好'].shift()
    df = df.loc[df['指数趋势良好'] == True]
    df.drop(['high', 'low', 'lower'], axis=1, inplace=True)

    # # 个股布林带过滤
    # Boll_lower(df, 21, '收盘价')
    # df['个股趋势良好'] = df['收盘价'] > df['lower']
    # df['个股趋势良好'] = df['个股趋势良好'].shift()
    # # df = df.loc[df['个股趋势良好'] == True]

    # # 双重布林带过滤(需去注释指数布林带和个股布林带代码)
    # df = df.loc[(df['指数趋势良好'] == True) & (df['个股趋势良好'] == True)]
      
    if df.empty:
        return pd.DataFrame()
    
    
    # =需要额外保存的字段
    extra_fill_0_list = []  # 在和上证指数合并时使用。



    # =将股票和上证指数合并，补全停牌的日期，新增数据"是否交易"、"指数涨跌幅"
    df = merge_with_index_data(df, index_data, extra_fill_0_list)


    # =股票退市时间小于指数上市时间，就会出现空值
    if df.empty:
        return pd.DataFrame()

    # # =计算量价选股因子：这个函数需要大家根据需要自行修改
    # df = cal_tech_factor(df, extra_agg_dict)

   

    # =导入财务数据，并计算相关衍生指标
    finance_df = import_fin_data(code, finance_data_path)

    # 提前定义一个空的列表，避免财务数据为空
    columns_list = []
    if not finance_df.empty:  # 如果数据不为空

        # 计算财务数据：选取需要的字段、计算指定字段的同比、环比、ttm等指标
        finance_df, finance_df_ = proceed_fin_data(finance_df, raw_fin_cols, flow_fin_cols, cross_fin_cols,
                                                   derived_fin_cols)
        # 获取去年同期的数据,如果需要计算，把这两行代码取消注释即可
        # df_, columns_list = get_his_data(finance_df_, ['R_np_atoopc@xbx', 'R_np@xbx'], span='4q')
        # finance_df = pd.merge(left=finance_df, right=df_[['publish_date'] + columns_list], on='publish_date',
        #                       how='left')
        # 财务数据和股票k线数据合并，使用merge_asof
        df = pd.merge_asof(left=df, right=finance_df, left_on='交易日期', right_on='publish_date',
                           direction='backward')

    else:  # 如果数据为空
        for col in raw_fin_cols + derived_fin_cols:
            df[col] = np.nan

    # 有修改
    for col in raw_fin_cols + columns_list:  # 财务数据在周期转换的时候，都是选取最后一天的数据
        extra_agg_dict[col] = 'last'

    # =计算财务因子：这个函数需要大家根据需要自行修改
    df = calc_fin_factor(df, extra_agg_dict)

    # =计算下个交易的相关情况
    df['下日_是否交易'] = df['是否交易'].shift(-1)
    df['下日_一字涨停'] = df['一字涨停'].shift(-1)
    df['下日_开盘涨停'] = df['开盘涨停'].shift(-1)
    df['下日_是否ST'] = df['股票名称'].str.contains('ST').shift(-1)
    df['下日_是否S'] = df['股票名称'].str.contains('S').shift(-1)
    df['下日_是否退市'] = df['股票名称'].str.contains('退').shift(-1)
    df['下日_开盘买入涨跌幅'] = df['开盘买入涨跌幅'].shift(-1)

    extra_agg_dict['申万二级行业名称'] = 'last'
    extra_agg_dict['申万一级行业名称'] = 'last'
    
    # 处理择时后涨跌幅
    df = timing_strategy_process(df, extra_agg_dict)
    # =将日线数据转化为月线或者周线
    df = transfer_to_period_data(df, period_type, extra_agg_dict)

    # =对数据进行整理
    # 删除上市的第一个周期
    df.drop([0], axis=0, inplace=True)  # 删除第一行数据
    # 删除2007年之前的数据
    df = df[df['交易日期'] > pd.to_datetime('20061231')]
    # 计算下周期每天涨幅
    df['下周期每天涨跌幅'] = df['每天涨跌幅'].shift(-1)
    df['下周期涨跌幅'] = df['涨跌幅'].shift(-1)
    del df['每天涨跌幅']

    # 计算下周期择时涨跌幅
    df['下周期每天涨跌幅_择时'] = df['每天涨跌幅_择时'].shift(-1)
    df['下周期涨跌幅_择时'] = df['涨跌幅_择时'].shift(-1)
    del df['每天涨跌幅_择时']

    # 删除月末为st状态的周期数
    df = df[df['股票名称'].str.contains('ST') == False]
    # 删除月末为s状态的周期数
    df = df[df['股票名称'].str.contains('S') == False]
    # 删除月末有退市风险的周期数
    df = df[df['股票名称'].str.contains('退') == False]
    # 删除月末不交易的周期数
    df = df[df['是否交易'] == 1]
    # 删除交易天数过少的周期数
    # df = df[df['交易天数'] / df['市场交易天数'] >= 0.8]
    df.drop(['交易天数', '市场交易天数'], axis=1, inplace=True)
    
    # 控制CPU温度
    time.sleep(0.3)

    return df  # 返回计算好的数据


# ===并行提速的办法
if __name__ == '__main__':

    # 添加对windows多进程的支持
    # https://docs.python.org/zh-cn/3.7/library/multiprocessing.html
    if 'Windows' in platform.platform():
        freeze_support()

    # 试运行
    # df = calculate_by_stock('sh603196')
    # exit()

    # 标记开始时间
    start_time = datetime.now()
    print(start_time)

    multiple_process = True
    # 标记开始时间
    if multiple_process:
        # 开始并行
        with Pool(max(cpu_count() - 1, 1)) as pool:
            # 使用并行批量获得data frame的一个列表
            df_list = pool.map(calculate_by_stock, sorted(stock_code_list))
            print('读入完成, 开始合并', datetime.now() - start_time)

    else:
        df_list = []
        for stock in stock_code_list:
            res_df = calculate_by_stock(stock)
            df_list.append(res_df)

    # 合并为一个大的DataFrame
    all_stock_data = pd.concat(df_list, ignore_index=True)
    all_stock_data.sort_values(['交易日期', '股票代码'], inplace=True)  # ===将数据存入数据库之前，先排序、reset_index
    all_stock_data.reset_index(inplace=True, drop=True)

    # 将数据存储到pickle文件
    all_stock_data.to_pickle(root_path + '/data/output/选股策略/all_stock_data_' + period_type + '.pkl')

    # 看一下花了多久
    print(datetime.now() - start_time)
