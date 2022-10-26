"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

财务数据选股专属代码

数据整理需要计算的因子脚本，可以在这里修改/添加别的因子计算
"""
import talib as ta

# !!!
def cal_macd(df, extra_agg_dict):
    df['macd'], df['macdsignal'], df['macdhist'] = ta.MACD(df['收盘价_复权'], fastperiod=12, slowperiod=26, signalperiod=9)
    extra_agg_dict['macd'] = 'last'
    extra_agg_dict['macdsignal'] = 'last'
    extra_agg_dict['macdhist'] = 'last'
    return df

def cal_sma(df, extra_agg_dict):
    df["SMA10"] = ta.SMA(df['收盘价_复权'], timeperiod=10)
    df["SMA20"] = ta.SMA(df['收盘价_复权'], timeperiod=20)
    df["SMA30"] = ta.SMA(df['收盘价_复权'], timeperiod=30)
    extra_agg_dict['SMA10'] = 'last'
    extra_agg_dict['SMA20'] = 'last'
    extra_agg_dict['SMA30'] = 'last'
    return df

def cal_rsi(df, extra_agg_dict):
    df["rsi"] = ta.RSI(df['收盘价_复权'], timeperiod=14)
    extra_agg_dict['rsi'] = 'last'
    return df

def cal_boll(df, extra_agg_dict):
    df['boll_upper'], df['boll_middle'], df['boll_lower'] = ta.BBANDS(
        df['收盘价_复权'],
        timeperiod=20,
        # number of non-biased standard deviations from the mean
        nbdevup=2,
        nbdevdn=2,
        # Moving average type: simple moving average here
        matype=0)
    extra_agg_dict['boll_upper'], extra_agg_dict['boll_middle'], extra_agg_dict['boll_lower'] = 'last', 'last', 'last'
    return df

def cal_obv(df, extra_agg_dict):
    df['obv'] = ta.OBV(df['收盘价_复权'], df['成交量'])
    extra_agg_dict['obv'] = 'last'
    return df

def cal_kdj(df, extra_agg_dict):
    df['slowk'], df['slowd'] = ta.STOCH(df['最高价_复权'],
                                        df['最低价_复权'],
                                        df['收盘价_复权'],
                                        fastk_period=9,
                                        slowk_period=3,
                                        slowk_matype=0,
                                        slowd_period=3,
                                        slowd_matype=0)
    extra_agg_dict['slowk'] = 'last'
    extra_agg_dict['slowd'] = 'last'
    return df


def cal_tech_factor(df, extra_agg_dict):  # 计算量价因子及技术指标
    """
    计算量价因子及技术指标
    :param df:
    :param extra_agg_dict: 数据处理方式
    :return:
    """
    # =计算均价
    df['VWAP'] = df['成交额'] / df['成交量']
    extra_agg_dict['VWAP'] = 'last'

    df['5VWAP'] = df['VWAP'].rolling(5).mean()
    extra_agg_dict['5VWAP'] = 'last'

    df['10VWAP'] = df['VWAP'].rolling(10).mean()
    extra_agg_dict['10VWAP'] = 'last'

    # =计算换手率
    df['换手率'] = df['成交额'] / df['流通市值']
    extra_agg_dict['换手率'] = 'sum'

    df['换手率_5avg'] = df['换手率'].rolling(5).mean()
    extra_agg_dict['换手率_5avg'] = 'last'

    df['换手率_20avg'] = df['换手率'].rolling(20).mean()
    extra_agg_dict['换手率_20avg'] = 'last'

    # =计算均线
    df['5日均线'] = df['收盘价_复权'].rolling(5).mean()
    extra_agg_dict['5日均线'] = 'last'

    df['10日均线'] = df['收盘价_复权'].rolling(10).mean()
    extra_agg_dict['10日均线'] = 'last'

    df['13日均线'] = df['收盘价_复权'].rolling(13).mean()
    extra_agg_dict['13日均线'] = 'last'

    df['20日均线'] = df['收盘价_复权'].rolling(20).mean()
    extra_agg_dict['20日均线'] = 'last'

    df['30日均线'] = df['收盘价_复权'].rolling(30).mean()
    extra_agg_dict['30日均线'] = 'last'

    df['60日均线'] = df['收盘价_复权'].rolling(60).mean()
    extra_agg_dict['60日均线'] = 'last'

    df['90日均线'] = df['收盘价_复权'].rolling(90).mean()
    extra_agg_dict['90日均线'] = 'last'

    df['120日均线'] = df['收盘价_复权'].rolling(120).mean()
    extra_agg_dict['120日均线'] = 'last'

    df['200日均线'] = df['收盘价_复权'].rolling(200).mean()
    extra_agg_dict['200日均线'] = 'last'

    df['250日均线'] = df['收盘价_复权'].rolling(250).mean()
    extra_agg_dict['250日均线'] = 'last'

    # =计算bias
    df['bias'] = df['收盘价_复权'] / df['5日均线'] - 1
    extra_agg_dict['bias'] = 'last'

    df['bias_10'] = df['收盘价_复权'] / df['10日均线'] - 1
    extra_agg_dict['bias_10'] = 'last'

    df['bias_20'] = df['收盘价_复权'] / df['20日均线'] - 1
    extra_agg_dict['bias_20'] = 'last'

    df['bias_30'] = df['收盘价_复权'] / df['30日均线'] - 1
    extra_agg_dict['bias_30'] = 'last'

    df['bias_60'] = df['收盘价_复权'] / df['60日均线'] - 1
    extra_agg_dict['bias_60'] = 'last'

    df['bias_90'] = df['收盘价_复权'] / df['90日均线'] - 1
    extra_agg_dict['bias_90'] = 'last'

    df['bias_200'] = df['收盘价_复权'] / df['200日均线'] - 1
    extra_agg_dict['bias_200'] = 'last'

    # =计算累计涨跌幅
    df['3日累计涨跌幅'] = df['收盘价_复权'].pct_change(3)
    extra_agg_dict['3日累计涨跌幅'] = 'last'

    df['5日累计涨跌幅'] = df['收盘价_复权'].pct_change(5)
    extra_agg_dict['5日累计涨跌幅'] = 'last'

    df['7日累计涨跌幅'] = df['收盘价_复权'].pct_change(7)
    extra_agg_dict['7日累计涨跌幅'] = 'last'

    df['8日累计涨跌幅'] = df['收盘价_复权'].pct_change(8)
    extra_agg_dict['8日累计涨跌幅'] = 'last'

    df['10日累计涨跌幅'] = df['收盘价_复权'].pct_change(10)
    extra_agg_dict['10日累计涨跌幅'] = 'last'

    df['20日累计涨跌幅'] = df['收盘价_复权'].pct_change(20)
    extra_agg_dict['20日累计涨跌幅'] = 'last'

    df['30日累计涨跌幅'] = df['收盘价_复权'].pct_change(30)
    extra_agg_dict['30日累计涨跌幅'] = 'last'

    df['60日累计涨跌幅'] = df['收盘价_复权'].pct_change(60)
    extra_agg_dict['60日累计涨跌幅'] = 'last'

    df['90日累计涨跌幅'] = df['收盘价_复权'].pct_change(90)
    extra_agg_dict['90日累计涨跌幅'] = 'last'

    df['120日累计涨跌幅'] = df['收盘价_复权'].pct_change(120)
    extra_agg_dict['120日累计涨跌幅'] = 'last'

    df['250日累计涨跌幅'] = df['收盘价_复权'].pct_change(250)
    extra_agg_dict['250日累计涨跌幅'] = 'last'

    # 计算资金流
    df['中户买入占比'] = df['中户资金买入额'] * 10000 / df['成交额']
    extra_agg_dict['中户买入占比'] = 'last'

    df['中户买入占比_5avg'] = df['中户买入占比'].rolling(5).mean()
    extra_agg_dict['中户买入占比_5avg'] = 'last'

    df['中户买入占比_20avg'] = df['中户买入占比'].rolling(20).mean()
    extra_agg_dict['中户买入占比_20avg'] = 'last'

    df['散户卖出占比'] = df['散户资金卖出额'] / (
                df['散户资金卖出额'] + df['中户资金卖出额'] + df['大户资金卖出额'] + df['机构资金卖出额'])
    extra_agg_dict['散户卖出占比'] = 'last'

    df['散户卖出占比_5avg'] = df['散户卖出占比'].rolling(5).mean()
    extra_agg_dict['散户卖出占比_5avg'] = 'last'

    df['散户卖出占比_20avg'] = df['散户卖出占比'].rolling(20).mean()
    extra_agg_dict['散户卖出占比_20avg'] = 'last'

    df["rsi"] = ta.RSI(df['收盘价_复权'], timeperiod=14)
    extra_agg_dict['rsi'] = 'last'

    # 计算技术指标
    df = cal_macd(df, extra_agg_dict)
    df = cal_kdj(df, extra_agg_dict)
    df = cal_rsi(df, extra_agg_dict)
    df = cal_obv(df, extra_agg_dict)
    df = cal_boll(df, extra_agg_dict)

    return df


def calc_fin_factor(df, extra_agg_dict):  # 计算财务因子
    """
    计算财务因子
    :param df:              原始数据
    :param extra_agg_dict:  resample需要用到的
    :return:
    """
    # ===计算企业倍数指标：EV2 / EBITDA
    """
    EV2 = 总市值 + 有息负债 - 货币资金, 
    # EBITDA税息折旧及摊销前利润
    EBITDA = 营业总收入-营业税金及附加-营业成本+利息支出+手续费及佣金支出+销售费用+管理费用+研发费用+坏账损失+存货跌价损失+固定资产折旧、油气资产折耗、生产性生物资产折旧+无形资产摊销+长期待摊费用摊销+其他收益
    """
    # 有息负债 = 短期借款 + 长期借款 + 应付债券 + 一年内到期的非流动负债
    df['有息负债'] = df[
        ['B_st_borrow@xbx', 'B_lt_loan@xbx', 'B_bond_payable@xbx', 'B_noncurrent_liab_due_in1y@xbx']].sum(axis=1)
    df['EV2'] = df['总市值'] + df['有息负债'] - df['B_currency_fund@xbx'].fillna(0)  # 计算EV2

    # 计算EBITDA，坏账损失 字段无法直接从财报中获取，暂去除不计
    df['EBITDA'] = df[[
        'R_operating_total_revenue@xbx',  # 营业总收入
        'B_interest_payable@xbx',  # 负债应付利息
        'B_charge_and_commi_payable@xbx',  # 应付手续费及佣金

        'R_sales_fee@xbx',  # 销售费用
        'R_manage_fee@xbx',  # 管理费用
        'R_rad_cost_sum@xbx',  # 研发费用
        'R_asset_impairment_loss@xbx',  # 资产减值损失

        'C_depreciation_etc@xbx',  # 固定资产折旧、油气资产折耗、生产性生物资产折旧
        'C_intangible_assets_amortized@xbx',  # 无形资产摊销
        'C_lt_deferred_expenses_amrtzt@xbx',  # 长期待摊费用摊销

        'R_other_compre_income@xbx',  # 其他综合利益
        'B_total_current_liab@xbx',  # 流动负债合计
        'B_total_noncurrent_liab@xbx',  # 非流动负债合计
    ]].sum(axis=1) - df[['R_operating_taxes_and_surcharge@xbx',  # 税金及附加
                         'R_operating_cost@xbx',  # 营业成本
                         ]].sum(axis=1)
    df['企业倍数'] = df['EV2'] / df['EBITDA']  # 计算企业倍数
    extra_agg_dict['企业倍数'] = 'last'

    # ====计算常规的财务指标
    # 计算归母PE
    # 归母PE = 总市值 / 归母净利润(ttm)
    df['归母PE(ttm)'] = df['总市值'] / df['R_np_atoopc@xbx_ttm']
    extra_agg_dict['归母PE(ttm)'] = 'last'

    # =市销率 = 总市值 / 主营业务收入
    # 'R_revenue@xbx_ttm'报错
    df['ps_ttm'] = df['总市值'] / df['R_revenue@xbx_ttm']
    extra_agg_dict['ps_ttm'] = 'last'

    df['归母PE(ttm)比120'] = df['归母PE(ttm)'] / df['120日均线']
    extra_agg_dict['归母PE(ttm)比120'] = 'last'

    # 计算归母净利润率
    df['归母净利润率(ttm)'] = df['R_np_atoopc@xbx_ttm'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['归母净利润率(ttm)'] = 'last'

    # 计算归母ROE
    # 归母ROE(ttm) = 归母净利润(ttm) / 归属于母公司股东权益合计
    df['归母ROE(ttm)'] = df['R_np_atoopc@xbx_ttm'] / df['B_total_equity_atoopc@xbx']
    extra_agg_dict['归母ROE(ttm)'] = 'last'

    df['归母ROE比120'] = df['归母ROE(ttm)'] / df['120日均线']
    extra_agg_dict['归母ROE比120'] = 'last'

    df['净利润_TTM同比'] = df['R_np@xbx_ttm同比']
    extra_agg_dict['净利润_TTM同比'] = 'last'

    # 新增ROE历史平均
    df['ROE_AVG'] = df['归母ROE(ttm)'].rolling(600).mean()
    df['ROE_R'] = df['归母ROE(ttm)'] / df['ROE_AVG']
    extra_agg_dict['ROE_R'] = 'last'

    # 计算市净率倒数
    # 市净率倒数 = 归属于母公司股东权益合计 / 总市值
    df['BP'] = df['B_total_equity_atoopc@xbx'] / df['总市值']
    extra_agg_dict['BP'] = 'last'

    # 计算息税前利润EBIT
    # 息税前利润EBIT = 归母净利润 + 利息费用 + 所得税
    df['EBIT'] = df['R_np_atoopc@xbx'] + df['R_interest_fee@xbx'] + df['R_income_tax_cost@xbx']
    # 计算EV(企业价值)= 总市值 + 其他权益工具 + 少数股东权益+ 带息负债
    df['EV'] = df['总市值'] + df['B_other_equity_instruments@xbx'].fillna(0) + df['B_minority_equity@xbx'] + df[
        '有息负债']
    # 计算EY(股票收益率）= 息税前利润 / 企业价值
    df['EY'] = df['EBIT'] / df['EV']
    extra_agg_dict['EY'] = 'last'

    # ROC总资产收益率= 息税前利润 / （净营运资本 + 固定资产）
    # 净营运资本 = 应收账款 + 其他应收款* + 预付账款 + 存货 + 长期股权投资 + 投资性房地产 - 无息流动负债(应付账款 + 预收帐款 + 应付职工薪酬 + 应付税费 + 其他应付款* + (预提费用) + 递延收益流动负债 + 其他流动负债)
    df['净营运资本'] = df[['B_account_receivable@xbx',
                           'B_other_receivables@xbx',
                           'B_prepays@xbx',
                           'B_inventory@xbx',
                           'B_lt_equity_invest@xbx',
                           'B_invest_property@xbx'
                           ]].sum(axis=1) - df[['B_accounts_payable@xbx',
                                                'B_advance_payment@xbx',
                                                'B_payroll_payable@xbx',
                                                'B_tax_payable@xbx',
                                                'B_other_payables_sum@xbx',
                                                'B_differed_incomencl@xbx',
                                                'B_other_current_liab@xbx'
                                                ]].sum(axis=1)
    df['ROC'] = df['EY'] / (df['净营运资本'] + df['B_fixed_asset@xbx'])
    extra_agg_dict['ROC'] = 'last'

    # 计算毛利率ttm
    # 'R_operating_total_cost@xbx_ttm'报错
    # 毛利率(ttm) = ( 营业总收入_ttm - 营业总成本_ttm ) / 营业总收入_ttm
    df['毛利率(ttm)'] = 1 - df['R_operating_total_cost@xbx_ttm'] / df['R_operating_total_revenue@xbx_ttm']
    extra_agg_dict['毛利率(ttm)'] = 'last'

    # 计算净资产负债率
    # 净资产负债率 = 负债合计 / 归属于母公司股东权益合计
    df['净资产负债率'] = df['B_total_liab@xbx'] / df['B_total_equity_atoopc@xbx']
    extra_agg_dict['净资产负债率'] = 'last'

    # =计算总负债比
    # 财务数据中没有'总负债'和'总资产'
    df['总负债比'] = df['总负债'] / df['总资产']
    extra_agg_dict['总负债比'] = 'last'

    # 存货周转
    # 存货周转 = 365 * 流动资产的存货 / (营业总成本 - 资产减值损失)
    df['存货周转'] = 365 * df['B_inventory@xbx'] / (
                df['R_operating_total_cost@xbx'] - df['R_asset_impairment_loss@xbx'])
    extra_agg_dict['存货周转'] = 'last'

    #  存货周转率 = 营业成本 / 存货 高 false
    df['存货周转率'] = df['R_operating_cost@xbx'] / df['B_inventory@xbx']
    extra_agg_dict['存货周转率'] = 'last'

    # 投资占比:投资支出/营业总收入
    df['投资占比'] = df['C_invest_paid_cash@xbx'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['投资占比'] = 'last'

    # 'C_sub_total_of_ci_from_oa@xbx'报错
    df['经营活动现金流入小计'] = df['C_sub_total_of_ci_from_oa@xbx']
    extra_agg_dict['经营活动现金流入小计'] = 'last'

    # 'C_sub_total_of_cos_from_oa@xbx'报错
    df['经营活动现金流出小计'] = df['C_sub_total_of_cos_from_oa@xbx']
    extra_agg_dict['经营活动现金流出小计'] = 'last'

    # 'C_sub_total_of_ci_from_oa@xbx'报错
    df['经营活动现金流比率'] = df['C_sub_total_of_ci_from_oa@xbx'] / df['C_sub_total_of_cos_from_oa@xbx']

    # 计算现金流负债比
    # 现金流负债比 = 现金流量净额(经营活动) / 总负债(流动负债合计 + 非流动负债合计)
    df['现金流负债比'] = df['C_ncf_from_oa@xbx'] / (df['B_total_current_liab@xbx'] + df['B_total_noncurrent_liab@xbx'])
    extra_agg_dict['现金流负债比'] = 'last'

    # 新增
    # 'C_ncf_from_oa_im@xbx'报错
    # 计算净利润现金含量
    df['T'] = df['R_income_tax_cost@xbx'] / df['R_total_profit@xbx']
    df['净利润现金含量'] = df['C_ncf_from_oa_im@xbx'] * (1 - df['T']) / df['R_np@xbx_ttm']
    extra_agg_dict['净利润现金含量'] = 'last'

    df['经营现金流量总负债比'] = df['C_ncf_from_oa@xbx'] / df['B_total_liab@xbx']
    extra_agg_dict['经营现金流量总负债比'] = 'last'

    # 计算流动比率
    df['流动比率'] = df['B_total_current_assets@xbx'] / df['B_total_current_liab@xbx']
    extra_agg_dict['流动比率'] = 'last'

    # 计算速动比率
    df['速动比率'] = (df['B_total_current_assets@xbx'] - df['B_inventory@xbx']) / df['B_total_current_liab@xbx']
    extra_agg_dict['速动比率'] = 'last'

    # 营收含金量：经营净现金流/营总收
    df['营收含金量'] = df['C_ncf_from_oa@xbx'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['营收含金量'] = 'last'

    # 计算主营业务收入市值比Ty
    df['主营业务收入市值比'] = df['R_revenue@xbx'] / df['总市值']
    extra_agg_dict['主营业务收入市值比'] = 'last'

    return df
# !!!
