from django.contrib import admin

# Register your models here.

from .models import Klines, Predict_grow, Coins

class Predict_growAdmin(admin.ModelAdmin):
    
    fields = ('pair', 'nn', 'period', 'value', 'price', 'trueorfalse', 'time_close')
    list_display = ['id', 'time', 'pair', 'nn', 'period', 'value', 'price', 'trueorfalse', 'time_close']

class CoinsAdmin(admin.ModelAdmin):
    
    fields = ('name', 'tiker', 'pair', 'logo')
    list_display = ['id', 'name', 'tiker', 'pair', 'logo']

admin.site.register(Klines)
admin.site.register(Predict_grow, Predict_growAdmin)
admin.site.register(Coins, CoinsAdmin)