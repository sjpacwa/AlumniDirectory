from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
# Create your views here.


def index(request):
	return render(request, 'directory/index.html')

#Patric
def submit(request):
	return render(request, 'directory/submit.html')

def detail(request):
	return render(request, 'directory/detail.html')

def search(request):
	return render(request, 'directory/search.html')

def statistics(request):
	return render(request, 'directory/statistics.html')

def login(request):
	return render(request, 'directory/login.html')

def approve(request):
	return render(request, 'directory/approve.html')
