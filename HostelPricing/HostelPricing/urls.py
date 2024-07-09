from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('calculate_price/', views.calculate_price, name='calculate_price'),
    path('viewDatabase/', views.viewDatabase, name='viewDatabase'),
    path('updateDatabase/', views.updateDatabase, name = 'updateDatabase'),
]



