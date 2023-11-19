from django.contrib import admin
from django.urls import path

from catalog import views


urlpatterns = [
     path('', views.index, name='index'),
     path('books/', views.books, name='books'),
     path('report/', views.report, name='report'),
     path('download_report/', views.download_report, name='download_report'),
]
