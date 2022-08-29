from django.shortcuts import render, redirect
from . models import Predict_grow, Coins
from datetime import datetime, timedelta





def check_delta_price (tokenpair):

    timenow = datetime.now()
    time_1h_early = timenow - timedelta(hours = 1)  #определяем значение времени которое было час назад
    time_1d_early = timenow - timedelta(days = 1)
    time_7d_early = timenow - timedelta(days = 7)
            
    last_price = Predict_grow.objects.filter(period = '1h').filter(pair = tokenpair).last().price

    try:
        price_1h_early = Predict_grow.objects.filter(pair = tokenpair).filter(time__lte = time_1h_early).last().price
        delta_1h_percent = ((last_price - price_1h_early)/price_1h_early)*100
        delta_1h_percent = round(delta_1h_percent,1)
    except:
        delta_1h_percent = ':('
        
     
    try:
        price_1d_early = Predict_grow.objects.filter(pair = tokenpair).filter(time__lte = time_1d_early).last().price
        delta_1d_percent = ((last_price - price_1d_early)/price_1d_early)*100
        delta_1d_percent = round(delta_1d_percent,1)
    except:
        delta_1d_percent = ':('

    try:
        price_7d_early = Predict_grow.objects.filter(pair = tokenpair).filter(time__lte = time_7d_early).last().price
        delta_7d_percent = ((last_price - price_7d_early)/price_7d_early)*100
        delta_7d_percent = round(delta_7d_percent,1)
    except:
        delta_7d_percent = ':('

    list_delta_price = [delta_1h_percent, delta_1d_percent, delta_7d_percent]
    
    return(list_delta_price)


def about_view(request):
 
    return render(request, 'about.html', )  

def donate_view(request):
 
    return render(request, 'donate.html', )  


# Create your views here.

def allcoins_view(request):
 
   # list_wbt = ['fire', 'water', 'earth', 'air']
    
    tokens = Coins.objects.all()
    j = tokens.count()
    list1 = [0] * j #будет список списков (токены из таблицы Cions)
    j2 = 0
    
    for i in tokens:
        list1[j2] = [i.name, i.tiker, i.logo]
        tokenpair = i.pair
        
        my_filter = {}
        my_filter['period'] = '1h'
        my_filter['pair'] = tokenpair
        try:
            price = Predict_grow.objects.filter(**my_filter).last().price
        except:
            price = 0 #если сделать None а не 0 то при добавлении новых токенов в базу страница всех криптовалют не будет открываться 
        list1[j2].append(price)   #добавляем значение predict в конец списка
        
        list_delta_price = check_delta_price(tokenpair)
        list1[j2].extend(list_delta_price)
        
        j2 = j2 + 1   
  
    return render(request, 'allcoins.html', {'list1': list1,})  



def coin_view(request, coin):
    
       
    
    timenow = datetime.now()
    time_7d_early = timenow - timedelta(days = 7)
    time_1d_early = timenow - timedelta(days = 1)
    time_30d_early = timenow - timedelta(days = 30)
    
    expert_list = ['fire','water', 'earth', 'air']
    try:
        token = Coins.objects.get(tiker=coin)
        tokenpair = token.pair
         
        
        
        
        #--------------шкала даты время для графика цены---------

         
        predicts_fire = Predict_grow.objects.filter(period = '1h').filter(time__gte = time_7d_early).filter(nn__icontains = 'fire').filter(pair = tokenpair).order_by('id')   #берем только 1H и только по одной NN чтоб не дублировать цены, так как нам нужно получить график цен
        j = predicts_fire.count()
        xxxx = [0] * j #будет список c датами-временем часовых предиктов 
        
        #----------------список цена и изменения Ч Д Н----------
        list_price = []#----------------список цена и изменения Ч Д Н
        last_pr = predicts_fire.last().price
        list_price.append(last_pr)
        list_delta_price = check_delta_price(tokenpair)
        list_price.extend(list_delta_price)
               
        
        #--------------получаем список c датами-временем дневных предиктов за неделю 
        predicts_fire_1d = Predict_grow.objects.filter(period = '1d').filter(time__gte = time_7d_early).filter(nn__icontains = 'fire').filter(pair = tokenpair).order_by('id')
        сount_1d = predicts_fire_1d.count()
        xxxx_1d = [0] * сount_1d #будет список c датами-временем предиктов
        j8 = 0
        for i in predicts_fire_1d:
            time_msk = i.time_close + timedelta(hours=6)    #чтоб на странице отображалось не UTC(как в базе), а UTC+3 (Московское) 
            str_time = str(time_msk)
            xxxx_1d[j8] = str_time[:-9]  # удаляем лишнюю точность времени(последние 9 символов строки) #в тимплейте в скрипте vue при передаче списка не забудь добавить safe, потому что javascript не понравятся ковычки - вот так например {{ xxxx|safe }}
            j8 = j8 + 1    


        #--------------получаем список c датами-временем часовых предиктов за день
        predicts_fire_1h = Predict_grow.objects.filter(period = '1h').filter(time__gte = time_1d_early).filter(nn__icontains = 'fire').filter(pair = tokenpair).order_by('id')
        сount_1h = predicts_fire_1h.count()
        xxxx_1h = [0] * сount_1h #будет список c датами-временем предиктов
        j9 = 0
        for i in predicts_fire_1h:
            time_msk = i.time_close + timedelta(hours=6)    #чтоб на странице отображалось не UTC(как в базе), а UTC+3 (Московское) 
            str_time = str(time_msk)
            xxxx_1h[j9] = str_time[:-9]  # удаляем лишнюю точность времени(последние 9 символов строки) #в тимплейте в скрипте vue при передаче списка не забудь добавить safe, потому что javascript не понравятся ковычки - вот так например {{ xxxx|safe }}
            j9 = j9 + 1 
            
        #--------------получаем список c датами-временем недельных предиктов за месяц
        predicts_fire_7d = Predict_grow.objects.filter(period = '7d').filter(time__gte = time_30d_early).filter(nn__icontains = 'fire').filter(pair = tokenpair).order_by('id')
        сount_7d = predicts_fire_7d.count()
        xxxx_7d = [0] * сount_7d #будет список c датами-временем предиктов
        j10 = 0
        for i in predicts_fire_7d:
            time_msk = i.time_close + timedelta(hours=6)    #чтоб на странице отображалось не UTC(как в базе), а UTC+3 (Московское) 
            str_time = str(time_msk)
            xxxx_7d[j10] = str_time[:-9]  # удаляем лишнюю точность времени(последние 9 символов строки) #в тимплейте в скрипте vue при передаче списка не забудь добавить safe, потому что javascript не понравятся ковычки - вот так например {{ xxxx|safe }}
            j10 = j10 + 1             

        #------------график цены------------------
        j2 = 0
        zzzz = [0] * j #будет список с ценами
        for i in predicts_fire:
            time_msk = i.time_close + timedelta(hours=6)    #чтоб на странице отображалось не UTC(как в базе), а UTC+3 (Московское) 
            str_time = str(time_msk)
            xxxx[j2] = str_time[:-9]  # удаляем лишнюю точность времени(последние 9 символов строки) #в тимплейте в скрипте vue при передаче списка не забудь добавить safe, потому что javascript не понравятся ковычки - вот так например {{ xxxx|safe }}
            zzzz[j2] = i.price
            j2 = j2 + 1
            
            
        #--------------график часовых предиктов за день------------------------
        j3 = 0
        yyyy = [0] * 8 #будет список из восьми длинных списков: 0 - прогнозы fire за неделю, 1 - труорфолсы fire за неделю (цвета зеленый красный серый для графика), 2 - пронозы water, 3 - труорфолс water и т.д.
        for i in expert_list:
            my_filter = {}
            my_filter['period'] = '1h'
            my_filter['pair'] = tokenpair
            my_filter['time__gte'] = time_1d_early
            my_filter['nn__icontains'] = i
            predicts = Predict_grow.objects.filter(**my_filter).order_by('id')
            jj = predicts.count()
            
            wwww = [0] * jj
            j4 = 0
            for h in predicts:
                wwww[j4] = h.value
                j4 = j4 + 1
            yyyy[j3] = wwww
            
            j3 = j3 + 1
            
            wwww = [0] * jj
            j4 = 0    
            for h in predicts:
                color = ''
                if h.trueorfalse == True:
                    color = 'green'
                elif h.trueorfalse == False:
                    color = 'red'
                else:
                    color = 'gray'
                wwww[j4] = color
                j4 = j4 + 1
            yyyy[j3] = wwww
            
            j3 = j3 + 1
                
                
        #--------------график дневных предиктов за неделю------------------------        
 
        j5 = 0
        aaaa = [0] * 8 #будет список из восьми длинных списков: 0 - прогнозы fire за неделю, 1 - труорфолсы fire за неделю (цвета зеленый красный серый для графика), 2 - пронозы water, 3 - труорфолс water и т.д.
        for i in expert_list:
            
            my_filter = {}
            my_filter['period'] = '1d'
            my_filter['pair'] = tokenpair
            my_filter['time__gte'] = time_7d_early
            my_filter['nn__icontains'] = i
            predicts = Predict_grow.objects.filter(**my_filter).order_by('id')
            jj = predicts.count()
            
            wwww = [0] * jj
            j4 = 0
            for h in predicts:
                wwww[j4] = h.value
                j4 = j4 + 1
            aaaa[j5] = wwww
            
            j5 = j5 + 1
            
            wwww = [0] * jj
            j4 = 0
                        
            for h in predicts:
                color = ''
                if h.trueorfalse == True:
                    color = 'green'
                elif h.trueorfalse == False:
                    color = 'red'
                else:
                    color = 'gray'
                wwww[j4] = color
                j4 = j4 + 1
               
            aaaa[j5] = wwww
            
            j5 = j5 + 1



#--------------график недельных предиктов за месяц------------------------        
 
        j10 = 0
        bbbb = [0] * 8 #будет список из восьми длинных списков: 0 - прогнозы fire , 1 - труорфолсы fire  (цвета зеленый красный серый для графика), 2 - пронозы water, 3 - труорфолс water и т.д.
        for i in expert_list:
            
            my_filter = {}
            my_filter['period'] = '7d'
            my_filter['pair'] = tokenpair
            my_filter['time__gte'] = time_30d_early
            my_filter['nn__icontains'] = i
            predicts = Predict_grow.objects.filter(**my_filter).order_by('id')
            jj = predicts.count()
            
            wwww = [0] * jj
            j4 = 0
            for h in predicts:
                wwww[j4] = h.value
                j4 = j4 + 1
            bbbb[j10] = wwww
            
            j10 = j10 + 1
            
            wwww = [0] * jj
            j4 = 0
                        
            for h in predicts:
                color = ''
                if h.trueorfalse == True:
                    color = 'green'
                elif h.trueorfalse == False:
                    color = 'red'
                else:
                    color = 'gray'
                wwww[j4] = color
                j4 = j4 + 1
               
            bbbb[j10] = wwww
            
            j10 = j10 + 1


 
        
        return render(request, 'coin.html', {'token': token,
            'xxxx': xxxx, 'zzzz': zzzz, 'yyyy': yyyy, 'aaaa': aaaa, 'xxxx_1d': xxxx_1d, 'xxxx_1h': xxxx_1h, 'xxxx_7d': xxxx_7d, 'bbbb': bbbb, 'list_price': list_price,
          
            
            })
    except:
        return redirect ('/')    
    

def expert_view(request, expert):
    
    
#----этот кусок очень не хотелось, но пришлось написать, чтоб у экспертов были ссылки по их именам, так как из адресной строки браузера принимаем 'ilon','vitalik','satoshi','chanpen', а надо 'fire','water', 'earth', 'air'  
    if expert not in ['ilon','vitalik','satoshi','chanpen']:
        return redirect ('/')
    
    if expert in ['ilon','vitalik','satoshi','chanpen']:
        if expert == 'ilon':
            expert = 'fire'
        elif expert == 'vitalik':
            expert = 'water'
        elif expert == 'satoshi':
            expert = 'earth'
        else:
            expert = 'air'            
#--------------------------------------------------------------------------    
    
   
    expert_list = ['fire','water', 'earth', 'air']
    if expert in expert_list:
        
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
                my_filter['nn__icontains'] = expert
                my_filter['pair'] = tokenpair
                try:
                    predict = Predict_grow.objects.filter(**my_filter).last().value
                except:
                    predict = None
                list1[j2].append(predict)   #добавляем значение predict в конец списка
            j2 = j2 + 1   

        
        timenow = datetime.now()
        time_7d_early = timenow - timedelta(days = 7)
        time_1d_early = timenow - timedelta(days = 1)
        time_30d_early = timenow - timedelta(days = 30)

        #для графика с процентом правильности прогнозов по периодам
        true_count_1h = Predict_grow.objects.filter(time__gte = time_1d_early).filter(period = '1h').filter(trueorfalse = True).filter(nn__icontains = expert).count()
        false_count_1h = Predict_grow.objects.filter(time__gte = time_1d_early).filter(period = '1h').filter(trueorfalse = False).filter(nn__icontains = expert).count()
        try:
            percent_1h = true_count_1h / (true_count_1h + false_count_1h)
        except:
            percent_1h = 'Dontknow'  
        
        true_count_1d = Predict_grow.objects.filter(time__gte = time_7d_early).filter(period = '1d').filter(trueorfalse = True).filter(nn__icontains = expert).count()
        false_count_1d = Predict_grow.objects.filter(time__gte = time_7d_early).filter(period = '1d').filter(trueorfalse = False).filter(nn__icontains = expert).count()
        try:
            percent_1d = true_count_1d / (true_count_1d + false_count_1d)
        except:
            percent_1d = 'Dontknow'  
            
        true_count_7d = Predict_grow.objects.filter(time__gte = time_30d_early).filter(period = '7d').filter(trueorfalse = True).filter(nn__icontains = expert).count()
        false_count_7d = Predict_grow.objects.filter(time__gte = time_30d_early).filter(period = '7d').filter(trueorfalse = False).filter(nn__icontains = expert).count()
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
            
            true_count_1h_token = Predict_grow.objects.filter(time__gte = time_1d_early).filter(period = '1h').filter(trueorfalse = True).filter(nn__icontains = expert).filter(pair = tokenpair).count()
            false_count_1h_token = Predict_grow.objects.filter(time__gte = time_1d_early).filter(period = '1h').filter(trueorfalse = False).filter(nn__icontains = expert).filter(pair = tokenpair).count()
            try:
                percent_1h_token = 100*true_count_1h_token / (true_count_1h_token + false_count_1h_token)
                percent_1h_token = round(percent_1h_token,1)
            except:
                percent_1h_token = 'Dontknow'  
            list2[j3].append(percent_1h_token)
            
            true_count_1d_token = Predict_grow.objects.filter(time__gte = time_7d_early).filter(period = '1d').filter(trueorfalse = True).filter(nn__icontains = expert).filter(pair = tokenpair).count()
            false_count_1d_token = Predict_grow.objects.filter(time__gte = time_7d_early).filter(period = '1d').filter(trueorfalse = False).filter(nn__icontains = expert).filter(pair = tokenpair).count()
            try:
                percent_1d_token = 100*true_count_1d_token / (true_count_1d_token + false_count_1d_token)
                percent_1d_token = round(percent_1d_token,1)
            except:
                percent_1d_token = 'Dontknow'  
            list2[j3].append(percent_1d_token)
            
            true_count_7d_token = Predict_grow.objects.filter(time__gte = time_30d_early).filter(period = '7d').filter(trueorfalse = True).filter(nn__icontains = expert).filter(pair = tokenpair).count()
            false_count_7d_token = Predict_grow.objects.filter(time__gte = time_30d_early).filter(period = '7d').filter(trueorfalse = False).filter(nn__icontains = expert).filter(pair = tokenpair).count()
            try:
                percent_7d_token = 100*true_count_7d_token / (true_count_7d_token + false_count_7d_token)
                percent_7d_token = round(percent_7d_token,1)
            except:
                percent_7d_token = 'Dontknow'        
            list2[j3].append(percent_7d_token)
            j3 = j3 + 1
        
        
    
        return render(request, 'expert.html', {'expert': expert,
        'list1': list1,
#        'true_count_1h': true_count_1h, 'false_count_1h': false_count_1h,
#        'true_count_1d': true_count_1d, 'false_count_1d': false_count_1d,
#        'true_count_7d': true_count_7d, 'false_count_7d': false_count_7d,
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
  
    return render(request, 'predict_1h.html', {'list1': list1,})


    
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
  
    return render(request, 'predict_1d.html', {'list1': list1,}) 
    

  
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
  
    return render(request, 'predict_7d.html', {'list1': list1,}) 
    

 