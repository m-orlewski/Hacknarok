from django.shortcuts import render

def index(request):
    return render(request, 'webserver/index.html')

def create(request):
    return render(request, 'webserver/create.html')
