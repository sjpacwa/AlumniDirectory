from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Business, Alumni
from django.forms import ModelForm
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
	return render(request, 'directory/search.html')

def statistics(request):
	return render(request, 'directory/statistics.html')

def login(request):
	return render(request, 'directory/login.html')

def approve(request):
	return render(request, 'directory/approve.html')
