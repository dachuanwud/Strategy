
# !!!


from Config import *

def filter_and_rank_M(df):
    """
    通过财务因子设置过滤条件
    :param df: 原始数据
    :return: 返回 通过财务因子过滤并叠加量价因子的df
    """
    # === 前置过滤,注意这样筛选有前后顺序不同，导致结果不同。
    # ===删除下个交易日不交易、开盘涨停的股票，因为这些股票在下个交易日开盘时不能买入。

    df = df[df['周五涨跌幅'] < 0.07]
    df = df[df['周五涨跌幅'] > -0.061]
    # df = df[df['上影线'] < 0.05]
    # 选股的方法请写在这里
    ascending = True

    df['流通市值_排名'] = df.groupby('交易日期')['流通市值'].rank(pct=True)

    df['bias_5_排名'] = df.groupby('交易日期')['bias_5'].rank()
    df['bias_10_排名'] = df.groupby('交易日期')['bias_10'].rank()
    df['L97_排名'] = df.groupby('交易日期')['L97'].rank(ascending=True)
    df['成交额std_5_排名'] = df.groupby('交易日期')['成交额std_5'].rank(ascending=True)
    df['成交额std_10_排名'] = df.groupby('交易日期')['成交额std_10'].rank(ascending=True)
    df['成交额std_20_排名'] = df.groupby('交易日期')['成交额std_20'].rank(ascending=True)
    #根据郑老板新增30、60排名
    df['成交额std_30_排名'] = df.groupby('交易日期')['成交额std_30'].rank(ascending=True)
    df['成交额std_60_排名'] = df.groupby('交易日期')['成交额std_60'].rank(ascending=True)
    df['量价相关性_10_排名'] = df.groupby('交易日期')['量价相关性_10'].rank(ascending=True)
    df['量价相关性_30_排名'] = df.groupby('交易日期')['量价相关性_30'].rank(ascending=True)
    df['量价相关性_60_排名'] = df.groupby('交易日期')['量价相关性_60'].rank(ascending=True)
    df['Illiquidity_排名'] = df.groupby('交易日期')['Illiquidity'].rank(ascending=True)
    df['量稳换手率变化率_排名'] = df.groupby('交易日期')['量稳换手率变化率'].rank(ascending=False)
    df['cro_w_排名'] = df.groupby('交易日期')['cro_w'].rank(ascending=False)
    df['cro_m_排名'] = df.groupby('交易日期')['cro_m'].rank(ascending=False)
    df['cro_2w_排名'] = df.groupby('交易日期')['cro_2w'].rank(ascending=True)
    df['cro_3w_排名'] = df.groupby('交易日期')['cro_3w'].rank(ascending=True)

    # 利润要大
    df['归母净利润单季环比分位数'] = df.groupby(['交易日期'])['归母净利润单季环比'].rank(ascending=True, pct=True)
    condition = (df['归母净利润单季环比分位数'] >= 0.3)
    # ROE 要高
    df['归母ROE(ttm)'] = df.groupby(['交易日期'])['归母ROE(ttm)'].rank(ascending=False, pct=True)
    condition &= (df['归母ROE(ttm)'] >= 0.3) & (df['归母ROE(ttm)'] <= 0.9)
    # 相对低价
    df['归母ROE比120_分位数'] = df.groupby(['交易日期'])['归母ROE比120'].rank(ascending=False, pct=True)
    condition &= (df['归母ROE比120_分位数'] <= 0.4)
    # condition &= (df['归母ROE比120_分位数'] >= 0.1)
    #毛利率大于0
    condition = df['毛利率(ttm)'] > 0
    # PE要低，且去除行业属性，计算归母PE(ttm) 在二级行业的分位数
    # 归母PE(ttm)会存在负数的情况 => 先求倒数，EP要大的好。ascending=True从小到大排，
    df['归母EP(ttm)'] = 1 / df['归母PE(ttm)']
    df['归母EP(ttm)_二级行业分位数'] = df.groupby(['交易日期', '申万二级行业名称'])['归母EP(ttm)'].rank(ascending=True, pct=True)
    condition &= (df['归母EP(ttm)_二级行业分位数'] >= 0.3)

    df = df[(df['大户资金净流入'] > 0.2) & (df['big_cash_ma5'] > 1) & (df['big_cash_ma10'] > 0.2) &
            (df['mid_cash_ma10'] < 0.2) & (df['mid_cash_ma5'] > 0.3)]

    # df = df[(df['J'] > 9) & (df['D'] > 40)]
    df = df[(df['J'] > -5)]
    df = df[df['MACD_Hist'] > 0.083]

    condition &= df['bias_5'] <= 9
    condition &= df['bias_30'] <= 9
    #
    # df['VWAP10'] = df.groupby(['交易日期'])['10VWAP'].rank(ascending=False, pct=True)
    # condition &= (df['VWAP10'] <= 0.92)
    # condition &= df['10VWAP'] <= 10
    #
    df['BP_排名'] = df.groupby('交易日期')['BP'].rank(pct=True)
    condition &= (df['BP_排名'] <= 0.96)
    condition &= (df['BP_排名'] >= 0.1)
    #
    # df['成交额_排名'] = 5 * df.groupby('交易日期')['成交额'].rank(pct=True)
    # condition &= (df['成交额_排名'] >= 0.05)

    # df['空方力量_排名'] = df.groupby('交易日期')['空方力量'].rank(pct=True)
    # condition &= (df['空方力量_排名'] >= 0.013)

    #择时指标
    condition &= (df['均线_5'] > df['均线_31'])

    condition &= (df['成交额'] > df['成交额_5'])

    # condition &= (df['累计涨跌幅_5'] <= 0.1)
    # condition &= (df['累计涨跌幅_10'] <= 0.15)
    # condition &= (df['累计涨跌幅_10'] >= -0.16)

    # condition &= (df['成交额_5'] > df['成交额_60'])
    # condition &= (df['均线_31'].shift(1) <= df['均线_31'])
    # & (df['均线_31'].shift(2) <= df['均线_31']).shift(1)

    condition &= (df['5日累计涨跌幅'] < 0.1)
    condition &= (df['10日累计涨跌幅'] > -0.09)
    condition &= (df['20日累计涨跌幅'] > -0.03)
    condition &= (df['30日累计涨跌幅'] > -0.115)
    condition &= (df['10日累计涨跌幅'] < 0.23)
    condition &= (df['20日累计涨跌幅'] < 0.25)
    # condition &= (df['5日累计涨跌幅'] > -0.08)
    # === 综上所有财务因子的过滤条件，选股

    df = df[condition]

    # 定义需要进行rank的因子， 排序方式，True从小到大，False从大到小
    factors_rank_dict = [
        ('总市值', True, 1),
    ]

    for (factor, ascending, rate) in factors_rank_dict:
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=ascending, method='first')
    df['因子'] = 0
    for (factor, ascending, rate) in factors_rank_dict:
        df['因子'] += df[factor + '_rank'] * rate
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first')
    df = df[df['排名'] <= select_stock_num]
    # print(df.tail(200))
    # exit()
    return df

# !!!
