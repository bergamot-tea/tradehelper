from django.shortcuts import render
from . models import Predict_grow, Coins



# Create your views here.


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

    TON_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'TONCOIN_USDT').last().value
    TON_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'TONCOIN_USDT').last().value
    TON_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'TONCOIN_USDT').last().value
    
    BTC_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'BTC_USDT').last().value
    BTC_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'BTC_USDT').last().value
    BTC_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'BTC_USDT').last().value
    
    ETH_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'ETH_USDT').last().value
    ETH_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'ETH_USDT').last().value
    ETH_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'ETH_USDT').last().value
    
    BNB_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'BNB_USDT').last().value
    BNB_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'BNB_USDT').last().value
    BNB_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'BNB_USDT').last().value
    
    DOGE_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'DOGE_USDT').last().value
    DOGE_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'DOGE_USDT').last().value
    DOGE_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'DOGE_USDT').last().value
    
    ADA_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'ADA_USDT').last().value
    ADA_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'ADA_USDT').last().value
    ADA_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'ADA_USDT').last().value
    
    TRX_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'TRX_USDT').last().value
    TRX_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'TRX_USDT').last().value
    TRX_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'TRX_USDT').last().value
    
    XRP_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1h').filter(pair = 'XRP_USDT').last().value
    XRP_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1h').filter(pair = 'XRP_USDT').last().value
    XRP_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1h').filter(pair = 'XRP_USDT').last().value
    
    return render(request, 'predict_1h.html', {
    'TON_roma': TON_roma, 'TON_dasha': TON_dasha, 'TON_alisa': TON_alisa, 
    'BTC_roma': BTC_roma, 'BTC_dasha': BTC_dasha, 'BTC_alisa': BTC_alisa, 
    'ETH_roma': ETH_roma, 'ETH_dasha': ETH_dasha, 'ETH_alisa': ETH_alisa, 
    'BNB_roma': BNB_roma, 'BNB_dasha': BNB_dasha, 'BNB_alisa': BNB_alisa, 
    'DOGE_roma': DOGE_roma, 'DOGE_dasha': DOGE_dasha, 'DOGE_alisa': DOGE_alisa, 
    'ADA_roma': ADA_roma, 'ADA_dasha': ADA_dasha, 'ADA_alisa': ADA_alisa, 
    'TRX_roma': TRX_roma, 'TRX_dasha': TRX_dasha, 'TRX_alisa': TRX_alisa, 
    'XRP_roma': XRP_roma, 'XRP_dasha': XRP_dasha, 'XRP_alisa': XRP_alisa,
    })


    
def predict_1d_view(request):

    TON_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'TONCOIN_USDT').last().value
    TON_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'TONCOIN_USDT').last().value
    TON_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'TONCOIN_USDT').last().value
    
    BTC_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'BTC_USDT').last().value
    BTC_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'BTC_USDT').last().value
    BTC_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'BTC_USDT').last().value
    
    ETH_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'ETH_USDT').last().value
    ETH_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'ETH_USDT').last().value
    ETH_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'ETH_USDT').last().value
    
    BNB_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'BNB_USDT').last().value
    BNB_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'BNB_USDT').last().value
    BNB_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'BNB_USDT').last().value
    
    DOGE_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'DOGE_USDT').last().value
    DOGE_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'DOGE_USDT').last().value
    DOGE_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'DOGE_USDT').last().value
    
    ADA_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'ADA_USDT').last().value
    ADA_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'ADA_USDT').last().value
    ADA_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'ADA_USDT').last().value
    
    TRX_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'TRX_USDT').last().value
    TRX_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'TRX_USDT').last().value
    TRX_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'TRX_USDT').last().value
    
    XRP_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '1d').filter(pair = 'XRP_USDT').last().value
    XRP_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '1d').filter(pair = 'XRP_USDT').last().value
    XRP_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '1d').filter(pair = 'XRP_USDT').last().value
    
    return render(request, 'predict_1d.html', {
    'TON_roma': TON_roma, 'TON_dasha': TON_dasha, 'TON_alisa': TON_alisa, 
    'BTC_roma': BTC_roma, 'BTC_dasha': BTC_dasha, 'BTC_alisa': BTC_alisa, 
    'ETH_roma': ETH_roma, 'ETH_dasha': ETH_dasha, 'ETH_alisa': ETH_alisa, 
    'BNB_roma': BNB_roma, 'BNB_dasha': BNB_dasha, 'BNB_alisa': BNB_alisa, 
    'DOGE_roma': DOGE_roma, 'DOGE_dasha': DOGE_dasha, 'DOGE_alisa': DOGE_alisa, 
    'ADA_roma': ADA_roma, 'ADA_dasha': ADA_dasha, 'ADA_alisa': ADA_alisa, 
    'TRX_roma': TRX_roma, 'TRX_dasha': TRX_dasha, 'TRX_alisa': TRX_alisa, 
    'XRP_roma': XRP_roma, 'XRP_dasha': XRP_dasha, 'XRP_alisa': XRP_alisa,
    })
    

  
def predict_7d_view(request):

    TON_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'TONCOIN_USDT').last().value
    TON_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'TONCOIN_USDT').last().value
    TON_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'TONCOIN_USDT').last().value
    
    BTC_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'BTC_USDT').last().value
    BTC_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'BTC_USDT').last().value
    BTC_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'BTC_USDT').last().value
    
    ETH_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'ETH_USDT').last().value
    ETH_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'ETH_USDT').last().value
    ETH_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'ETH_USDT').last().value
    
    BNB_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'BNB_USDT').last().value
    BNB_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'BNB_USDT').last().value
    BNB_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'BNB_USDT').last().value
    
    DOGE_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'DOGE_USDT').last().value
    DOGE_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'DOGE_USDT').last().value
    DOGE_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'DOGE_USDT').last().value
    
    ADA_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'ADA_USDT').last().value
    ADA_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'ADA_USDT').last().value
    ADA_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'ADA_USDT').last().value
    
    TRX_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'TRX_USDT').last().value
    TRX_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'TRX_USDT').last().value
    TRX_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'TRX_USDT').last().value
    
    XRP_roma = Predict_grow.objects.filter(nn__icontains = 'roma').filter(period = '7d').filter(pair = 'XRP_USDT').last().value
    XRP_dasha = Predict_grow.objects.filter(nn__icontains = 'dasha').filter(period = '7d').filter(pair = 'XRP_USDT').last().value
    XRP_alisa = Predict_grow.objects.filter(nn__icontains = 'alisa').filter(period = '7d').filter(pair = 'XRP_USDT').last().value
    
    return render(request, 'predict_7d.html', {
    'TON_roma': TON_roma, 'TON_dasha': TON_dasha, 'TON_alisa': TON_alisa, 
    'BTC_roma': BTC_roma, 'BTC_dasha': BTC_dasha, 'BTC_alisa': BTC_alisa, 
    'ETH_roma': ETH_roma, 'ETH_dasha': ETH_dasha, 'ETH_alisa': ETH_alisa, 
    'BNB_roma': BNB_roma, 'BNB_dasha': BNB_dasha, 'BNB_alisa': BNB_alisa, 
    'DOGE_roma': DOGE_roma, 'DOGE_dasha': DOGE_dasha, 'DOGE_alisa': DOGE_alisa, 
    'ADA_roma': ADA_roma, 'ADA_dasha': ADA_dasha, 'ADA_alisa': ADA_alisa, 
    'TRX_roma': TRX_roma, 'TRX_dasha': TRX_dasha, 'TRX_alisa': TRX_alisa, 
    'XRP_roma': XRP_roma, 'XRP_dasha': XRP_dasha, 'XRP_alisa': XRP_alisa,
    })
    

 