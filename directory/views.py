from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect, HttpResponseNotFound
from .models import Business, Alumni
from .forms import BusinessForm, AlumniForm, BusinessSearchForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .choice import BUSINESS_TYPE_DICT
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
			new_business = form2.save(commit=False)
			new_business.author = request.user
			new_business.published_date = timezone.now()
			new_business.business_num_visit = 0
			new_business.business_approved = False

			type_error = ""
			state_error = ""
			if new_business.business_type == '0000':
				type_error = "You must select a business type."
			if new_business.business_state == '00':
				state_error = "You must select a state."

			if type_error != "" or state_error != "":
				return render(request, 'directory/submit.html', {'form': form, 'form2': form2, 
					'type_error':type_error, 'state_error': state_error})

			new_alumni.save()
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

	business.business_type = BUSINESS_TYPE_DICT[business.business_type]

	return render(request, 'directory/detail.html', {'business': business})

def search(request):
	results = []
	if request.method == "POST":
		form = BusinessSearchForm(request.POST)
		if form.is_valid():
			print(request.POST)

			results = Business.objects.all().filter(business_name__icontains=request.POST.get('business_name')).filter(business_approved=True)
			
			if request.POST.get('business_type') != '0000':
				results = results.filter(business_type=request.POST.get('business_type'))
			if request.POST.get('business_state') != '00':
				results = results.filter(business_state=request.POST.get('business_state'))

			#list(results).sort(key = lambda name: results[0])

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
	for item in list(query_set):
		item.business_type = BUSINESS_TYPE_DICT[item.business_type]

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
	messages = ()

	for choice in list(request.POST.items())[1:]:
		# Fetch the relevant business and alumni from database.
		business = Business.objects.get(id=choice[0])
		alumni = Alumni.objects.get(id=business.business_alumni_id)
		
		if choice[1] in ['approve']:
			business.business_approved = True
			alumni.alumni_approved = True
			business.save()
			alumni.save()
			if alumni.alumni_school_email is '':
				messages = (('[NOREPLY] Your submission has been approved', 'Congratulations, your submission is now viewable in the SCU Alumni Directory.\n' \
					'This is an unmonitored email address and any responses will be ignored.', 'scudirectory@gmail.com', [alumni.alumni_personal_email,]),)
			else:
				messages = (('[NOREPLY] Your submission has been approved', 'Congratulations, your submission is now viewable in the SCU Alumni Directory.\n' \
					'This is an unmonitored email address and any responses will be ignored.', 'scudirectory@gmail.com', [alumni.alumni_school_email,]),)
		elif choice[1] in ['deny']:
			if alumni.alumni_school_email is '':
				messages = (('[NOREPLY] Your submission has been denied', 'Your submission to the SCU Alumni Directory was denied. Please ensure that all fields are accurate when submitting again.\n' \
					'This is an unmonitored email address and any responses will be ignored.', 'scudirectory@gmail.com', [alumni.alumni_personal_email,]),)
			else:
				messages = (('[NOREPLY] Your submission has been denied', 'Your submission to the SCU Alumni Directory was denied. Please ensure that all fields are accurate when submitting again.\n' \
					'This is an unmonitored email address and any responses will be ignored.', 'scudirectory@gmail.com', [alumni.alumni_school_email,]),)
		
			alumni.delete()
			business.delete()

	send_mass_mail(messages)

	return HttpResponseRedirect('/directory/office/approve/')
