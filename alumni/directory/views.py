from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from .models import Business, Alumni
from .forms import BusinessForm, AlumniForm
from django.contrib.auth import authenticate
# Create your views here.


def index(request):
	return render(request, 'directory/index.html')

#Patric
def submit(request):
	form = BusinessForm()
	form2 = AlumniForm()
	return render(request, 'directory/submit.html', {'form1': form, 'form2': form2})

def detail(request):
	return render(request, 'directory/detail.html')

def search(request):
	found_entries = list(Businesses.objects.filter(business_approved=True))
	return render(request, 'directory/search.html')

def login(request):
	
	return render(request, 'directory/login.html')

def approve(request):
	user = authenticate(username='admin', password='default')
	if user is not None:
		method_return = render(request, 'directory/approve.html')
	else:
		method_return = HttpResponseForbidden("403 - Forbidden")

	return method_return

def statistics(request):
	user = authenticate(username='fsd', password='default')
	if user is not None:
		method_return = render(request, 'directory/statistics.html')
	else:
		method_return = HttpResponseForbidden("403 - Forbidden")
	
	return method_return