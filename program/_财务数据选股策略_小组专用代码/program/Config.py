"""
《邢不行-2021新版|Python股票量化投资课程》
author: 邢不行
微信: xbx9585

财务数据选股专属代码

配置参数
"""
import os

# ===策略名
strategy_name = '基础财务数据选股策略'
# ===系统配置
# 开启debug模式，调试参数
is_debug_swich = 1
# ===复权配置
fuquan_type = '后复权'

# ===选股参数设定
period_type = 'W'  # W代表周，M代表月
date_start = '2021-01-01'  # 需要从10年开始，因为使用到了ttm的同比差分，对比的是3年持续增长的数据
date_end = '2022-10-01'
select_stock_num = 1 # 选股数量
c_rate = 1.2 / 10000  # 手续费
t_rate = 1 / 1000  # 印花税

# ===获取项目根目录
_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, '..'))  # 返回根目录文件夹
# print(root_path)
# exit()
"""
财务数据选股小组第2期专属数据
百度网盘：
    链接：https://pan.baidu.com/s/1H8SXIjloK0gif2nEJRrNhQ 
    提取码：2ef9 
奶牛快传：
    https://xbx.cowtransfer.com/s/e271d2e7d0d64b
"""


# 股票日线数据
stock_data_path = root_path + '/data/daily_data/stock'

# 财务数据路径
finance_data_path = root_path + '/data/fin_data/fin_xbx'

# 指数数据路径
index_path = root_path + '/data/index_data/sh000300.csv'

# !!!
# 因为财务数据众多，将本策略中需要用到的财务数据字段罗列如下
raw_fin_cols = [
    # 短期借款 长期借款 应付债券 一年内到期的非流动负债
    'B_st_borrow@xbx', 'B_lt_loan@xbx', 'B_bond_payable@xbx', 'B_noncurrent_liab_due_in1y@xbx',
    # 营业总收入 负债应付利息 应付手续费及佣金
    'R_operating_total_revenue@xbx', 'B_interest_payable@xbx', 'B_charge_and_commi_payable@xbx',
    # 销售费用 管理费用 研发费用 资产减值损失
    'R_sales_fee@xbx', 'R_manage_fee@xbx', 'R_rad_cost_sum@xbx', 'R_asset_impairment_loss@xbx',
    # 固定资产折旧、油气资产折耗、生产性生物资产折旧 无形资产摊销 长期待摊费用摊销
    'C_depreciation_etc@xbx', 'C_intangible_assets_amortized@xbx', 'C_lt_deferred_expenses_amrtzt@xbx',
    # 其他综合利益 税金及附加 营业成本
    'R_other_compre_income@xbx', 'R_operating_taxes_and_surcharge@xbx', 'R_operating_cost@xbx',
    # 归母净利润 归母所有者权益合计 货币资金  利润表的净利润 利润表的营业总成本
    'R_np_atoopc@xbx', 'B_total_equity_atoopc@xbx', 'B_currency_fund@xbx', 'R_np@xbx', 'R_operating_total_cost@xbx',
    # 非流动负债合计 经营活动产生的现金流量净额 流动负债合计
    'B_total_noncurrent_assets@xbx', 'B_total_current_assets@xbx',	'B_total_assets@xbx', 'B_goodwill@xbx',
    #   股本        营业收入
    'B_actual_received_capital@xbx', 'R_revenue@xbx',
    # 利息费用 所得税 利润总额
    'R_interest_fee@xbx', 'R_income_tax_cost@xbx', 'R_total_profit@xbx', 'C_ncf_from_oa_im@xbx',
    'C_cash_pay_for_debt@xbx', 'C_invest_paid_cash@xbx',

    # 其他权益工具 少数股东权益 营业总收入
    'B_other_equity_instruments@xbx', 'B_minority_equity@xbx', 'R_operating_total_revenue@xbxx',

    # //计算净营运资本所用字段//
    # 应收账款 + 其他应收款* + 预付账款 + 存货 + 长期股权投资 + 投资性房地产 - 无息流动负债
    'B_account_receivable@xbx', 'B_other_receivables@xbx', 'B_prepays@xbx',
    'B_inventory@xbx', 'B_lt_equity_invest@xbx', 'B_invest_property@xbx',
    # 应付账款 + 预收帐款 + 应付职工薪酬 + 应付税费 + 其他应付款* + (预提费用) + 递延收益流动负债 + 其他流动负债
    'B_accounts_payable@xbx', 'B_advance_payment@xbx', 'B_payroll_payable@xbx',
    'B_tax_payable@xbx', 'B_other_payables_sum@xbx', 'B_differed_incomencl@xbx',
    'B_other_current_liab@xbx',
    # 资产固定资产    每股收益    经营活动产生的现金流量的商品销售、提供劳务收到的现金
    'B_fixed_asset@xbx', 'R_basic_eps@xbx', 'C_cash_received_of_sales_service@xbx',
    # 所有者权益合计   现金流量表_经营活动产生的现金流量的经营活动现金流入小计
    'B_total_owner_equity@xbx', 'C_sub_total_of_ci_from_oa@xbx', 'C_sub_total_of_cos_from_oa@xbx',
    # 营业利润  现金及现金等价物的净增加额   筹资活动产生的现金流量净额   投资活动产生的现金流量净额
    'R_op@xbx', 'C_net_increase_in_cce@xbx', 'C_ncf_from_fa@xbx', 'C_ncf_from_ia@xbx',
    # 资产负债表_流动负债的流动负债合计   资产负债表_非流动负债的非流动负债合计   现金流量净额  负债的负债合计
    'B_total_current_liab@xbx', 'B_total_noncurrent_liab@xbx', 'C_ncf_from_oa@xbx', 'B_total_liab@xbx',
    'B_total_liab_and_owner_equity@xbx',
]

# raw_fin_cols财务数据中所需要计算流量数据的原生字段
flow_fin_cols = [
    # 归母净利润 净利润 营业总收入 营业总成本
    'R_np_atoopc@xbx', 'R_np@xbx', 'R_operating_total_revenue@xbx', 'R_operating_total_cost@xbx',
    # 营业收入
    'R_revenue@xbx', 'B_total_noncurrent_assets@xbx',
    # 现金流量表_经营活动产生的现金流量的经营活动现金流入小计
    'C_sub_total_of_ci_from_oa@xbx',
    # 现金流量表_经营活动产生的现金流量的经营活动现金流出小计
    'C_sub_total_of_cos_from_oa@xbx',
]

# raw_fin_cols财务数据中所需要计算截面数据的原生字段
cross_fin_cols = []

# 下面是处理财务数据之后需要的ttm，同比等一些字段
derived_fin_cols = [
    # 归母净利润_TTM  归母净利润_TTM同比  净利润_TTM  净利润_TTM同比
    'R_np_atoopc@xbx_ttm', 'R_np_atoopc@xbx_ttm同比', 'R_np@xbx_ttm', 'R_np@xbx_ttm同比', 'R_np_atoopc@xbx_累计同比',
    '归母净利润率(ttm)',
    # 营业总收入_TTM  营业总成本_TTM  营业收入_TTM
    'R_operating_total_revenue@xbx_ttm', 'R_operating_total_cost@xbx_ttm', 'R_revenue@xbx_ttm', 'BV(ttm)',
    # 归母净利润单季同比 归母净利润单季环比 营业总收入单季同比 营业总收入单季环比
    'R_np_atoopc@xbx_单季环比', 'R_operating_total_revenue@xbx_单季环比', 'R_operating_total_revenue@xbx_累计同比',
    'R_revenue@xbx_ttm同比', 'R_revenue@xbx_上季ttm同比', 'R_np_atoopc@xbx_上季ttm同比',
]
# !!!
