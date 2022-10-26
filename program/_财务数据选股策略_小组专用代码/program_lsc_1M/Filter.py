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

    if is_input_data == True:
        return df

    condition = (df['总市值_分位数'] >= 0.01)
    condition &= (df['归母ROE比120_分位数'] <= 0.66)
    condition &= (df['BP_排名'] <= 0.9)
    condition &= (df['存货周转率'] <= 8.7) & (df['存货周转率'] >= 0.55)
    condition &= (df['归母EP(ttm)_二级行业分位数'] >= 0.03)
    condition &= (df['归母EP(ttm)_二级行业分位数'] <= 0.90)
    condition &= (df['经营活动现金流入小计_分位数'] >= 0)
    condition &= (df['经营活动现金流入小计_分位数'] <= 0.42)
    condition &= df['10VWAP'] <= 14
    condition &= df['10VWAP'] >= 5
    condition &= (df['成交额_排名'] >= 0.15)
    condition &= (df['10日累计涨跌幅'] < 0.2)
    condition &= (df['120日累计涨跌幅'] < 0.2)
    condition &= (df['250日累计涨跌幅'] < 0.2)

    # ===== 根据技术指标进行筛选
    condition &= (df['rsi'] >= 20)
    condition &= (df['rsi'] <= 80)

    df = df[condition]  # 综上所有财务因子的过滤条件，选股

    # 基于cnn的观测器进行筛选股票
    input_net_df = df[['交易日期', '股票名称', '总市值', '换手率','换手率_5avg','换手率_20avg','中户买入占比_5avg','中户买入占比_20avg','散户卖出占比','散户卖出占比_5avg','散户卖出占比_20avg','rsi', '5日均线', 'bias', '5日累计涨跌幅', '申万一级行业名称',
             '归母ROE(ttm)', '归母EP(ttm)', '现金流负债比','总市值_分位数','归母ROE比120_分位数', 'BP_排名','存货周转率',
             '归母EP(ttm)_二级行业分位数','经营活动现金流入小计_分位数','10VWAP','成交额_排名','10日累计涨跌幅','120日累计涨跌幅','250日累计涨跌幅','下周期每天涨跌幅']]
    # df_predict = pd.DataFrame(columns=['A'])
    # df_predict['A']  = get_data(input_net_df)[0]
    # df['predict_涨跌幅'] = list(get_data(input_net_df)[0])
    # df = df[df['predict_涨跌幅'] > 0]
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
    print(df.tail(100))
    exit()
    return df

# !!!
