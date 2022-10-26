"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

选股使用的过滤的脚本
"""
# !!!


from Config import *


def filter_and_rank(df):
    """
    通过财务因子设置过滤条件
    :param df: 原始数据
    :return: 返回 通过财务因子过滤并叠加量价因子的df
    """
    # ======根据各类条件对股票进行筛选

    # 计算归母PE(ttm) 在二级行业的分位数
    # 获取归母PE(ttm) 较小 的股票
    # 归母PE(ttm)会存在负数的情况 => 先求倒数，再从大到小排序
    df['归母EP(ttm)'] = 1 / df['归母PE(ttm)']
    df['归母PE(ttm)_二级行业分位数'] = df.groupby(['交易日期', '申万二级行业名称'])['归母EP(ttm)'].rank(ascending=False, pct=True)
    condition = (df['归母PE(ttm)_二级行业分位数'] <= 0.4)

    # 计算归母PE(ttm) 在所有股票的分位数
    # 获取归母PE(ttm) 较小的股票
    # 归母PE(ttm)会存在负数的情况 => 复用之前 PE(ttm) 的倒数 EP(ttm),再从大到小排序
    df['归母PE(ttm)_分位数'] = df.groupby(['交易日期'])['归母EP(ttm)'].rank(ascending=False, pct=True)
    condition &= (df['归母PE(ttm)_分位数'] > 0.1)
    condition &= (df['归母PE(ttm)_分位数'] <= 0.4)

    # 计算企业倍数 在所有股票的分位数
    # 获取企业倍数 较小 的股票
    # 企业倍数存在负数的情况 => 先求倒数，再从大到小排序
    df['企业倍数_倒数'] = 1 / df['企业倍数']
    df['企业倍数_分位数'] = df.groupby(['交易日期'])['企业倍数_倒数'].rank(ascending=False, pct=True)
    condition &= (df['企业倍数_分位数'] <= 0.4)

    # 计算现金流负债比 在所有股票的分位数
    # 获取现金流负债比 较大 的股票
    df['现金流负债比_分位数'] = df.groupby(['交易日期'])['现金流负债比'].rank(ascending=False, pct=True)
    condition &= (df['现金流负债比_分位数'] <= 0.4)

    # 综上所有财务因子的过滤条件，选股
    df = df[condition]

    factors_rank_list = {
        ('总市值', True, 1.0),
        ('归母ROE(ttm)', False, 1.0)
    }

    for (factor, ascending, rate) in factors_rank_list:
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=ascending, method='first')
    df['因子'] = 0
    for (factor, ascending, rate) in factors_rank_list:
        df['因子'] += df[factor + '_rank'] * rate
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first')
    df = df[df['排名'] <= select_stock_num]

    return df

# !!!
