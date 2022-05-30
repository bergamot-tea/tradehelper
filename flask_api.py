from flask import Flask
from flask_restful import Api, Resource, reqparse
import requests
import pandas as pd
import numpy as np
import math
from tensorflow.keras import Input, Model
from tensorflow.keras.models import model_from_json
from datetime import datetime


app = Flask(__name__)
api = Api(app)




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


class MyClass(Resource):
    def get(self,market,tick_interval,tick_limit, period, nn_name):
        time_close = ''
        price = 0
        lastpredict = 0
        try:
            #url = 'https://api.gateio.ws/api/v4/spot/candlesticks?currency_pair='+market+'&interval='+tick_interval+'&limit='+tick_limit
            url = 'https://api.binance.com/api/v3/klines?symbol='+market+'&interval='+tick_interval+'&limit='+tick_limit
            data_gateio = requests.get(url).json()

            df = pd.DataFrame(data_gateio)
            #df.columns = ['Open time','Quote asset volume','Close','High','Low','Open','Volume']
            df.columns = ['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume','Ignore']

            time_close = df.iloc[-1][0] #значение Open time в последней строке, берем пока не отбросили NaN, оно равно значению Close time в предпоследней строке

            time_close = str(time_close)
            
            df = df.astype(float)

            df = add_target(df,period)
            df = add_indicators(df)
            df = df.dropna(axis='index', how='any')
            price = df.iloc[-1][4] #значение Close в последней строке  
            df.drop(['Ignore', 'Open time', 'Close time'], axis=1, inplace=True)
            #отдельяем столбец с целевым значением от остальной таблицы с данными
            X_class = np.asarray(df.iloc[:,~df.columns.isin(['Target'])]) #все кроме столбца Target
            #Y_class = np.asarray(df.iloc[:,0]).reshape(-1, 1)   #если reshape то будут проблемы с отрисовкой графиков распределения значений в наборах
            Y_class = np.asarray(df.iloc[:,9])#только столбец Target

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
            lastpredict = float(lastpredict)
            lastpredict = round(lastpredict, 3) #округляем до трех знаков после запятой
        except:
            now = datetime.now()
            print('error in function get()', now)

        
        return time_close, price, lastpredict, 200


api.add_resource(MyClass, "/<market>_<tick_interval>_<tick_limit>_<int:period>_<nn_name>")


if __name__ == '__main__':
    app.run(debug=False)
