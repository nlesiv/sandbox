from django.shortcuts import render
from django.http import HttpResponse
import datetime
# Create your views here.

def display(request):
    return HttpResponse("<h1>My First Django App!!</h1>")

def displayDateTime(request):
    dt=datetime.datetime.now()
    s ="<b>Current date and time: </b>"+str(dt);
    return HttpResponse(s);