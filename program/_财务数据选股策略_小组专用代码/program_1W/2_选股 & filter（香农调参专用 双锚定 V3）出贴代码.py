"""
作者：香农
"""
import datetime
from Evaluate import *
from Filter import *
from Functions import *
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数


def tj(equity, select_stock):
    results = pd.DataFrame()
    def num_to_pct(value): # 将数字转为百分数
        return '%.2f%%' % (value * 100)
    results.loc[0, '累积净值'] = round(equity['equity_curve'].iloc[-1], 2) # ===计算累积净值
    annual_return = (equity['equity_curve'].iloc[-1]) ** ('1 days 00:00:00' / (equity['交易日期'].iloc[-1] - equity['交易日期'].iloc[0]) * 365) - 1 # 计算年化收益
    results.loc[0, '年化收益'] = str(round(annual_return * 100, 2)) + '%'
    equity['max2here'] = equity['equity_curve'].expanding().max() # 最大回撤：计算当日之前的资金曲线的最高点
    equity['dd2here'] = equity['equity_curve'] / equity['max2here'] - 1 # 计算到历史最高值到当日的跌幅，drowdwon
    end_date, max_draw_down = tuple(equity.sort_values(by=['dd2here']).iloc[0][['交易日期', 'dd2here']]) # 计算最大回撤，以及最大回撤结束时间
    equity.drop(['max2here', 'dd2here'], axis=1, inplace=True)# 将无关的变量删除
    results.loc[0, '最大回撤'] = format(max_draw_down, '.2%')
    results.loc[0, '年化回撤比'] = round(annual_return / abs(max_draw_down), 2) # 年化回撤比
    return results


def ht(df, data_dict, date_col=None, right_axis=None, pic_size=[1500, 800], log=False, chg=False, title=None, path='./pic.html', show=True):
    draw_df = df.copy()
    if date_col: # 设置时间序列
        time_data = draw_df[date_col]
    else:
        time_data = draw_df.index

    fig = make_subplots(specs=[[{"secondary_y": True}]]) # 绘制左轴数据
    for key in data_dict:
        if chg:
            draw_df[data_dict[key]] = (draw_df[data_dict[key]] + 1).fillna(1).cumprod()
        fig.add_trace(go.Scatter(x=time_data, y=draw_df[data_dict[key]], name=key, ))

    if right_axis: # 绘制右轴数据
        # for key in list(right_axis.keys()):
        key = list(right_axis.keys())[0]
        fig.add_trace(go.Scatter(x=time_data, y=draw_df[right_axis[key]], name=key + '(右轴)', marker=dict(color='rgba(220, 220, 220, 0.8)'), yaxis='y2'))  # 标明设置一个不同于trace1的一个坐标轴
    fig.update_layout(template="none", width=pic_size[0], height=pic_size[1], title_text=title, hovermode='x')
    
    if log: # 是否转为log坐标系
        fig.update_layout(yaxis_type="log")
    plot(figure_or_data=fig, filename=path, auto_open=False)

    if show: # 打开图片的html文件，需要判断系统的类型
        res = os.system('start ' + path)
        if res != 0:
            os.system('open ' + path)


def elements(df,x,y): # 锚定指标：几何年化收益率
    # 去掉北交所，科创等股票
    df = df[~df['股票代码'].str.contains('sh68|bj')]

    df = df[df['下日_是否交易'] == 1]
    df = df[df['下日_开盘涨停'] == False]
    df = df[df['下日_是否ST'] == False]
    df = df[df['下日_是否退市'] == False]

    df = df[df['周五涨跌幅'] < 0.055]
    df = df[df['周五涨跌幅'] > -0.092]
    # condition = df['毛利率(ttm)'] > 0

    condition = (df['收盘价_复权'] > df['均线_250'] * 0.8)
    condition &= (df['收盘价_复权'] < df['均线_250'] * 1.2)
    condition &= (df['收盘价_复权'] >= df['周均线_20'])
    condition &= (df['收盘价_复权'] <= df['周均线_20'] * 1.12)

    condition &= (df['DIF'] >= x)
    condition &= (df['DIF'] <= y)
    condition &= (df['周_macd'] >= 0)
    condition &= (df['周_macd'] < 0.12)

    condition &= (df['5日累计涨跌幅'] < 0.06)
    condition &= (df['30日累计涨跌幅'] > -0.115)
    condition &= (df['30日累计涨跌幅'] <= 0.23)
    condition &= (df['10日累计涨跌幅'] > -0.39)
    condition &= (df['10日累计涨跌幅'] < 0.20)

    condition &= (df['均线_5']  > df['均线_34'] * 0.8)
    condition &= (df['均线_5']  < df['均线_34'] * 1.12)

    condition &= (df['MA34_斜率_5'] > 0)
    condition &= (df['MA34_斜率_10'] > 0)
    condition &= (df['MA34_斜率_20'] > 0)


    # condition &= (df['周五成交量'] < df['成交量_5'] * 0.8)

    # condition &= (df['MA60_斜率_20'] > 1)


    df = df[condition]

    # 定义需要进行rank的因子， 排序方式，True从小到大，False从大到小
    factors_rank_dict = [
        ('总市值', True, 1),
    ]
    ascending = True
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


# *************************************************** 主程序 ***************************************************
df1 = pd.read_pickle(root_path + '/data/output/选股策略/all_stock_data_%s.pkl' % period_type) # 导入数据，从pickle文件中读取整理好的所有股票数据
df1.dropna(subset=['下周期每天涨跌幅'], inplace=True)
index_data = import_index_data(root_path + '/data/index_data/sh000300.csv', back_trader_start=date_start, back_trader_end=date_end) # 导入指数数据
empty_df1 = create_empty_data(index_data, period_type) # 创造空的事件周期表，用于填充不选股的周期

df1 = df1[df1['上市至今交易天数'] > 250] # 删除新股
df1 = df1[df1['下日_是否交易'] == 1] # 删除下个交易日不交易
df1 = df1[df1['下日_开盘涨停'] == False] # 删除下个交易日开盘涨停的股票
df1 = df1[df1['下日_是否ST'] == False]
df1 = df1[df1['下日_是否退市'] == False]
all_re = pd.DataFrame()
all_re = pd.DataFrame(columns = ['x','y','累积净值','几何年化','最大回撤','年化回撤比'])
t1 = datetime.datetime.now()
for x in numpy.arange(0,1.01,0.05):
    for y in numpy.arange(x,1.01,0.05):
        if x < y:
            df = pd.DataFrame()
            df = df1.copy()
            empty_df = empty_df1.copy()
            df = elements(df, x, y) # 筛选股票
            
            df['下日_开盘买入涨跌幅'] = df['下日_开盘买入涨跌幅'].apply(lambda x: [x]) # 按照开盘买入的方式，修正选中股票在下周期每天的涨跌幅，即将下周期每天的涨跌幅中第一天的涨跌幅，改成由开盘买入的涨跌幅
            df['下周期每天涨跌幅'] = df['下周期每天涨跌幅'].apply(lambda x: x[1:])
            df['下周期每天涨跌幅'] = df['下日_开盘买入涨跌幅'] + df['下周期每天涨跌幅']
            # ===整理选中股票数据，挑选出选中股票
            df['股票代码'] += ' '
            df['股票名称'] += ' '
            group = pd.DataFrame()
            group = df.groupby('交易日期')
            select_stock = pd.DataFrame()
            select_stock['股票数量'] = group['股票名称'].size()
            select_stock['买入股票代码'] = group['股票代码'].sum()
            select_stock['买入股票名称'] = group['股票名称'].sum()
            #print(select_stock.tail())
            # 计算下周期每天的资金曲线
            select_stock['选股下周期每天资金曲线'] = group['下周期每天涨跌幅'].apply(lambda x: np.cumprod(np.array(list(x)) + 1, axis=1).mean(axis=0))
            select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'] * (1 - c_rate)  # 扣除买入手续费，计算有不精准的地方
            select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(x[:-1]) + [x[-1] * (1 - c_rate - t_rate)]) # 扣除卖出手续费、印花税。最后一天的资金曲线值，扣除印花税、手续费
            select_stock['选股下周期涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: x[-1] - 1) # 计算下周期整体涨跌幅
            select_stock['选股下周期每天涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(pd.DataFrame([1] + x).pct_change()[0].iloc[1:])) # 计算下周期每天的涨跌幅
            del select_stock['选股下周期每天资金曲线']
            empty_df.update(select_stock) # 将选股结果更新到empty_df上
            select_stock = empty_df
            select_stock.reset_index(inplace=True) # 计算整体资金曲线
            select_stock['资金曲线'] = (select_stock['选股下周期涨跌幅'] + 1).cumprod()
            #print(select_stock.tail())
            
            # 计算选中股票每天的资金曲线，计算每日资金曲线
            equity = pd.DataFrame()
            equity = pd.merge(left=index_data, right=select_stock[['交易日期', '买入股票代码']], on=['交易日期'],how='left', sort=True) # 将选股结果和大盘指数合并
            equity['持有股票代码'] = equity['买入股票代码'].shift()
            equity['持有股票代码'].fillna(method='ffill', inplace=True)
            equity.dropna(subset=['持有股票代码'], inplace=True)
            del equity['买入股票代码']
            equity['涨跌幅'] = select_stock['选股下周期每天涨跌幅'].sum()
            equity['equity_curve'] = (equity['涨跌幅'] + 1).cumprod()
            equity['benchmark'] = (equity['指数涨跌幅'] + 1).cumprod()
            
            
            jz = round(equity['equity_curve'].iloc[-1], 2) # 计算累积净值
            nh = (equity['equity_curve'].iloc[-1]) ** ('1 days 00:00:00' / (equity['交易日期'].iloc[-1] - equity['交易日期'].iloc[0]) * 365) - 1 # 计算年化收益
            equity['max2here'] = equity['equity_curve'].expanding().max() # 最大回撤：计算当日之前的资金曲线的最高点
            equity['dd2here'] = equity['equity_curve'] / equity['max2here'] - 1 # 计算到历史最高值到当日的跌幅，drowdwon
            end_date, hc = tuple(equity.sort_values(by=['dd2here']).iloc[0][['交易日期', 'dd2here']]) # 计算最大回撤，以及最大回撤结束时间
            re1 = {
                'x':x,
                'y':y,
                '累积净值':jz,
                '几何年化':format(nh,'.4f'),
                '最大回撤':format(-hc,'.4f'),
                '年化回撤比':format(- nh / hc,'.2f')
                }
            all_re = all_re.append(re1,ignore_index = True)

df2 = all_re.sort_values(by = ['年化回撤比','x','y'], ascending = [True,False,True]).tail(1)

bs1 = df2.iloc[0,0] - 0.05
be1 = df2.iloc[0,0] + 0.05

bs2 = df2.iloc[0,1] - 0.05
be2 = df2.iloc[0,1] + 0.05
if bs1 < 0:
    bs1 = 0
if be2 > 1:
    be2 = 1

for i in numpy.arange(bs1,be1,0.01):
    for j in numpy.arange(bs2,be2,0.01):
        if i < j:
            df = pd.DataFrame()
            df = df1.copy()
            empty_df = empty_df1.copy()
            df = elements(df, i, j) # 筛选股票
            
            df['下日_开盘买入涨跌幅'] = df['下日_开盘买入涨跌幅'].apply(lambda x: [x]) # 按照开盘买入的方式，修正选中股票在下周期每天的涨跌幅，即将下周期每天的涨跌幅中第一天的涨跌幅，改成由开盘买入的涨跌幅
            df['下周期每天涨跌幅'] = df['下周期每天涨跌幅'].apply(lambda x: x[1:])
            df['下周期每天涨跌幅'] = df['下日_开盘买入涨跌幅'] + df['下周期每天涨跌幅']
            # ===整理选中股票数据，挑选出选中股票
            df['股票代码'] += ' '
            df['股票名称'] += ' '
            group = pd.DataFrame()
            group = df.groupby('交易日期')
            select_stock = pd.DataFrame()
            select_stock['股票数量'] = group['股票名称'].size()
            select_stock['买入股票代码'] = group['股票代码'].sum()
            select_stock['买入股票名称'] = group['股票名称'].sum()
            #print(select_stock.tail())
            # 计算下周期每天的资金曲线
            select_stock['选股下周期每天资金曲线'] = group['下周期每天涨跌幅'].apply(lambda x: np.cumprod(np.array(list(x)) + 1, axis=1).mean(axis=0))
            select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'] * (1 - c_rate)  # 扣除买入手续费，计算有不精准的地方
            select_stock['选股下周期每天资金曲线'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(x[:-1]) + [x[-1] * (1 - c_rate - t_rate)]) # 扣除卖出手续费、印花税。最后一天的资金曲线值，扣除印花税、手续费
            select_stock['选股下周期涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: x[-1] - 1) # 计算下周期整体涨跌幅
            select_stock['选股下周期每天涨跌幅'] = select_stock['选股下周期每天资金曲线'].apply(lambda x: list(pd.DataFrame([1] + x).pct_change()[0].iloc[1:])) # 计算下周期每天的涨跌幅
            del select_stock['选股下周期每天资金曲线']
            empty_df.update(select_stock) # 将选股结果更新到empty_df上
            select_stock = empty_df
            select_stock.reset_index(inplace=True) # 计算整体资金曲线
            select_stock['资金曲线'] = (select_stock['选股下周期涨跌幅'] + 1).cumprod()
            #print(select_stock.tail())
            
            # 计算选中股票每天的资金曲线，计算每日资金曲线
            equity = pd.DataFrame()
            equity = pd.merge(left=index_data, right=select_stock[['交易日期', '买入股票代码']], on=['交易日期'],how='left', sort=True) # 将选股结果和大盘指数合并
            equity['持有股票代码'] = equity['买入股票代码'].shift()
            equity['持有股票代码'].fillna(method='ffill', inplace=True)
            equity.dropna(subset=['持有股票代码'], inplace=True)
            del equity['买入股票代码']
            equity['涨跌幅'] = select_stock['选股下周期每天涨跌幅'].sum()
            equity['equity_curve'] = (equity['涨跌幅'] + 1).cumprod()
            equity['benchmark'] = (equity['指数涨跌幅'] + 1).cumprod()
            
            jz = round(equity['equity_curve'].iloc[-1], 2) # 计算累积净值
            nh = (equity['equity_curve'].iloc[-1]) ** ('1 days 00:00:00' / (equity['交易日期'].iloc[-1] - equity['交易日期'].iloc[0]) * 365) - 1 # 计算年化收益
            equity['max2here'] = equity['equity_curve'].expanding().max() # 最大回撤：计算当日之前的资金曲线的最高点
            equity['dd2here'] = equity['equity_curve'] / equity['max2here'] - 1 # 计算到历史最高值到当日的跌幅，drowdwon
            end_date, hc = tuple(equity.sort_values(by=['dd2here']).iloc[0][['交易日期', 'dd2here']]) # 计算最大回撤，以及最大回撤结束时间
            re1 = {
                'x':i,
                'y':j,
                '累积净值':jz,
                '几何年化':format(nh,'.4f'),
                '最大回撤':format(-hc,'.4f'),
                '年化回撤比':format(- nh / hc,'.2f')
                }
            all_re = all_re.append(re1,ignore_index = True)
            
all_re.fillna(value='0', inplace = True)
all_re.to_csv(f"/Users/lishechuan/python/coincock/data/枚举清单.csv", encoding = 'gbk', index = False)
print(all_re)
print(f"\n最佳回撤比：\n{all_re.sort_values(by = ['年化回撤比','x','y'], ascending = [True,False,True]).tail(1)}")
print(f"\n最佳年化：\n{all_re.sort_values(by = ['几何年化','x','y'], ascending = [True,False,True]).tail(1)}")

ht(all_re, data_dict={'收益': '几何年化','回撤': '最大回撤','比率': '年化回撤比'}, date_col='x')
t2 = datetime.datetime.now()
print(f"\n********** 全部完成 **********\n开始时间：{str(t1)[:-7]}\n结束时间：{str(t2)[:-7]}\n合计耗时：{str(t2-t1)[:-7]}")
