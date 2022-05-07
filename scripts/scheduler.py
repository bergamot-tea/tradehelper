import os, time
from datetime import datetime, timedelta
from helperapp.models import Klines, Predict_grow
import schedule
import pandas as pd #для работы с таблицами
import numpy as np
import requests

import math
import numpy as np
import pandas as pd
from tensorflow.keras import Input, Model
from tensorflow.keras.models import model_from_json #загрузка модели из файлов json и h5



def target(data, ndays, name_column):   #добавляет столбец к датафрейму в котором 1 - если цена повысится через nday периодов и 0 - если цена понизится через nday периодов
    Close = data['Close']

    target = pd.Series((Close.shift(0 - ndays) - Close) ,name = name_column)
    #если в плюс то 1 если в минус то 0
    for i in range(0,len(target)-1):
        if target[i] > 0:
            target[i] = 1
        else:
            target[i] = 0

    data = data.join(target) 
    return data

def CCI(data, ndays, name_column): 
    TP = (data['High'] + data['Low'] + data['Close']) / 3 
    CCI = pd.Series((TP - TP.rolling(ndays).mean()) / (0.015 * TP.rolling(ndays).std()),
                    name = name_column) 
    data = data.join(CCI) 
    return data

def EVM(data, ndays, name_column): 
    dm = ((data['High'] + data['Low'])/2) - ((data['High'].shift(1) + data['Low'].shift(1))/2)
    br = (data['Volume'] / 100000000) / ((data['High'] - data['Low']))
    EVM = dm / br 
    EVM_MA = pd.Series(EVM.rolling(ndays).mean(), name = name_column) 
    data = data.join(EVM_MA) 
    return data


def SMA(data, ndays, name_column): 
    SMA = pd.Series(data['Close'].rolling(ndays).mean(), name = name_column) 
    data = data.join(SMA) 
    return data

# Exponentially-weighted Moving Average 
def EWMA(data, ndays, name_column): 
    EMA = pd.Series(data['Close'].ewm(span = ndays, min_periods = ndays - 1).mean(),name = name_column) 
    data = data.join(EMA) 
    return data

def ROC(data,n,name_column):
    N = data['Close'].diff(n)
    D = data['Close'].shift(n)
    ROC = pd.Series(N/D,name=name_column)
    data = data.join(ROC)
    return data

def ForceIndex(data, ndays, name_column): 
    FI = pd.Series(data['Close'].diff(ndays) * data['Volume'], name = name_column) 
    data = data.join(FI) 
    return data


def add_target(df, period):
    df = target(df,period,'Target') #целевой столбец
    return df

def add_indicators(df):
    df = CCI(df,24,'CCI_24') # 24 часа
    df = CCI(df,72,'CCI_72') # 72 часа
    df = EVM(df,24,'EVM_24') # 24 часа
    df = EVM(df,72,'EVM_72') # 72 часа    
    df = SMA(df,24,'SMA_24') # 24 часа
    df = SMA(df,72,'SMA_72') # 72 часа
    df = EWMA(df,24,'EWMA_24') # 24 часа
    df = EWMA(df,72,'EWMA_72') # 72 часа 
    df = ROC(df,24,'ROC_24') # 24 часа
    df = ROC(df,72,'ROC_72') # 72 часа 
    df = ForceIndex(df,24,'ForceIndex_24') # 24 часа
    df = ForceIndex(df,72,'ForceIndex_72') # 72 часа       
    return df




'''
def get_from_binance_in_csv(pair, period):
    market = pair
    tick_interval = period
    url = 'https://api.binance.com/api/v3/klines?symbol='+market+'&interval='+tick_interval
    data_binance = requests.get(url).json()
    df = pd.DataFrame(data_binance)
    df.columns = ['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','Ignore']
    df = df.astype(float)
    df = add_indicators(df)
    df = df.dropna(axis='index', how='any')
    
    df.to_csv('klines_'+pair+'_'+period+'.csv', sep='\t', encoding='utf-8', index=False)
    
    what_time = np.asarray(df.iloc[:,6])#только столбец Close time, берем пока не дропнули
    
    df.drop(['Ignore', 'Open time', 'Close time'], axis=1, inplace=True)
    #отдельяем столбец с целевым значением от остальной таблицы с данными
    X_class = np.asarray(df.iloc[:,~df.columns.isin(['Target'])]) #все кроме столбца Target
    Y_class = np.asarray(df.iloc[:,9])#только столбец Target

    mean_X = X_class.mean(axis=0)
    std_X = X_class.std(axis=0)

    X_class_std = X_class - mean_X
    X_class_std = X_class_std / std_X
    X_class = X_class_std

    folder = ''

    model_json=folder+"my_model.json"
    model_h5=folder+"my_model.h5"


    #загрузка структуры
    json_file = open(model_json, "r")
    loaded_model_json = json_file.read()
    json_file.close()

    model2 = model_from_json(loaded_model_json)
    # загрузка весов
    model2.load_weights(model_h5)
    model = Model(model2.input, model2.layers[-1].output)
    model.trainable = True

    pred = model.predict(X_class) 

    np2 = np.column_stack((what_time, pred, Y_class)) #соединяем массивы Numpy в один
    df2 = pd.DataFrame(np2)
    df2.columns = ['Время', 'Прогноз роста', 'Рост']
    
    df2.loc[df2['Рост'] == 1, 'Рост'] = 'Да'
    df2.loc[df2['Рост'] == 0, 'Рост'] = 'Нет'
    
  
    for i in df2['Время']:
        i = i / 1000
        i = datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S')
    
    df2.to_csv('klines_predict_'+pair+'_'+period+'.csv', sep=',', encoding='utf-8', index=False)
    
   
'''

#period_predict: 24h,   \\это просто значение для базы чтоб понимать на сколько прогноз
#period: 24,            \\это значение для добавления целевого столбца Target (на сколько свечей брать прогноз)
#tick_interval: 10s, 1m, 5m, 15m, 30m, 1h, 4h, 8h, 1d, 7d, 30d  \\from gate.io

 
def get_from_gateio(market, tick_interval, tick_limit, nn_name, period_predict, period):
    while True:
        try:
            url = 'https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair='+market+'&interval='+tick_interval+'&limit='+tick_limit
            data_gateio = requests.get(url).json()
            df = pd.DataFrame(data_gateio)
            df.columns = ['Open time','Quote asset volume','Close','High','Low','Open','Volume']
            df = df.astype(float)
            df = add_target(df,period)
            df = add_indicators(df)
            df = df.dropna(axis='index', how='any')

            price = df.iloc[-1][2] #значение Close в последней строке  

    #    df.to_csv('gate_io_klines_'+tick_interval+'_'+tick_limit+'.csv', sep='\t', encoding='utf-8', index=False)

            what_time = np.asarray(df.iloc[:,0])#только столбец Open time, берем пока не дропнули

            df.drop(['Open time'], axis=1, inplace=True)
        #отдельяем столбец с целевым значением от остальной таблицы с данными
            X_class = np.asarray(df.iloc[:,~df.columns.isin(['Target'])]) #все кроме столбца Target
        #Y_class = np.asarray(df.iloc[:,0]).reshape(-1, 1)   #если reshape то будут проблемы с отрисовкой графиков распределения значений в наборах
            Y_class = np.asarray(df.iloc[:,6])#только столбец Target

            mean_X = X_class.mean(axis=0)
            std_X = X_class.std(axis=0)

            X_class_std = X_class - mean_X
            X_class_std = X_class_std / std_X
            X_class = X_class_std

            folder = ''

            model_json=folder+nn_name+".json"
            model_h5=folder+nn_name+".h5"


        #загрузка структуры
            json_file = open(model_json, "r")
            loaded_model_json = json_file.read()
            json_file.close()

            model2 = model_from_json(loaded_model_json)
        # загрузка весов
            model2.load_weights(model_h5)
            model = Model(model2.input, model2.layers[-1].output)
            model.trainable = True

            pred = model.predict(X_class) 
            lastpredict = pred[-1] #pred - массив Numpy
            newpredict = Predict_grow.objects.create()
            newpredict.pair = market
            newpredict.nn = nn_name
            newpredict.period = period_predict
    #    lastpredict = df2.iloc[-1][1]   #значение ячейки последней строки во втором столбце
            lastpredict = float(lastpredict)
            lastpredict = round (lastpredict, 3) #округляем до трех знаков после запятой
            newpredict.value = lastpredict
            newpredict.price = price
            newpredict.trueorfalse = None
            newpredict.save()
        except:
            now = datetime.now()
            print('get from gateio and predict ERROR: ' + str(now))
            time.sleep(60)#если ошибка выводим в консольвремя ошибки, ждем 60 секунд и с помощью continue заново входим в цикл while, если ошибки небыло - выходим из цикла while с помощью break
            continue
        break
 


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


#--------------------------------- 1d прогноз каждый 1 час -------------------------------------------
schedule.every().hour.at(":01").do(get_from_gateio, 'TONCOIN_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'TONCOIN_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'TONCOIN_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)

schedule.every().hour.at(":01").do(get_from_gateio, 'BTC_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'BTC_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'BTC_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)

schedule.every().hour.at(":01").do(get_from_gateio, 'ETH_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'ETH_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'ETH_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)

schedule.every().hour.at(":01").do(get_from_gateio, 'BNB_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'BNB_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'BNB_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)

schedule.every().hour.at(":01").do(get_from_gateio, 'DOGE_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'DOGE_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'DOGE_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)

schedule.every().hour.at(":01").do(get_from_gateio, 'ADA_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'ADA_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'ADA_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)

schedule.every().hour.at(":01").do(get_from_gateio, 'TRX_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'TRX_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'TRX_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)

schedule.every().hour.at(":01").do(get_from_gateio, 'XRP_USDT', '1h', '200', 'gateio_v1_roma', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'XRP_USDT', '1h', '200', 'gateio_v1_dasha', '1d', 24)
schedule.every().hour.at(":01").do(get_from_gateio, 'XRP_USDT', '1h', '200', 'gateio_v1_alisa', '1d', 24)


#--------------------------------- 1h прогноз каждые 5 минут -------------------------------------------
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'TONCOIN_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'TONCOIN_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'TONCOIN_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

schedule.every(5).minutes.at(":01").do(get_from_gateio, 'BTC_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'BTC_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'BTC_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

schedule.every(5).minutes.at(":01").do(get_from_gateio, 'ETH_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'ETH_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'ETH_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

schedule.every(5).minutes.at(":01").do(get_from_gateio, 'BNB_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'BNB_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'BNB_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

schedule.every(5).minutes.at(":01").do(get_from_gateio, 'DOGE_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'DOGE_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'DOGE_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

schedule.every(5).minutes.at(":01").do(get_from_gateio, 'ADA_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'ADA_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'ADA_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

schedule.every(5).minutes.at(":01").do(get_from_gateio, 'TRX_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'TRX_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'TRX_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

schedule.every(5).minutes.at(":01").do(get_from_gateio, 'XRP_USDT', '5m', '200', 'gateio_v1_roma', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'XRP_USDT', '5m', '200', 'gateio_v1_dasha', '1h', 12)
schedule.every(5).minutes.at(":01").do(get_from_gateio, 'XRP_USDT', '5m', '200', 'gateio_v1_alisa', '1h', 12)

#--------------------------------- 7d прогноз каждый 1 день -------------------------------------------
schedule.every().day.at("00:01").do(get_from_gateio, 'TONCOIN_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'TONCOIN_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'TONCOIN_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

schedule.every().day.at("00:01").do(get_from_gateio, 'BTC_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'BTC_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'BTC_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

schedule.every().day.at("00:01").do(get_from_gateio, 'ETH_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'ETH_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'ETH_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

schedule.every().day.at("00:01").do(get_from_gateio, 'BNB_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'BNB_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'BNB_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

schedule.every().day.at("00:01").do(get_from_gateio, 'DOGE_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'DOGE_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'DOGE_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

schedule.every().day.at("00:01").do(get_from_gateio, 'ADA_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'ADA_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'ADA_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

schedule.every().day.at("00:01").do(get_from_gateio, 'TRX_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'TRX_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'TRX_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

schedule.every().day.at("00:01").do(get_from_gateio, 'XRP_USDT', '8h', '200', 'gateio_v1_roma', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'XRP_USDT', '8h', '200', 'gateio_v1_dasha', '7d', 21)
schedule.every().day.at("00:01").do(get_from_gateio, 'XRP_USDT', '8h', '200', 'gateio_v1_alisa', '7d', 21)

#schedule.every().day.at("14:29").do(get_from_gateio, 'ETH_USDT', '1h', '200', 'gateio_v1_roma', '24h')
#schedule.every().day.at("14:29").do(get_from_gateio, 'ETH_USDT', '1h', '200', 'gateio_v1_dasha', '24h')
#schedule.every().day.at("14:29").do(get_from_gateio, 'ETH_USDT', '1h', '200', 'gateio_v1_alisa', '24h')

schedule.every(5).minutes.at(":02").do(check_predict_true_or_false, '1h')
schedule.every().hour.at(":02").do(check_predict_true_or_false, '1d')
schedule.every().day.at("00:02").do(check_predict_true_or_false, '7d')


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

      
