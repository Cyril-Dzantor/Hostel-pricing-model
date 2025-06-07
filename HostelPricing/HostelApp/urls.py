from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('calculate_price/', views.calculate_price, name='calculate_price'),
    path('viewDatabase/', views.viewDatabase, name='viewDatabase'),
    path('updateDatabase/', views.updateDatabase, name = 'updateDatabase'),
    path('ViewAbout/', views.ViewAbout, name="ViewAbout" ),
    path('ViewHelp/', views.ViewHelp, name='ViewHelp'),
    path('recommend/', views.recommend_hostels, name='recommend_hostels'),
]



