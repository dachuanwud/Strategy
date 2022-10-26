# 简单移动平均线策略
def simple_moving_average_signal(df, para=[20, 120]):
    """
    简单的移动平均线策略。只能做多。
    当短期均线上穿长期均线的时候，做多，当短期均线下穿长期均线的时候，平仓
    :param df:
    :param para: ma_short, ma_long
    :return: 最终输出的df中，新增字段：signal，记录发出的交易信号
    """

    # ===策略参数
    ma_short = para[0]  # 短期均线。ma代表：moving_average
    ma_long = para[1]  # 长期均线

    # ===计算均线。所有的指标，都要使用复权价格进行计算。
    df['ma_short'] = df['收盘价_复权'].rolling(ma_short, min_periods=1).mean()
    df['ma_long'] = df['收盘价_复权'].rolling(ma_long, min_periods=1).mean()

    # ===找出做多信号
    condition1 = df['ma_short'] > df['ma_long']  # 短期均线 > 长期均线
    condition2 = df['ma_short'].shift(1) <= df['ma_long'].shift(1)  # 上一周期的短期均线 <= 长期均线
    df.loc[condition1 & condition2, 'signal'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # ===找出做多平仓信号
    condition1 = df['ma_short'] < df['ma_long']  # 短期均线 < 长期均线
    condition2 = df['ma_short'].shift(1) >= df['ma_long'].shift(1)  # 上一周期的短期均线 >= 长期均线
    df.loc[condition1 & condition2, 'signal'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===删除无关中间变量
    # df.drop(['ma_short', 'ma_long'], axis=1, inplace=True)

    return df


# 简单移动平均线策略
def boll_timing_signal(df, period = 21):
    """
    简单的移动平均线策略。只能做多。
    当短期均线上穿长期均线的时候，做多，当短期均线下穿长期均线的时候，平仓
    :param df:
    :param para: ma_short, ma_long
    :return: 最终输出的df中，新增字段：signal，记录发出的交易信号
    """
    mid_name = f'boll_{period}_mid'
    up_name = f'boll_{period}_up'
    down_name = f'boll_{period}_down'
    df[mid_name] = df['收盘价_复权'].rolling(period, min_periods=1).mean()
    df['std'] = df['收盘价_复权'].rolling(period, min_periods=1).std(ddof=0)

    df[up_name] = df[mid_name] + df['std'] * 2
    df[down_name] = df[mid_name] - df['std'] * 2

    # ===站上下轨买入
    condition1 = df[down_name] < df['收盘价_复权']
    condition2 = df[down_name].shift(1) >= df['收盘价_复权'].shift(1)
    df.loc[condition1 & condition2, 'signal'] = 1  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===上轨突破回踩 或者 破下轨,卖出
    condition1 = df[up_name] > df['收盘价_复权'] # 短期均线 > 长期均线
    condition2 = df[up_name].shift(1) < df['收盘价_复权'].shift(1)  # 上一周期的短期均线 <= 长期均线
    condition3 = df[down_name] > df['收盘价_复权']
    condition4 = df[down_name].shift(1) <= df['收盘价_复权'].shift(1)
    df.loc[(condition1 & condition2) | (condition3 & condition4), 'signal'] = 0

    return df

def simple_always_buy_signal(df):
    df['signal'] = 1
    return df

def select_stock_position(df, extra_agg_dict={}):
    """
    signal是收盘发生信号的日期。
    pos是实际交易的日期。
    :param df:
    :param para: ma_short, ma_long
    :return: 最终输出的df中，新增字段：signal，记录发出的交易信号
    """
    # 计算pos
    df['signal'].fillna(method='ffill', inplace=True)
    df['signal'].fillna(value=1, inplace=True)
    df['pos'] = df['signal'].shift(1)
    df['pos'].fillna(value=1, inplace=True)

    df['涨跌幅_择时'] = df['涨跌幅']
    df.loc[df['pos'] == 0, '涨跌幅_择时'] = 0

    # 用于计算每个周期首日涨跌幅
    extra_agg_dict['pos'] = 'last'

    return df


def timing_strategy_process(df, extra_agg_dict={}):
    #df = simple_moving_average_signal(df, para=[5, 22])
    df = boll_timing_signal(df, period=21)
    # df = simple_always_buy_signal(df)
    df = select_stock_position(df, extra_agg_dict)
    return df