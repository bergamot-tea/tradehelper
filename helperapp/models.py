from django.db import models

# Create your models here.



class Klines(models.Model):
    
    pair = models.CharField(max_length=50, blank=True)
    period = models.CharField(max_length=50, blank=True)
    opentime = models.DateTimeField(blank=True)
    open = models.FloatField(blank=True)
    high = models.FloatField(blank=True)
    low = models.FloatField(blank=True)
    close = models.FloatField(blank=True)
    volume = models.FloatField(blank=True)
    closetime = models.DateTimeField(blank=True)
    q_a_s = models.FloatField(blank=True)   #Quote asset volume
    n_a_t = models.PositiveIntegerField(blank=True) #Number of trades
    t_b_b = models.FloatField(blank=True) #Taker buy base asset volume
    t_b_q = models.FloatField(blank=True) #Taker buy quote asset volume
    ignore = models.PositiveIntegerField(blank=True)
    predict24h = models.FloatField(blank=True)  #предсказанная вероятность того что повысится цена закрытия через 24 часа



class Predict_grow(models.Model):
    time = models.DateTimeField(auto_now_add=True, blank=True)
    pair = models.CharField(max_length=50, blank=True)      #например ETH_USDT
    nn = models.CharField(max_length=250, blank=True)       #название нейронной сети (название файла)
    period = models.CharField(max_length=50, blank=True)    #через какой период предсказание
    value = models.FloatField(blank=True, null=True)        #вероятность роста, значение от 0 до 1
    price = models.FloatField(blank=True, null=True)        #цена на момент прогноза (текущая цена)
    trueorfalse = models.BooleanField(blank=True, null=True)#сбылось или нет