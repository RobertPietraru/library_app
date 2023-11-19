from django.http import HttpResponse
from django.db.models import Q
from django.shortcuts import render

from catalog.models import Book, BookInstance

# Create your views here.


def home(request):
    return HttpResponse('<a href=\'{% url \'books\' %}\'>Catalog</a>')

