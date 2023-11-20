from django.contrib import admin
from django.urls import path

from catalog import views


urlpatterns = [
     path('', views.index, name='index'),
     path('books/', views.books, name='books'),
     path('report/', views.report, name='report'),
     path('download_report/', views.download_report, name='download_report'),
     path('my_books/', views.my_books, name='my_books'),
     path('return/<uuid:id>/', views.return_book, name='return_book'),
     path('borrow/<uuid:id>/', views.borrow_book, name='borrow_book'),
     path('verify/<str:username>/', views.verify_user, name='verify_user'),
     path('unverify/<str:username>/', views.unverify_user, name='unverify_user'),
     path('not_verified/', views.not_verified, name='not_verified'),
]
