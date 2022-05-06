from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout



def home_view(request):

          
    return render(request, 'index.html')



          