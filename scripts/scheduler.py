import os, time
from datetime import datetime, timedelta
from helperapp.models import Predict_grow
import schedule
import requests
#import random


#http://127.0.0.1:5000/TONCOIN_USDT_1h_75_24_gateio-v1-alisa

#period_predict: 24h,   \\это просто значение для базы чтоб понимать на сколько прогноз
#period: 24,            \\это значение для добавления целевого столбца Target (на сколько свечей брать прогноз)
#tick_interval: 10s, 1m, 5m, 15m, 30m, 1h, 4h, 8h, 1d, 7d, 30d  \\from gate.io
 
def get_from_flask_api(market, tick_interval, tick_limit, nn_name, period_predict, period):
    url = 'http://flask:5000/'+market+'_'+tick_interval+'_'+tick_limit+'_'+period+'_'+nn_name
    data_from_api = requests.get(url).json()
    print(market)
    print(data_from_api)
    unix_time_close = data_from_api[0]
    price = data_from_api[1]
    value_predict = data_from_api[2]
    request_status_code = data_from_api[3]

    #почему то по риплу и тон NaN иногда приходят в предикте если Volume 0 менять на 1 а не на 1000 возможно связано с тем что цена меньше 1
    #if value_predict == '' or value_predict == None:
    #    value_predict = random.randint(490,510) / 1000


    newpredict = Predict_grow.objects.create()
    newpredict.pair = market
    newpredict.nn = nn_name
    newpredict.period = period_predict

    newpredict.value = value_predict
    newpredict.price = price
    newpredict.trueorfalse = None
    
    unix_time_close = int(unix_time_close)
    datetime_close = datetime.utcfromtimestamp(unix_time_close)#переводим юникс-время в формат YYYY-MM-DD HH:MM[:ss[.uuuuuu]]
    
    newpredict.time_close = datetime_close
    newpredict.save()     
            

def check_predict_true_or_false (period_predict):
    if period_predict == '1h':
        try:
            timenow = datetime.now()
            time_1h_early = timenow - timedelta(hours = 1)  #определяем значение времени которое было час назад
            dontknown_list = Predict_grow.objects.filter(period = '1h').filter(trueorfalse = None).exclude(time__gt = time_1h_early)
            #dontknown_list - список объектов модели Predict_grow, с периодом 1h и у которых еще не проставлено значение trueorfalse (сбылось не сбылось)
            #за исключением тех которые были добавлены час назад
            for i in dontknown_list:#проверяем сбылось не сбылось и проставляем значения
                i_pair = i.pair
                i_price = i.price
                i_value = i.value
                i_time = i.time
                time_1h_later = i_time + timedelta(hours = 1)  #определяем значение времени которое было через час после i_time
                price_after_1h = Predict_grow.objects.filter(pair = i_pair).filter(time__gte = time_1h_later).first().price
                #определяем цену через час (берем все значения через час и позднее и берем первое из них)
                delta_price = price_after_1h - i_price
                if (delta_price < 0) and (i_value < 0.5):
                    i.trueorfalse = True
                elif (delta_price > 0) and (i_value > 0.5):
                    i.trueorfalse = True
                else:
                    i.trueorfalse = False
                i.save()
        except:
            print('check predict 1H error')
    elif period_predict == '1d':
        try:
            timenow = datetime.now()
            time_1d_early = timenow - timedelta(days = 1)  #определяем значение времени которое было день назад
            dontknown_list = Predict_grow.objects.filter(period = '1d').filter(trueorfalse = None).exclude(time__gt = time_1d_early)
            for i in dontknown_list:#проверяем сбылось не сбылось и проставляем значения
                i_pair = i.pair
                i_price = i.price
                i_value = i.value
                i_time = i.time
                time_1d_later = i_time + timedelta(days = 1)  #определяем значение времени которое было через день после i_time
                price_after_1d = Predict_grow.objects.filter(pair = i_pair).filter(time__gte = time_1d_later).first().price
                #определяем цену через час (берем все значения через час и позднее и берем первое из них)
                delta_price = price_after_1d - i_price
                if (delta_price < 0) and (i_value < 0.5):
                    i.trueorfalse = True
                elif (delta_price > 0) and (i_value > 0.5):
                    i.trueorfalse = True
                else:
                    i.trueorfalse = False
                i.save()
        except:
            print('check predict 1d error')
    elif period_predict == '7d':
        try:
            timenow = datetime.now()
            time_7d_early = timenow - timedelta(days = 7)  #определяем значение времени которое было неделю назад
            dontknown_list = Predict_grow.objects.filter(period = '7d').filter(trueorfalse = None).exclude(time__gt = time_7d_early)
            for i in dontknown_list:#проверяем сбылось не сбылось и проставляем значения
                i_pair = i.pair
                i_price = i.price
                i_value = i.value
                i_time = i.time
                time_7d_later = i_time + timedelta(days = 7)  #определяем значение времени которое было через день после i_time
                price_after_7d = Predict_grow.objects.filter(pair = i_pair).filter(time__gte = time_7d_later).first().price
                #определяем цену через час (берем все значения через час и позднее и берем первое из них)
                delta_price = price_after_7d - i_price
                if (delta_price < 0) and (i_value < 0.5):
                    i.trueorfalse = True
                elif (delta_price > 0) and (i_value > 0.5):
                    i.trueorfalse = True
                else:
                    i.trueorfalse = False
                i.save()
        except:
            print('check predict 7d error')
    else:
        print('check predict')


#schedule.every(60).seconds.do(get_from_binance_in_csv, 'ETHUSDT', '1m')
#schedule.every().hour.do(get_from_binance_in_csv, 'ETHUSDT', '1h')


list_token_pair = ['TONCOIN_USDT', 'BTC_USDT', 'ETH_USDT', 'BNB_USDT', 'DOGE_USDT', 'ADA_USDT', 'TRX_USDT', 'XRP_USDT']

#1h прогноз
for x in list_token_pair:
    schedule.every(10).minutes.at(":01").do(get_from_flask_api, x, '5m', '75', 'gateio_v1_roma', '1h', '12')
    schedule.every(10).minutes.at(":01").do(get_from_flask_api, x, '5m', '75', 'gateio_v1_dasha', '1h', '12')
    schedule.every(10).minutes.at(":01").do(get_from_flask_api, x, '5m', '75', 'gateio_v1_alisa', '1h', '12')
#1d прогноз
for x in list_token_pair:
    schedule.every().hour.at(":05").do(get_from_flask_api, x, '1h', '75', 'gateio_v1_roma', '1d', '24')
    schedule.every().hour.at(":05").do(get_from_flask_api, x, '1h', '75', 'gateio_v1_dasha', '1d', '24')
    schedule.every().hour.at(":05").do(get_from_flask_api, x, '1h', '75', 'gateio_v1_alisa', '1d', '24')
#7d прогноз
for x in list_token_pair:
    schedule.every().day.at("00:07").do(get_from_flask_api, x, '8h', '75', 'gateio_v1_roma', '7d', '21')
    schedule.every().day.at("00:07").do(get_from_flask_api, x, '8h', '75', 'gateio_v1_dasha', '7d', '21')
    schedule.every().day.at("00:07").do(get_from_flask_api, x, '8h', '75', 'gateio_v1_alisa', '7d', '21')


schedule.every(10).minutes.at(":04").do(check_predict_true_or_false, '1h')
schedule.every().hour.at(":09").do(check_predict_true_or_false, '1d')
schedule.every().day.at("00:17").do(check_predict_true_or_false, '7d')


'''
schedule.every().day.at("08:05").do(base_downloader)
schedule.every().day.at("08:10").do(base_loader)
schedule.every(5).seconds.do(base_downloader)
schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
'''


while True:
    schedule.run_pending()
    time.sleep(1)

      
