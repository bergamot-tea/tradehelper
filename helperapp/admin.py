from django.contrib import admin

# Register your models here.

from .models import Klines, Predict_grow

class Predict_growAdmin(admin.ModelAdmin):
    
    fields = ('pair', 'nn', 'period', 'value', 'price', 'trueorfalse')
    list_display = ['id', 'time', 'pair', 'nn', 'period', 'value', 'price', 'trueorfalse']


admin.site.register(Klines)
admin.site.register(Predict_grow, Predict_growAdmin)