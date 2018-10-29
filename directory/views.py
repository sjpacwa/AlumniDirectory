from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect, HttpResponseNotFound
from .models import Business, Alumni
from .forms import BusinessForm, AlumniForm, BusinessSearchForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.


def index(request):
	return render(request, 'directory/index.html')

#Patric
def submit(request):
	if request.method == "POST":
		form = AlumniForm(request.POST)
		form2 = BusinessForm(request.POST)
		if form.is_valid() and form2.is_valid():
			# Save both forms and refresh the page
			new_alumni = form.save(commit=False)
			new_alumni.author = request.user
			new_alumni.published_date = timezone.now()
			new_alumni.alumni_approved = False
			new_alumni.save()
			new_business = form2.save(commit=False)
			new_business.author = request.user
			new_business.published_date = timezone.now()
			new_business.business_num_visit = 0
			new_business.business_approved = False
			new_business.business_alumni_id = new_alumni.id
			new_business.save()
			return HttpResponseRedirect('/directory/submit/')
	else:
		form = AlumniForm()
		form2 = BusinessForm()
	return render(request, 'directory/submit.html', {'form': form, 'form2': form2})
		

def detail(request, business_id):
	business = get_object_or_404(Business, id=business_id)
	if business.business_approved is False:
		return HttpResponseNotFound('<h1>Page not found</h1>')

	return render(request, 'directory/detail.html', {'business': business})

def search(request):
	results = []
	if request.method == "POST":
		form = BusinessSearchForm(request.POST)
		if form.is_valid():
			print(request.POST)
			# Save the search and refresh the page
			#search = form.save(commit=False)
			#search.date = timezone.now()
			#search.save()
			#add entries found
			results = Business.objects.all().filter(business_name__icontains=request.POST.get('business_name')).filter(business_type=request.POST.get('business_type')).filter(business_state=request.POST.get('business_state')).filter(business_approved=True)
			
			results.sort(key = lambda name: results[0])

			return render(request, 'directory/search.html', {'form': form, 'results':results})
			#return render()
		else:
			return HttpResponseRedirect('/directory/search/')

	else:
		form = BusinessSearchForm()
		return render(request, 'directory/search.html', {'form': form, 'results':results})
	#found_entries = list(Businesses.objects.filter(business_approved=True))
	#return render(request, 'directory/search.html')

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
