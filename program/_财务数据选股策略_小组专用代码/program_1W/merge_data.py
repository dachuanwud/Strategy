"""
目的：将日线更新包的数据覆盖到完整数据中

读取更新包解压后所在目录
将数据逐行写入完整数据文件

"""
import shutil
import time
import chardet

import pandas as pd
from pathlib import Path
from multiprocessing import Pool, cpu_count

pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 5000)  # 最多显示数据的行数
# 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.ambiguous_as_wide', True)
pd.set_option('display.unicode.east_asian_width', True)

# 股票所在根目录
path_stock = Path.cwd().parent / 'data' / 'daily_data' / 'stock'
# 更新包所在目录
path_update = path_stock.parent.parent.parent.parent.parent.parent.parent / 'Downloads' / 'stock'

print(path_stock)
print(path_update)

start_time = time.time()
slogan_xbx = '数据由邢不行整理，对数据字段有疑问的，可以直接微信私信邢不行，微信号：xbx297'


def count_run_time(start_t):
    # 时间处理
    # https://blog.csdn.net/chichoxian/article/details/53108365
    # https://www.waynerv.com/posts/differences-bettween-time-and-datetime-in-python/

    end_t = time.time()
    diff_time = end_t - start_t

    # zs, xs = str(diff_time).split('.')
    zs = str(diff_time).split('.')[0]
    xs = str(diff_time).split('.')[1][:5]

    m, s = divmod(int(zs), 60)
    h, m = divmod(m, 60)

    print("\n%02d:%02d:%02d.%05d" % (h, m, s, int(xs)))


def reset_index_from_trade_date(df):
    df.reset_index(inplace=True)
    td_col = df["index"]
    df.drop('index', axis=1, inplace=True)
    df.insert(2, '交易日期', td_col)


def drop_same_date_data(date, df, df_son):
    if df_son.index == date:
        # 去掉同一天的原数据
        df.drop(labels=date, inplace=True)


def merge_df_slow(stock_update, stock_path):
    df_update = pd.read_csv(stock_update, skiprows=1, encoding='gbk', index_col='交易日期')

    for i, data_update in df_update.iterrows():
        # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.read_csv.html
        # df_stock = pd.read_csv(stock_path, skiprows=1, on_bad_lines='skip', encoding='gbk', index_col='交易日期')
        df_stock = pd.read_csv(stock_path, skiprows=1, encoding='gbk', index_col='交易日期')

        df_stock.drop_duplicates(inplace=True)  # 数据去重，防止后续出错

        # 需要更新的日期
        date_of_update = data_update.name
        data_update = pd.DataFrame(data_update.T)
        df_append = data_update.T

        # 更新日期之后的所有数据, 其实这个会包含更新日期当天
        following_data = df_stock.truncate(before=date_of_update)

        if following_data.empty:
            # 此日期之后无数据，则可以直接追加数据到最后一行
            reset_index_from_trade_date(df_append)
            df_append.to_csv(stock_path, index=False, header=False, mode='a', encoding='gbk')
            continue
        f_head = following_data.head(1)
        drop_same_date_data(date_of_update, following_data, f_head)

        # 此日期之前的所有数据
        previous_data = df_stock.truncate(after=date_of_update)
        p_tail = previous_data.tail(1)
        drop_same_date_data(date_of_update, previous_data, p_tail)

        df_new = pd.concat([previous_data, df_append, following_data])
        reset_index_from_trade_date(df_new)

        pd.DataFrame(columns=[slogan_xbx]).to_csv(stock_path, index=False, encoding='gbk')
        df_new.to_csv(stock_path, index=False, mode='a', encoding='gbk')


def merge_df_fast(stock_update, stock_path):
    df_update = pd.read_csv(stock_update, skiprows=1, encoding='gbk', engine='python')
    df_stock = pd.read_csv(stock_path, skiprows=1, encoding='gbk', engine='python')

    df_new = df_stock.append(df_update)
    df_new.sort_values('交易日期', inplace=True)
    df_new.drop_duplicates(subset='交易日期', keep='last', inplace=True)

    pd.DataFrame(columns=[slogan_xbx]).to_csv(stock_path, index=False, encoding='gbk')
    df_new.to_csv(stock_path, index=False, mode='a', encoding='gbk')


def data_merge_with_stock_path(stock_update):
    # 判断file_update是否为文件
    if Path.is_file(stock_update):
        # 获取文件名含后缀
        file_name = stock_update.name
        # 组成原数据路径
        stock_path = path_stock / file_name

        if Path.exists(stock_path):
            if config == 1:
                merge_df_fast(stock_update, stock_path)
            else:
                merge_df_slow(stock_update, stock_path)
        else:
            print("--新股 {}, 直接复制--".format(stock_update.stem))  # .stem 获取不含后缀文件名
            shutil.copy(stock_update, stock_path)

        print("\r", stock_update.stem + '搞定', end="", flush=True)
        # https://blog.csdn.net/qq_35975447/article/details/88072657
        # break   # test
    else:
        print("不是文件")
        exit()

    return 1


# 获取所有待更新股票代码,
def get_code_list_for_update(stock_update_path):
    stock_list = []

    for idx, stock_update in enumerate(Path.iterdir(stock_update_path), 0):
        if Path.is_file(stock_update) & (stock_update.suffix == '.csv'):
            stock_list.append(stock_update)
    print(len(stock_list))
    return stock_list


def data_merge():
    if multi is True:
        stock_list = get_code_list_for_update(path_update)
        with Pool(max(cpu_count() - 2, 1)) as pool:
            pool.map(data_merge_with_stock_path, sorted(stock_list))
    else:
        for idx, stock_update in enumerate(Path.iterdir(path_update), 1):  # 计数从1开始
            # print(idx,stock_update)
            data_merge_with_stock_path(stock_update)


# config: 1 fast, 2 slow
config = 1
multi = True

if __name__ == '__main__':
    data_merge()

    count_run_time(start_time)
