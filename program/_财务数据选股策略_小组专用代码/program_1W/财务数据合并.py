"""
创建者：香农
********** V1 更新内容 20220629 **********
1、重构并行/串行合并邢不行财务数据代码
"""
import os
import datetime
import pandas as pd
import platform
from multiprocessing import Pool, freeze_support, cpu_count
from joblib import Parallel, delayed
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore")
pd.set_option('expand_frame_repr', False)  # 当列太多时不换行
pd.set_option('display.max_rows', 8000)  # 最多显示数据的行数
pd.set_option('display.unicode.ambiguous_as_wide', True) # 设置命令行输出时的列对齐功能
pd.set_option('display.unicode.east_asian_width', True)

# *************************************************** 设置参数 ***************************************************
author = '香农'
old_folder = '/Users/lishechuan/python/coincock/program/_财务数据选股策略_小组专用代码/data/fin_data/fin_xbx'
new_folder = '/Users/lishechuan/python/coincock/program/_财务数据选股策略_小组专用代码/data/fin_data/fin_xbx增量财务' # 需固定文件夹名为老文件夹名+“增量财务”，代码中会有响应转换处理逻辑
col = 'publish_date' # 指定筛选的列（财务数据按照更新时间筛选，日线数据根据交易日期筛选）
multiply_process = False  # True为并行，False为串行

# *************************************************** 自定函数 ***************************************************
def creat_repeat_list(path): # 生成股票代码列表
    stock_list = []
    repeat_list = [] # 多个文件的列表
    for root, dirs, files in os.walk(path): # os遍历文件夹中的所有文件
        if files:  # 当files不为空的时候
            for f in files:
                if f.endswith('.csv'):
                    if f[:8] in stock_list:
                        repeat_list.append(f[:8])
                    else:
                        stock_list.append(f[:8])
    return sorted(repeat_list)


def creat_path_list(path): # 导入某文件夹下所有股票的代码
    path_list = []
    for root, dirs, files in os.walk(path): # os遍历文件夹中的所有文件
        if files:  # 当files不为空的时候
            for f in files:
                if f.endswith('.csv'):
                    path_list.append(os.path.join(root, f))
    return sorted(path_list)


def update_data(path, col):
    new_df = pd.read_csv(path, skiprows = 1, parse_dates = [col], encoding = 'gbk')  # 读取增量数据
    if not new_df.empty:
        old_path = path.replace('增量财务', '')  # 用增量路径转换为存量路径
        if os.path.exists(old_path):
            old_df = pd.read_csv(old_path, skiprows = 1, parse_dates = [col], encoding = 'gbk')
            all_df = pd.concat([old_df, new_df])
            all_df.drop_duplicates(subset = ['report_date','publish_date'], keep = 'first', inplace = True)
            all_df.sort_values(by = ['publish_date','report_date'], inplace = True)
            if len(all_df) - len(old_df) != 0:
                pd.DataFrame(columns = [f'数据由{author}整理']).to_csv(old_path, index = False, encoding = 'gbk')
                all_df.to_csv(old_path, mode = 'a', index = False, encoding = 'gbk') # 保存的文件不含索引列
        else:
            file_name = os.path.basename(path)  # 根据路径获取文件名
            folder_path = old_path.split(file_name)[0]
            if not os.path.exists(folder_path):  # 如果文件夹不存在
                os.mkdir(folder_path)  # 创建文件夹
            pd.DataFrame(columns = [f'数据由{author}整理']).to_csv(old_path, index = False, encoding = 'gbk')
            new_df.to_csv(old_path, mode = 'a', index = False, encoding = 'gbk')

# *************************************************** 主体程序 ***************************************************
if __name__ == '__main__':
    t1 = datetime.datetime.now()
    
    old_repeat_list = creat_repeat_list(old_folder)
    new_repeat_list = creat_repeat_list(new_folder)
    old_path_list = creat_path_list(old_folder)
    new_path_list = creat_path_list(new_folder)
    #new_path_list = new_path_list[0:3] # 用来调试
    print('存量股票数:', len(old_path_list) - len(old_repeat_list), '存在多文件个股：', old_repeat_list)
    print('增量股票数:', len(new_path_list) - len(new_repeat_list), '存在多文件个股：', new_repeat_list)
    
    if 'Windows' in platform.platform(): # 添加对windows多进程的支持
        freeze_support()
    if multiply_process: # 并行更新
        with Pool(max(cpu_count() - 1, 1)) as pool:
            Parallel(n_jobs = cpu_count() - 1)(delayed(update_data)(path, col) for path in tqdm(new_path_list)) # 适用spyder
    else: # 串行更新
        for path in new_path_list:
            update_data(path, col)

t2 = datetime.datetime.now()
print(f"\n********** 全部完成 **********\n开始时间：{str(t1)[:-7]}\n结束时间：{str(t2)[:-7]}\n合计耗时：{str(t2-t1)[:-7]}")

