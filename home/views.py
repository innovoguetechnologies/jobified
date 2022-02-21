from django.shortcuts import render
from django.http import  HttpResponse

def homeView(request):
	return render(request, 'home/home.html')

def aboutView(request):
	return HttpResponse("About")

def dashboardView(request):
	return render(request, 'home/dashboard.html')
