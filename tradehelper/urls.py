"""tradehelper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . views import home_view
from helperapp.views import predict_1h_view, predict_1d_view, predict_7d_view, roma_view, spirit_view, coin_view, allcoins_view
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home_page'),
#    path('helper/', include('helperapp.urls')),
    path('predict/hour/', predict_1h_view, name='predict_1h_page'),
    path('predict/day/', predict_1d_view, name='predict_1d_page'),
    path('predict/week/', predict_7d_view, name='predict_7d_page'),
    path('roma/', roma_view, name='roma_page'),
    path('coins/', allcoins_view, name='allcoins_page'),
    path('coins/<coin>/', coin_view, name='coin_page'),
    path('<spirit>/', spirit_view, name='spirit_page'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

