from django.shortcuts import render, redirect
from . models import Predict_grow, Coins



# Create your views here.


def coin_view(request, coin):
    spirit_list = ['fire','water', 'earth', 'air']
    try:
        token = Coins.objects.get(tiker=coin)
        tokenpair = token.pair
        predicts = Predict_grow.objects.filter(period = '1h').filter(nn__icontains = 'fire').filter(pair = tokenpair)   #берем только 1H и только по одной NN чтоб не дублировать цены, так как нам нужно получить график цен
        j = predicts.count()
        xxxx = [0] * j #будет список списков (датавремя, цена),
        zzzz = [0] * j
        j2 = 0
        for i in predicts:
            xxxx[j2] = str(i.time_close) #в тимплейте в скрипте vue при передаче списка не забудь добавить safe, потому что javascript не понравятся ковычки - вот так например {{ xxxx|safe }}
            zzzz[j2] = i.price
            j2 = j2 + 1
       
        
        
        return render(request, 'coin.html', {'token': token,
            'xxxx': xxxx, 'zzzz': zzzz,
            })
    except:
        return redirect ('/')    
    

def spirit_view(request, spirit):
    spirit_list = ['fire','water', 'earth', 'air']
    if spirit in spirit_list:

    
        tokens = Coins.objects.all()
        
        #таблица с прогнозами по каждой монете за каждый период
        j = tokens.count()
        list1 = [0] * j #будет список списков (токены из таблицы Cions),
        j2 = 0
        list_period = ['1h','1d','7d']
        
        for i in tokens:
            list1[j2] = [i.name, i.tiker, i.logo]
            tokenpair = i.pair
            for period in list_period:
                my_filter = {}
                my_filter['period'] = period
                my_filter['nn__icontains'] = spirit
                my_filter['pair'] = tokenpair
                try:
                    predict = Predict_grow.objects.filter(**my_filter).last().value
                except:
                    predict = None
                list1[j2].append(predict)   #добавляем значение predict в конец списка
            j2 = j2 + 1   



        #для графика с процентом правильности прогнозов по периодам
        true_count_1h = Predict_grow.objects.filter(period = '1h').filter(trueorfalse = True).filter(nn__icontains = spirit).count()
        false_count_1h = Predict_grow.objects.filter(period = '1h').filter(trueorfalse = False).filter(nn__icontains = spirit).count()
        try:
            percent_1h = true_count_1h / (true_count_1h + false_count_1h)
        except:
            percent_1h = 'Dontknow'  
        
        true_count_1d = Predict_grow.objects.filter(period = '1d').filter(trueorfalse = True).filter(nn__icontains = spirit).count()
        false_count_1d = Predict_grow.objects.filter(period = '1d').filter(trueorfalse = False).filter(nn__icontains = spirit).count()
        try:
            percent_1d = true_count_1d / (true_count_1d + false_count_1d)
        except:
            percent_1d = 'Dontknow'  
            
        true_count_7d = Predict_grow.objects.filter(period = '7d').filter(trueorfalse = True).filter(nn__icontains = spirit).count()
        false_count_7d = Predict_grow.objects.filter(period = '7d').filter(trueorfalse = False).filter(nn__icontains = spirit).count()
        try:
            percent_7d = true_count_7d / (true_count_7d + false_count_7d)
        except:
            percent_7d = 'Dontknow'        
    
    
    
    
    
        #процент правильности прогнозов каждого токена по периодам
        list2 = [0] * j #будет список списков (токены из таблицы Cions),
        j3 = 0
        for i in tokens:
            list2[j3] = [i.name, i.tiker, i.logo]
            tokenpair = i.pair            
            
            true_count_1h_token = Predict_grow.objects.filter(period = '1h').filter(trueorfalse = True).filter(nn__icontains = spirit).filter(pair = tokenpair).count()
            false_count_1h_token = Predict_grow.objects.filter(period = '1h').filter(trueorfalse = False).filter(nn__icontains = spirit).filter(pair = tokenpair).count()
            try:
                percent_1h_token = true_count_1h_token / (true_count_1h_token + false_count_1h_token)
            except:
                percent_1h_token = 'Dontknow'  
            list2[j3].append(percent_1h_token)
            
            true_count_1d_token = Predict_grow.objects.filter(period = '1d').filter(trueorfalse = True).filter(nn__icontains = spirit).filter(pair = tokenpair).count()
            false_count_1d_token = Predict_grow.objects.filter(period = '1d').filter(trueorfalse = False).filter(nn__icontains = spirit).filter(pair = tokenpair).count()
            try:
                percent_1d_token = true_count_1d_token / (true_count_1d_token + false_count_1d_token)
            except:
                percent_1d_token = 'Dontknow'  
            list2[j3].append(percent_1d_token)
            
            true_count_7d_token = Predict_grow.objects.filter(period = '7d').filter(trueorfalse = True).filter(nn__icontains = spirit).filter(pair = tokenpair).count()
            false_count_7d_token = Predict_grow.objects.filter(period = '7d').filter(trueorfalse = False).filter(nn__icontains = spirit).filter(pair = tokenpair).count()
            try:
                percent_7d_token = true_count_7d_token / (true_count_7d_token + false_count_7d_token)
            except:
                percent_7d_token = 'Dontknow'        
            list2[j3].append(percent_7d_token)
            j3 = j3 + 1
        
        
    
        return render(request, 'spirit.html', {'spirit': spirit,
        'list1': list1,
        'true_count_1h': true_count_1h, 'false_count_1h': false_count_1h,
        'true_count_1d': true_count_1d, 'false_count_1d': false_count_1d,
        'true_count_7d': true_count_7d, 'false_count_7d': false_count_7d,
        'percent_1h': percent_1h, 'percent_1d': percent_1d, 'percent_7d': percent_7d,
        'list2': list2,
        
        })

    return redirect ('/')
    
    
    
    
    
    
    

def roma_view(request):
    
    #тут пока общее количество считается по всем вомбатам
    
    true_count_1h = Predict_grow.objects.filter(period = '1h').filter(trueorfalse = True).count()
    false_count_1h = Predict_grow.objects.filter(period = '1h').filter(trueorfalse = False).count()
    percent_1h = true_count_1h / (true_count_1h + false_count_1h)
    
    true_count_1d = Predict_grow.objects.filter(period = '1d').filter(trueorfalse = True).count()
    false_count_1d = Predict_grow.objects.filter(period = '1d').filter(trueorfalse = False).count()
    percent_1d = true_count_1d / (true_count_1d + false_count_1d)

    true_count_7d = Predict_grow.objects.filter(period = '7d').filter(trueorfalse = True).count()
    false_count_7d = Predict_grow.objects.filter(period = '7d').filter(trueorfalse = False).count()
    try:
        percent_7d = true_count_7d / (true_count_7d + false_count_7d)
    except:
        percent_7d = 'Dontknow'


    return render(request, 'roma.html', {
    'percent_1h': percent_1h, 'percent_1d': percent_1d, 'percent_7d': percent_7d,

    })


    
def predict_1h_view(request):

#    TON_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'TONCOIN_USDT').last().value
#    TON_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'TONCOIN_USDT').last().value
#    TON_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'TONCOIN_USDT').last().value
 
    list_wbt = ['fire', 'water', 'earth', 'air']
    
    tokens = Coins.objects.all()
    j = tokens.count()
    list1 = [0] * j #будет список списков (токены из таблицы Cions)
    j2 = 0
    
    for i in tokens:
        list1[j2] = [i.name, i.tiker, i.logo]
        tokenpair = i.pair
        for wbt in list_wbt:
            my_filter = {}
            my_filter['period'] = '1h'
            my_filter['nn__icontains'] = wbt
            my_filter['pair'] = tokenpair
            try:
                predict = Predict_grow.objects.filter(**my_filter).last().value
            except:
                predict = None
            list1[j2].append(predict)   #добавляем значение predict в конец списка
        j2 = j2 + 1   
  
    return render(request, 'predict_1h.html', {'list1': list1,}) #передаем в шаблон словарь, в котором словарь и два списка


    
def predict_1d_view(request):

    list_wbt = ['fire', 'water', 'earth', 'air']
    
    tokens = Coins.objects.all()
    j = tokens.count()
    list1 = [0] * j #будет список списков (токены из таблицы Cions)
    j2 = 0
    
    for i in tokens:
        list1[j2] = [i.name, i.tiker, i.logo]
        tokenpair = i.pair
        for wbt in list_wbt:
            my_filter = {}
            my_filter['period'] = '1d'
            my_filter['nn__icontains'] = wbt
            my_filter['pair'] = tokenpair
            try:
                predict = Predict_grow.objects.filter(**my_filter).last().value
            except:
                predict = None
            list1[j2].append(predict)   #добавляем значение predict в конец списка
        j2 = j2 + 1   
  
    return render(request, 'predict_1d.html', {'list1': list1,}) #передаем в шаблон словарь, в котором словарь и два списка
    

  
def predict_7d_view(request):

    list_wbt = ['fire', 'water', 'earth', 'air']
    
    tokens = Coins.objects.all()
    j = tokens.count()
    list1 = [0] * j #будет список списков (токены из таблицы Cions)
    j2 = 0
    
    for i in tokens:
        list1[j2] = [i.name, i.tiker, i.logo]
        tokenpair = i.pair
        for wbt in list_wbt:
            my_filter = {}
            my_filter['period'] = '7d'
            my_filter['nn__icontains'] = wbt
            my_filter['pair'] = tokenpair
            try:
                predict = Predict_grow.objects.filter(**my_filter).last().value
            except:
                predict = None
            list1[j2].append(predict)   #добавляем значение predict в конец списка
        j2 = j2 + 1   
  
    return render(request, 'predict_7d.html', {'list1': list1,}) #передаем в шаблон словарь, в котором словарь и два списка
    

 