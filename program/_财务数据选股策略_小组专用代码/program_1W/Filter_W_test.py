"""
一、策略思路
先基于上一期岛老板的帖子抄了因子，给大家做因子参考。
不过实际只用了现金流量比例。

二、策略描述
现金流比负债高，说明经营比较稳健，我觉得老板比较务实。
在这个浮躁的年代这么稳健也很好了。
"""
# !!!


from Config import *

def filter_and_rank_W_test(df):
    """
    通过财务因子设置过滤条件
    :param df: 原始数据
    :return: 返回 通过财务因子过滤并叠加量价因子的df
    """
    # === 前置过滤,注意这样筛选有前后顺序不同，导致结果不同。
    # ===删除下个交易日不交易、开盘涨停的股票，因为这些股票在下个交易日开盘时不能买入。

    df = df[df['周五涨跌幅'] < 0.04]
    df = df[df['周五涨跌幅'] > -0.092]
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

    # df['经营活动现金流入小计_分位数'] = df.groupby(['交易日期'])['经营活动现金流入小计'].rank(ascending=True, pct=True)
    # condition &= (df['经营活动现金流入小计_分位数'] >= 0)
    # # condition &= (df['经营活动现金流入小计_分位数'] <= 0.99)
    #
    # df['成交额_排名'] = 10 * df.groupby('交易日期')['成交额'].rank(pct=True)
    # condition &= (df['成交额_排名'] >= 0.1)

    # condition &= (df['30日累计涨跌幅'] < 0.18)

    # condition &= (df['存货周转率'] <= 8.7) & (df['存货周转率'] >= 0.55)

    # condition &= (df['累计涨跌幅_30'] < 0.18)

    # df['BP_排名'] = df.groupby('交易日期')['BP'].rank(pct=True)
    # condition &= (df['BP_排名'] <= 0.9)
    # df['VWAP10'] = df.groupby(['交易日期'])['10VWAP'].rank(ascending=False, pct=True)
    # condition &= df['10VWAP'] <= 30

    # ****************红牛***********
    # df['归母PE(ttm)_分位数'] = df.groupby(['交易日期'])['归母EP(ttm)'].rank(ascending=False, pct=True)
    # condition &= (df['归母PE(ttm)_分位数'] >= 0.093)
    #
    # df['归母PE(ttm)比120_分位数'] = df.groupby(['交易日期'])['归母PE(ttm)比120'].rank(ascending=False, pct=True)
    # condition &= (df['归母PE(ttm)比120_分位数'] <= 0.82)


    # df['归母净利润单季环比分位数'] = df.groupby(['交易日期'])['归母净利润单季环比'].rank(ascending=False, pct=True)
    # condition &= (df['归母净利润单季环比分位数'] <= 0.9)

    # 计算企业倍数 在所有股票的分位数
    # 获取企业倍数 较小 的股票
    # 企业倍数存在负数的情况 => 先求倒数，再从大到小排序
    # df['企业倍数_倒数'] = 1 / df['企业倍数']
    # df['企业倍数_分位数'] = df.groupby(['交易日期'])['企业倍数_倒数'].rank(ascending=False, pct=True)
    # condition &= (df['企业倍数_分位数'] <= 0.189)

    # 计算现金流负债比 在所有股票的分位数
    # 获取现金流负债比 较大 的股票
    # df['现金流负债比_分位数'] = df.groupby(['交易日期'])['现金流负债比'].rank(ascending=False, pct=True)
    # condition &= (df['现金流负债比_分位数'] <= 0.42)

    # df['中户资金流比'] = df.groupby(['交易日期'])['中户资金流'].rank(ascending=False, pct=True)
    # condition &= (df['中户资金流比'] <= 0.3)
    #
    # df['散户资金流出比'] = df.groupby(['交易日期'])['散户资金流'].rank(ascending=False, pct=True)
    # condition &= (df['散户资金流出比'] <= 0.233)
    #
    # df['大户资金流出比'] = df.groupby(['交易日期'])['大户资金流比'].rank(ascending=False, pct=True)
    # condition &= (df['大户资金流出比'] <= 0.99)

    # df['毛利率(ttm)_倒数'] = 1 / df['毛利率(ttm)']
    # df['毛利率_分位数'] = df.groupby(['交易日期'])['毛利率(ttm)_倒数'].rank(ascending=False, pct=True)
    # condition &= (df['毛利率_分位数'] >= 0.21) & (df['毛利率_分位数'] <= 0.6)
    #
    # df['10日累计涨跌幅20日标准差_分位数'] = df.groupby(['交易日期'])['10日累计涨跌幅20日标准差'].rank(ascending=True, pct=True)
    # df['20日累计涨跌幅20日标准差_分位数'] = df.groupby(['交易日期'])['20日累计涨跌幅20日标准差'].rank(ascending=True, pct=True)
    # condition &= (df['20日累计涨跌幅20日标准差_分位数'] / df['10日累计涨跌幅20日标准差_分位数'] >= 0.12)

    # df['换手率比'] = df.groupby(['交易日期'])['换手率'].rank(ascending=False, pct=True)
    # df['5换手率'] = df.groupby(['交易日期'])['5日换手率'].rank(ascending=False, pct=True)
    # df['10换手率'] = df.groupby(['交易日期'])['10日换手率'].rank(ascending=False, pct=True)
    # condition &= (df['5换手率'] <= df['10换手率'] / df['5换手率'])
    # condition &= (df['换手率比'] >= 0.16)

    # df['30成交额'] = df.groupby(['交易日期'])['成交额_30'].rank(ascending=False, pct=True)
    # df['60成交额'] = df.groupby(['交易日期'])['成交额_60'].rank(ascending=False, pct=True)
    # condition &= (df['30成交额'] / df['60成交额'] >= 0.78)

    # df['成交额_M50_std_分位数'] = df.groupby(['交易日期'])['成交额_M50_std'].rank(ascending=False, pct=True)
    # condition &= df['成交额_M50_std_分位数'] >= 0.08
    #
    # df['120日价线率_分位数'] = df.groupby(['交易日期'])['120日价线率'].rank(ascending=False, pct=True)
    # condition &= (df['120日价线率_分位数'] <= 0.848)

    # df['现金流平均比120_分位数'] = df.groupby(['交易日期'])['现金流平均比120'].rank(ascending=False, pct=True)
    # condition &= (df['现金流平均比120_分位数'] <= 0.42)

    # df['总负债比_分位数'] = df.groupby(['交易日期'])['总负债比'].rank(ascending=False, pct=True)
    # condition &= (df['总负债比_分位数'] <= 0.75)

    # df['流动比率_分位数'] = df.groupby(['交易日期'])['流动比率'].rank(ascending=False, pct=True)
    # condition &= (df['流动比率_分位数'] <= 0.97)

    # df['经营活动现金流出小计_分位数'] = df.groupby(['交易日期'])['经营活动现金流出小计'].rank(ascending=False, pct=True)
    # condition &= (df['经营活动现金流出小计_分位数'] >= 0.15)

    # df['经营活动产生的现金流量净额_分位数'] = df.groupby(['交易日期'])['经营活动产生的现金流量净额'].rank(ascending=False, pct=True)
    # condition &= (df['经营活动产生的现金流量净额_分位数'] >= 0.08) & (df['经营活动产生的现金流量净额_分位数'] <= 0.45)
    #
    # df['净利润_TTM同比分位数'] = df.groupby(['交易日期'])['净利润_TTM同比'].rank(ascending=False, pct=True)
    # condition &= (df['净利润_TTM同比分位数'] <= 0.74) & (df['净利润_TTM同比分位数'] >= 0.02)
    #
    # condition &= (df['速动比率'] >= 0.3) & (df['速动比率'] <= 4)
    #根据邓老板

    # condition &= (df['累计涨跌幅_60'] <= 0.16)
    # condition &= (df['累计涨跌幅_5'] >= -0.168)
    # condition &= (df['累计涨跌幅_10'] >= -0.3)
    # condition &= (df['存货周转率'] <= 8.7)
    # condition &= (df['存货周转率'] <= 8.7) & (df['存货周转率'] >= 0.5)
    # condition &= (df['ps_ttm'] >= 0.57)
    # condition &= df['基本每股收益'] <= 0.7
    #
    # condition &= (df['经营安全边际率'] >= 0.77) & (df['经营安全边际率'] <= 4.2)
    #


    df = df[(df['大户资金净流入'] > 0) & (df['big_cash_ma5'] > 0) & (df['big_cash_ma10'] > 0) &
            (df['mid_cash_ma10'] < 0) & (df['mid_cash_ma5'] > 0)]
    # df = df[(df['J'] > 9) & (df['D'] > 40)]
    df = df[(df['J'] > -12)]
    df = df[df['MACD_Hist'] > 0.08]
    condition &= df['bias_5'] <= 10
    condition &= df['bias_30'] <= 10
    #
    # df['VWAP10'] = df.groupby(['交易日期'])['10VWAP'].rank(ascending=False, pct=True)
    # condition &= (df['VWAP10'] <= 0.92)
    # condition &= df['10VWAP'] <= 10
    #
    df['BP_排名'] = df.groupby('交易日期')['BP'].rank(pct=True)
    condition &= (df['BP_排名'] <= 0.96)
    condition &= (df['BP_排名'] >= 0.09)
    #
    # df['成交额_排名'] = 5 * df.groupby('交易日期')['成交额'].rank(pct=True)
    # condition &= (df['成交额_排名'] >= 0.05)

    # df['空方力量_排名'] = df.groupby('交易日期')['空方力量'].rank(pct=True)
    # condition &= (df['空方力量_排名'] >= 0.013)

    #择时指标
    condition &= (df['均线_5'] > df['均线_31'])
    condition &= (df['成交额'] > df['成交额_5'])

    condition &= (df['累计涨跌幅_5'] <= 0.1)
    # condition &= (df['累计涨跌幅_10'] <= 0.15)
    # condition &= (df['累计涨跌幅_10'] >= -0.16)

    # condition &= (df['成交额_5'] > df['成交额_60'])
    # condition &= (df['均线_31'].shift(1) <= df['均线_31'])
    # & (df['均线_31'].shift(2) <= df['均线_31']).shift(1)


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
