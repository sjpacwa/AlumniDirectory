from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404
from .models import Business, Alumni
<<<<<<< HEAD
from django.views.generic import ModelForm
=======
from django.forms import ModelForm
from django.contrib.auth import authenticate
>>>>>>> 60056dfde23b0972686ec839804d0a846edd607d
# Create your views here.


def index(request):
	return render(request, 'directory/index.html')

#Patric
class SubmitView(ModelForm):
	template_name = 'submit.html'

	def get_context_data(self, **kwargs):
		context = super(SubmitView, self).get_context_data(**kwargs)
		context['business'] = Business.objects.all()
		context['alumni'] = Alumni.objects.all()
		return context

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