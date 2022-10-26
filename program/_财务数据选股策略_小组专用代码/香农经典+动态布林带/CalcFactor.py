# !!!
def cal_tech_factor(df, extra_agg_dict):
    # =计算均价
    df['VWAP'] = df['成交额'] / df['成交量']
    extra_agg_dict['VWAP'] = 'last'


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

    df['120日均线'] = df['收盘价_复权'].rolling(120).mean()
    extra_agg_dict['120日均线'] = 'last'


    # =计算bias
    df['bias'] = df['收盘价_复权'] / df['5日均线'] - 1
    extra_agg_dict['bias'] = 'last'
    
    df['bias_10'] = df['收盘价_复权'] / df['10日均线'] - 1
    extra_agg_dict['bias_10'] = 'last'
    
    df['bias_20'] = df['收盘价_复权'] / df['20日均线'] - 1
    extra_agg_dict['bias_20'] = 'last'
    
    df['bias_30'] = df['收盘价_复权'] / df['30日均线'] - 1
    extra_agg_dict['bias_30'] = 'last'


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

    df['120日累计涨跌幅'] = df['收盘价_复权'].pct_change(120)
    extra_agg_dict['120日累计涨跌幅'] = 'last'

    df['250日累计涨跌幅'] = df['收盘价_复权'].pct_change(250)
    extra_agg_dict['250日累计涨跌幅'] = 'last'

    # 计算资金流
    df['中户买入占比'] = df['中户资金买入额'] * 10000 / df['成交额']
    extra_agg_dict['中户买入占比'] = 'last'
    
    df['中户买入占比_5avg']  = df['中户买入占比'].rolling(5).mean()
    extra_agg_dict['中户买入占比_5avg'] = 'last'
    
    df['中户买入占比_20avg']  = df['中户买入占比'].rolling(20).mean()
    extra_agg_dict['中户买入占比_20avg'] = 'last'
    
    df['散户卖出占比'] = df['散户资金卖出额'] / (df['散户资金卖出额'] + df['中户资金卖出额'] + df['大户资金卖出额'] + df['机构资金卖出额'])
    extra_agg_dict['散户卖出占比'] = 'last'
    
    df['散户卖出占比_5avg'] = df['散户卖出占比'].rolling(5).mean()
    extra_agg_dict['散户卖出占比_5avg'] = 'last'
    
    df['散户卖出占比_20avg'] = df['散户卖出占比'].rolling(20).mean()
    extra_agg_dict['散户卖出占比_20avg'] = 'last'
    
    # # 计算成交额标准差
    # df['成交额std_5'] = df['成交额'].rolling(5).std()
    # extra_agg_dict['成交额std_5'] = 'last'
    
    # df['成交额std_10'] = df['成交额'].rolling(10).std()
    # extra_agg_dict['成交额std_10'] = 'last'
    
    # df['成交额std_20'] = df['成交额'].rolling(20).std()
    # extra_agg_dict['成交额std_20'] = 'last'

    return df


def calc_fin_factor(df, extra_agg_dict):
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
    df['有息负债'] = df[['B_st_borrow@xbx', 'B_lt_loan@xbx', 'B_bond_payable@xbx', 'B_noncurrent_liab_due_in1y@xbx']].sum(axis=1)
    df['EV2'] = df['总市值'] + df['有息负债'] - df['B_currency_fund@xbx'].fillna(0) # 计算EV2
    # 计算EBITDA
    # 坏账损失 字段无法直接从财报中获取，暂去除不计
    df['EBITDA'] = df[[
                        'R_operating_total_revenue@xbx', # 营业总收入
                        'B_interest_payable@xbx', # 负债应付利息
                        'B_charge_and_commi_payable@xbx', # 应付手续费及佣金
                        'R_sales_fee@xbx', # 销售费用
                        'R_manage_fee@xbx', # 管理费用
                        'R_rad_cost_sum@xbx', # 研发费用
                        'R_asset_impairment_loss@xbx', # 资产减值损失
                        'C_depreciation_etc@xbx', # 固定资产折旧、油气资产折耗、生产性生物资产折旧
                        'C_intangible_assets_amortized@xbx', # 无形资产摊销
                        'C_lt_deferred_expenses_amrtzt@xbx', # 长期待摊费用摊销
                        'R_other_compre_income@xbx', # 其他综合利益
                        'B_total_current_liab@xbx', # 流动负债合计
                        'B_total_noncurrent_liab@xbx' # 非流动负债合计
                        ]].sum(axis=1) - df[['R_operating_taxes_and_surcharge@xbx', # 税金及附加
                                             'R_operating_cost@xbx' # 营业成本
                                             ]].sum(axis=1)
    df['企业倍数'] = df['EV2'] / df['EBITDA'] # 计算企业倍数
    extra_agg_dict['企业倍数'] = 'last'
    
    # 计算归母PE
    # 归母PE = 总市值 / 归母净利润(ttm)
    df['归母PE(ttm)'] = df['总市值'] / df['R_np_atoopc@xbx_ttm']
    extra_agg_dict['归母PE(ttm)'] = 'last'
    
    #=市销率 = 总市值 / 主营业务收入
    df['ps_ttm'] = df['总市值'] / df['R_revenue@xbx_ttm']
    extra_agg_dict['ps_ttm'] = 'last'

    # 计算归母ROE
    # 归母ROE(ttm) = 归母净利润(ttm) / 归属于母公司股东权益合计
    df['归母ROE(ttm)'] = df['R_np_atoopc@xbx_ttm'] / df['B_total_equity_atoopc@xbx']
    extra_agg_dict['归母ROE(ttm)'] = 'last'
    
    # 新增ROE历史平均
    df['ROE_AVG'] = df['归母ROE(ttm)'].rolling(600).mean()
    df['ROE_R'] = df['归母ROE(ttm)'] / df['ROE_AVG']
    extra_agg_dict['ROE_R'] = 'last'
    
    # 计算EBIT（息税前利润）=归母净利润+利息费用+所得税
    df['EBIT'] = df['R_np_atoopc@xbx'] + df['R_interest_fee@xbx'] + df['R_income_tax_cost@xbx']
    # 计算EV(企业价值)= 总市值 + 其他权益工具 + 少数股东权益+ 带息负债
    df['EV'] = df['总市值'] + df['B_other_equity_instruments@xbx'].fillna(0) + df['B_minority_equity@xbx'] + df['有息负债']
    
    # 计算EY(股票收益率）= 息税前利润 / 企业价值
    df['EY'] = df['EBIT'] / df['EV']
    extra_agg_dict['EY'] = 'last'
    
    # ROC总资产收益率= 息税前利润 / （净营运资本 + 固定资产）
    #   净营运资本 = 应收账款 + 其他应收款* + 预付账款 + 存货 + 长期股权投资 + 投资性房地产 - 无息流动负债(应付账款 + 预收帐款 + 应付职工薪酬 + 应付税费 + 其他应付款* + (预提费用) + 递延收益流动负债 + 其他流动负债)
    df['净营运资本'] = df[['B_account_receivable@xbx',
                          'B_other_receivables@xbx',
                          'B_prepays@xbx','B_inventory@xbx',
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
    
    # 毛利率(ttm) = ( 营业总收入_ttm - 营业总成本_ttm ) / 营业总收入_ttm
    df['毛利率(ttm)'] = 1 - df['R_operating_total_cost@xbx_ttm'] / df['R_operating_total_revenue@xbx_ttm']
    extra_agg_dict['毛利率(ttm)'] = 'last'
    
    df['净资产负债率'] = df['B_total_liab@xbx'] / df['B_total_equity_atoopc@xbx']
    extra_agg_dict['净资产负债率'] = 'last'

    # 计算净利润现金含量
    df['T'] = df['R_income_tax_cost@xbx'] / df['R_total_profit@xbx']
    df['净利润现金含量'] = df['C_ncf_from_oa_im@xbx'] * (1 - df['T']) / df['R_np@xbx_ttm']
    extra_agg_dict['净利润现金含量'] = 'last'
    
    # 新增存货周转天数
    #df['存货周转天数'] = 365 * (df['B_inventory@xbx'] + df['B_inventory@xbx'].shift()) / 2 / (df['R_operating_total_cost@xbx'] - df['R_asset_impairment_loss@xbx'])
    #extra_agg_dict['存货周转天数'] = 'last'
    
    df['存货周转'] = 365 * df['B_inventory@xbx'] / (df['R_operating_total_cost@xbx'] - df['R_asset_impairment_loss@xbx'])
    extra_agg_dict['存货周转'] = 'last'
    
    # 投资占比:投资支出/营总收
    df['投资占比'] = df['C_invest_paid_cash@xbx'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['投资占比'] = 'last'
    
    df['经营活动现金流入小计'] = df['C_sub_total_of_ci_from_oa@xbx']
    extra_agg_dict['经营活动现金流入小计'] = 'last'

    df['经营活动现金流出小计'] = df['C_sub_total_of_cos_from_oa@xbx']
    extra_agg_dict['经营活动现金流出小计'] = 'last'
    
    df['经营活动现金流比率'] = df['C_sub_total_of_ci_from_oa@xbx'] / df['C_sub_total_of_cos_from_oa@xbx']
    extra_agg_dict['经营活动现金流比率'] = 'last'
    
    # 现金流负债比 = 现金流量净额(经营活动) / 总负债(流动负债合计 + 非流动负债合计)
    df['现金流负债比'] = df['C_ncf_from_oa@xbx'] / (df['B_total_current_liab@xbx'] + df['B_total_noncurrent_liab@xbx'])
    extra_agg_dict['现金流负债比'] = 'last'
    
    df['经营现金流量总负债比'] = df['C_ncf_from_oa@xbx'] / df['B_total_liab@xbx']
    extra_agg_dict['经营现金流量总负债比'] = 'last'
    
    df['流动比率'] = df['B_total_current_assets@xbx'] / df['B_total_current_liab@xbx']
    extra_agg_dict['流动比率'] = 'last'
    
    #新增速动比率
    df['速动比率'] = (df['B_total_current_assets@xbx'] -df['B_inventory@xbx']) / df['B_total_current_liab@xbx']
    extra_agg_dict['速动比率'] = 'last'

    # 营收含金量：经营净现金流/营总收
    df['营收含金量'] = df['C_ncf_from_oa@xbx'] / df['R_operating_total_revenue@xbx']
    extra_agg_dict['营收含金量'] = 'last'

    # #营业收入同比增长率 = 当期营业收入/上期营业收入 -1
    df['营业收入同比增加（ttm）'] = df['R_operating_total_revenue@xbx'] / df['R_operating_total_revenue@xbx'].shift() - 1
    extra_agg_dict['营业收入同比增加（ttm）'] = 'last'

    return df
# !!!
