"""NewsPaper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from allauth.account import views
from accounts.views import subscriptions
from NPbd.views import PostViewSet

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n'), name='lang'),
    path('', views.login),
    path('profile/', include('accounts.urls_profile')),
    path('admin/', admin.site.urls),
    path('paged/', include('django.contrib.flatpages.urls')),
    path('news/', include('NPbd.urls_news')),
    path('articles/', include('NPbd.urls_articles')),
    path('accounts/', include('allauth.urls')),
    path('subscription/', subscriptions, name='subscriptions'),
    path('api/v1/posts/', PostViewSet.as_view()),
    path('api/v1/posts/<int:pk>', PostViewSet.as_view()),
]
