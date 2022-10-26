# !!!
from Config import *


def filter_and_rank(df):
    df['总市值_分位数'] = df.groupby(['交易日期'])['总市值'].rank(ascending=True, pct=True)
    condition = (df['总市值_分位数'] >= 0.01)
    
    df['存货周转_分位数'] = df.groupby(['交易日期'])['存货周转'].rank(ascending=False, pct=True)
    condition &= (df['存货周转_分位数'] >= 0.3)
    condition &= (df['存货周转_分位数'] <= 0.62)
    
    df['经营现金流量总负债比_分位数'] = df.groupby(['交易日期'])['经营现金流量总负债比'].rank(ascending=True, pct=True)
    condition &= (df['经营现金流量总负债比_分位数'] >= 0.06)
    condition &= (df['经营现金流量总负债比_分位数'] <= 0.99)
    
    df['归母EP(ttm)'] = 1 / df['归母PE(ttm)']
    df['归母EP(ttm)_二级行业分位数'] = df.groupby(['交易日期', '申万二级行业名称'])['归母EP(ttm)'].rank(ascending=True, pct=True)
    condition &= (df['归母EP(ttm)_二级行业分位数'] >= 0.03)
    condition &= (df['归母EP(ttm)_二级行业分位数'] <= 0.97)
    
    df['经营活动现金流入小计_分位数'] = df.groupby(['交易日期'])['经营活动现金流入小计'].rank(ascending=True, pct=True)
    condition &= (df['经营活动现金流入小计_分位数'] >= 0)
    condition &= (df['经营活动现金流入小计_分位数'] <= 0.8)

    # condition &= (df['中户买入占比_20avg'] >= 0.4)
    # condition &= (df['散户卖出占比_20avg'] >= 0.2)

    
    df = df[condition] # 综上所有财务因子的过滤条件，选股
    factors_rank_dict = { # 定义需要进行rank的因子
        '总市值': True,
    }
    merge_factor_list = [] # 定义合并需要的list
    for factor in factors_rank_dict: # 遍历factors_rank_dict进行排序
        df[factor + '_rank'] = df.groupby('交易日期')[factor].rank(ascending=factors_rank_dict[factor], method='first')
        merge_factor_list.append(factor + '_rank') # 将计算好的因子rank添加到list中
    df['因子'] = df[merge_factor_list].mean(axis=1) # 对量价因子进行等权合并，生成新的因子
    df['排名'] = df.groupby('交易日期')['因子'].rank(method='first') # 对因子进行排名
    # print(df[df['排名'] <= 6].tail(60))
    df = df[df['排名'] <= select_stock_num]  # 选取排名靠前的股票

    return df
# !!!
