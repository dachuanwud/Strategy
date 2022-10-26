"""
配置参数
"""
import os

# ===策略名
strategy_name = '基础财务数据选股策略'

# ===复权配置
fuquan_type = '后复权'

# ===选股参数设定
period_type = 'W'  # W代表周，M代表月
date_start = '2020-01-01'  # 需要从10年开始，因为使用到了ttm的同比差分，对比的是3年持续增长的数据
date_end = '2022-09-16'
select_stock_num = 1  # 选股数量
c_rate = 1.2 / 10000  # 手续费
t_rate = 1 / 1000  # 印花税

# 是否生成神经网络的输入数据
is_input_data = False

# ===获取项目根目录
_ = os.path.abspath(os.path.dirname(__file__))  # 返回当前文件路径
root_path = os.path.abspath(os.path.join(_, '..'))  # 返回根目录文件夹
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
    'B_st_borrow@xbx',  # 短期借款
    'B_lt_loan@xbx',  # 长期借款
    'B_bond_payable@xbx',  # 应付债券
    'B_noncurrent_liab_due_in1y@xbx',  # 一年内到期的非流动负债
    'B_interest_payable@xbx',  # 负债应付利息
    'B_charge_and_commi_payable@xbx',  # 应付手续费及佣金
    'B_currency_fund@xbx',  # 货币资金
    'B_total_current_liab@xbx',  # 流动负债合计
    'B_total_noncurrent_liab@xbx',  # 非流动负债合计
    'B_total_equity_atoopc@xbx',  # 归母所有者权益合计

    'B_invest_property@xbx',  # 投资性房地产
    'B_advance_payment@xbx',  # 预收账款
    'B_account_receivable@xbx',  # 应收账款
    'B_other_receivables@xbx',  # 其他应收款
    'B_prepays@xbx',  # 预付账款
    'B_accounts_payable@xbx',  # 应付账款
    'B_payroll_payable@xbx',  # 应付职工薪酬
    'B_tax_payable@xbx',  # 应付税费
    'B_other_payables_sum@xbx',  # 其他应付款合计
    'B_lt_equity_invest@xbx',  # 长期股权投资
    'B_differed_incomencl@xbx',  # 递延收益-非流动负债
    'B_other_current_liab@xbx',  # 其他流动负债
    'B_inventory@xbx',  # 流动资产的存货
    'B_fixed_asset@xbx',  # 固定资产
    'B_total_current_assets@xbx',  # 流动资产合计
    'B_total_liab@xbx',  # 负债合计
    'B_minority_equity@xbx',  # 少数股东权益
    'B_total_liab_and_owner_equity@xbx',  # 所有者权益的负债及所有者权益总计
    'B_other_equity_instruments@xbx',  # 所有者权益的其他权益工具

    'R_operating_total_revenue@xbx',  # 营业总收入
    'R_revenue@xbx',  # 主营业务收入
    'R_operating_total_cost@xbx',  # 营业总成本
    'R_operating_cost@xbx',  # 营业成本
    'R_sales_fee@xbx',  # 销售费用
    'R_manage_fee@xbx',  # 管理费用
    'R_rad_cost_sum@xbx',  # 研发费用
    'R_asset_impairment_loss@xbx',  # 资产减值损失
    'R_other_compre_income@xbx',  # 其他综合利益
    'R_operating_taxes_and_surcharge@xbx',  # 税金及附加
    'R_np@xbx',  # 净利润
    'R_np_atoopc@xbx',  # 归母净利润
    'R_interest_payout@xbx',  # 利息支出
    'R_interest_fee@xbx',  # 利息费用
    'R_income_tax_cost@xbx',  # 利润表的所得税费用
    'R_total_profit@xbx',  # 利润表的利润总额

    'C_ncf_from_oa@xbx',  # 现金流量表_经营活动产生的现金流量的经营活动产生的现金流量净额
    'C_ncf_from_oa_im@xbx',  # 现金流量表_补充资料的间接法-经营活动产生的现金流量净额
    'C_sub_total_of_ci_from_oa@xbx',  # 经营活动现金流入小计
    'C_sub_total_of_cos_from_oa@xbx',  # 经营活动现金流出小计
    'C_depreciation_etc@xbx',  # 固定资产折旧、油气资产折耗、生产性生物资产折旧
    'C_intangible_assets_amortized@xbx',  # 无形资产摊销
    'C_lt_deferred_expenses_amrtzt@xbx',  # 长期待摊费用摊销
    'C_invest_paid_cash@xbx',  # 投资活动产生的现金流量的投资支付的现金
    'C_ncf_from_ia@xbx',  # 投资活动产生的现金流量净额
]

# raw_fin_cols财务数据中所需要计算流量数据的原生字段
flow_fin_cols = [
    'R_np@xbx',  # 净利润
    'R_np_atoopc@xbx',  # 归母净利润
    'R_operating_total_revenue@xbx',  # 营业总收入
    'R_operating_total_cost@xbx',  # 营业总成本
]

# raw_fin_cols财务数据中所需要计算截面数据的原生字段
cross_fin_cols = []

# 下面是处理财务数据之后需要的ttm，同比等一些字段
derived_fin_cols = [
    'R_np_atoopc@xbx_ttm',  # 归母净利润_TTM
    'R_np_atoopc@xbx_ttm同比',  # 归母净利润_TTM同比
    'R_np@xbx_ttm',  # 净利润_TTM
    'R_np@xbx_ttm同比',  # 净利润_TTM同比
    'R_operating_total_revenue@xbx_ttm',  # 营业总收入_TTM
    'R_operating_total_cost@xbx_ttm',  # 营业总成本_TTM
    'R_revenue@xbx_ttm',  # 主营业务收入_TTM
    'R_np_atoopc@xbx_单季环比',  # 归母净利润单季环比
    'R_operating_total_revenue@xbx_单季环比',  # 营业总收入单季环比
    'R_operating_total_revenue@xbx_累计同比',  # 营业总收入单季同比
]
# !!!