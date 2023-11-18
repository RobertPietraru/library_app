from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.

def catalog(_):
    return HttpResponse("HEEy");
