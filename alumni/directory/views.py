from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect
from .models import Business, Alumni
from .forms import BusinessForm, AlumniForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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

def log_in(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		# User is authenticated, redirect to approve.
		login(request, user)
		return HttpResponseRedirect('/directory/office/approve/')
	elif username is not '' or password is not '':
		# Incorrect login, update error_message.
		return render(request, 'directory/login.html', {
			'error_message': "Incorrect username/password."
			})

	return render(request, 'directory/login.html')

@login_required
def approve(request):
	query_set = Business.objects.filter(business_approved=False)
	print(list(query_set))

	return render(request, 'directory/approve.html', {'query': query_set})

@login_required
def statistics(request):
	return render(request, 'directory/statistics.html')

@login_required
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/directory/office/login/')

@login_required
def approve_deny(request):
	# Iterate through data other than CRSF token.
	print(request.POST)
	for choice in list(request.POST.items())[1:]:
		# Fetch the relevant business and alumni from database.
		business = Business.objects.get(id=choice[0])
		alumni = Alumni.objects.get(id=business.business_alumni_id)
		
		if choice[1] in ['approve']:
			business.business_approved = True
			alumni.alumni_approved = True
			business.save()
			alumni.save()
		elif choice[1] in ['deny']:
			alumni.delete()
			business.delete()

	return HttpResponseRedirect('/directory/office/approve/')