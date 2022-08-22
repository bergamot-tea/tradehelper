from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

import random
import os

def home_view(request):
    
    folder = 'static/img/comics/'
    files = os.listdir(folder)
    comics = random.choice(files)
          
    return render(request, 'index.html', {'comics': comics,})



          