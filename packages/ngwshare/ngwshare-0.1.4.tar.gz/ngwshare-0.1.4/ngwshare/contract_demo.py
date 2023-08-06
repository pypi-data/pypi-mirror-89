import ngshare as ng
import time
import pandas as pd
# pd.set_option('display.height',1000)
pd.set_option('display.max_rows',5000)
pd.set_option('display.max_columns',5000)
pd.set_option('display.width',10000)

# data = ng.get_hisBar(symbol='rb2011',exchange='SHFE',freq='1m',start='2020-09-01',end='2020-10-20')
# print(data)


# data = ng.get_hisBar(symbol='rbM',exchange='SHFE',freq='1m',start='2020-01-01',end='2020-10-20')
# print(data)

# data = ng.get_hisBar(symbol='rbM',exchange='SHFE',freq='1m',start='2019-01-01',end='2019-10-01')
# print(data)


# data = ng.get_hisBar(symbol='rb2011',exchange='SHFE',freq='15m',start='2019-10-01',end='2020-10-20')
# print(data)


# data = ng.get_hisBar(symbol='rb2011',exchange='SHFE',freq='15m',start='2019-10-01',end='2020-10-20')
# print(data)


# data = ng.get_hisBar(symbol='i2011',exchange='DCE',freq='1m',start='2019-10-01',end='2020-10-20')
# print(data)

# data = ng.get_hisBar(symbol='cM',exchange='DCE',freq='1d',start='2020-10-01',end='2020-10-20')
# print(data)



# data = ng.get_hisBar(symbol='ZC012',exchange='CZCE',freq='1d',start='2020-10-01',end='2020-10-20')
# print(data)


# data = ng.get_hisBar(symbol='rb2101',exchange='SHFE',freq='1m',start='2020-10-20',end='2020-10-21')
# print(data)

# close_price = data.loc[(data['time'] > 20201020222600)]
# print(close_price)

# close_price = data.loc[(data['time'] > 20201020222600)].iloc[0]['open']
# print(close_price)


# data = ng.get_hisBar(symbol='ag2101',exchange='SHFE',freq='1m',start='2020-10-29 09:00:00',end='2020-10-30 15:00:00')
# print(data)
#
# data = ng.get_hisBar(symbol='hcM',exchange='SHFE',freq='1m',start='2020-10-20 09:00:00',end='2020-10-30 15:00:00')
# print(data)

# data = ng.get_hisBar(symbol='ag2101',exchange='SHFE',freq='5m',start='2020-10-29 09:00:00',end='2020-10-30 15:00:00')
# print(data)
# data = ng.get_hisBar(symbol='ag2101',exchange='SHFE',freq='15m',start='2020-10-29 09:00:00',end='2020-10-30 15:00:00')
# print(data)
# data = ng.get_hisBar(symbol='ag2101',exchange='SHFE',freq='30m',start='2020-10-29 09:00:00',end='2020-10-30 15:00:00')
# print(data)
# data = ng.get_hisBar(symbol='ag2101',exchange='SHFE',freq='60m',start='2020-10-29 09:00:00',end='2020-10-30 15:00:00')
# print(data)
# data = ng.get_hisBar(symbol='ag2101',exchange='SHFE',freq='1d',start='2020-10-28 09:00:00',end='2020-10-30 15:00:00')
# print(data)


# data = ng.contract_depth(symbol='rb2101',exchange='SHFE')
# print(data)


# # 获取某一时刻的全部价格(time不传为目前时间)
# data = ng.all_contract_price(freq='1d',time='2020-11-19')
# print(data)
# data = ng.all_contract_price(freq='1m')
# print(data)

# # -----------------------------------------------------------------------------------------------------------
# t1 = time.time()

# # Tick
#
# data = ng.get_hisTick(symbol='rb2101',exchange='SHFE',count=1)
# print(data)


# data = ng.get_hisTick(symbol='rb2101',exchange='SHFE',start='2020-11-10 13:30:00',end='2020-11-10 14:30:00')
# print(data)

# # 获取用户持仓
# import hashlib
# def get_sign1(start,end):
#     m = hashlib.md5()
#     m.update('inquantRisk:{}{}'.format(start, end).encode('utf-8'))
#     return m.hexdigest().upper()
#
# start = '2020-11-10'
# end = '2020-11-11'
# sign = get_sign1(start,end)
# print(sign)
# data = ng.contract_position_users(start=start,end=end,sign=sign)
# print(data)



# def get_sign2(start,end,code):
#     m = hashlib.md5()
#     m.update('inquantRiskContract:{}{}{}'.format(start, end, code).encode('utf-8'))
#     return m.hexdigest().upper()
# # 获取用户持仓
# code = 'a1909'
# start = '2020-11-16'
# end = '2020-11-20'
# sign = get_sign2(start,end,code)
# print(sign)
# data = ng.contract_all_position_users(start=start,end=end,code=code,sign=sign)
# print(data)



# # # 获取所有现货code
# # data = ng.get_all_spot()
# # print(data)

# # # 获取现货价格
# # data = ng.get_spot_price(spotCode='cuXH',start='2020-11-10',end='2020-11-11')
# # print(data)


# # 获取合约分类
# data = ng.get_contract_varieties(type=4)
# print(data)
# # type（3：中金所，4：上期所，5：大商所，6：郑商所 ,11:主力合约 12：夜盘合约,13:环球,101:主连合约


# # 获取买卖情况
# data = ng.get_TradeVolumeRanking(vid=24,start='2020-01-13',end='2020-02-10')
# print(data)




# # 获取所有合约
# data = ng.get_all_contract()
# print(data)


# # 获取单个合约信息
# data = ng.get_contract_detail(symbol='rb2105',exchange='SHFE')
# print(data)

# # 获取单个合约信息
# data = ng.get_contract_detail(symbol='ag2101',exchange='SHFE')
# print(data)

# 获取单个合约信息
# data = ng.get_contract_detail(symbol='i2101',exchange='DCE')
# print(data)
# # 获取单个合约信息
# data = ng.get_contract_detail(symbol='au2012',exchange='SHFE')
# print(data)


# # 获取主力合约
# data = ng.get_main_contract(variety_code='rb')
# print(data)
# print(data['symbol'])


# # 获取一个时间段的 交易时间
# data = ng.get_contract_openTime(start='2020-09-01',end='2020-10-01')
# print(data)
#
#
# print(time.time()-t1)
# # -----------------------------------------------------------------------------------------------------------



# # 获取所有品种variety
# data = ng.get_all_varieties()
# print(data)


# a = data.loc[data['varietyCode']=='cs']
# print(a)
#
#
# varietyId = a['id'].tolist()[0]
# print(varietyId,type(varietyId))
#
# lots = a['lots'].tolist()[0]
# print(lots,type(lots))


# # 获取乘数、保证金比率
all_margin_ratios = ng.get_all_margin_ratios()
print(all_margin_ratios)
# data = all_margin_ratios[all_margin_ratios.varietyID==10]
# print(data)
# data = all_margin_ratios[(all_margin_ratios.varietyID==23) & (all_margin_ratios['code']=='!')]
# print(data)
# data = all_margin_ratios[(all_margin_ratios.varietyID==23) & (all_margin_ratios['code']=='!')]['ratio'].tolist()[-1]
# print(data)


# a = all_margin_ratios.loc[all_margin_ratios['varietyID']==varietyId]['ratio']
# print(a)
#
# b = a.tolist()[-1]
# print(b)



# t1 = time.time()
#
#
# universe = 'buM.SHFE'
# variety = universe.split(".")[0][:-1]
# market = universe.split(".")[1]
# data = ng.get_main_contract(variety_code=variety)
# print(data)
# main_symbol = data["symbol"]+"."+market
# print([main_symbol])
#
#
#
# print(time.time()-t1)
