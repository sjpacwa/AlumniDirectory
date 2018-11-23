from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect, HttpResponseNotFound
from .models import Business, Alumni
from .forms import BusinessForm, AlumniForm, BusinessSearchForm, BusinessEditForm
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .choice import BUSINESS_TYPE_DICT
from random import random

#Heroku hosting URL: http://scu-directory.herokuapp.com

def index(request):
	return render(request, 'directory/index.html')

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

			# Generate the random edit code.
			edit_code = []
			while len(edit_code) is not 6:
				edit_code.append(str(int(random() * 9)))

			edit_code = ''.join(edit_code)
			new_business.business_edit_code = edit_code

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
			return HttpResponseRedirect('/submit/')
	else:
		form = AlumniForm()
		form2 = BusinessForm()
	return render(request, 'directory/submit.html', {'form': form, 'form2': form2})
		

def detail(request, business_id):
	business = get_object_or_404(Business, id=business_id)
	if business.business_approved is False:
		return HttpResponseNotFound('<h1>Page not found</h1>')
	
	business.business_num_visit = business.business_num_visit + 1
	
	business.business_type = BUSINESS_TYPE_DICT[business.business_type]

	return render(request, 'directory/detail.html', {'business': business})

def search(request):
	def dict_fix(results):
		for item in list(results):
			item.business_type = BUSINESS_TYPE_DICT[item.business_type]
		return results

	results = []
	results = Business.objects.all().filter(business_approved=True)
	if request.method == "POST":
		form = BusinessSearchForm(request.POST)
		if form.is_valid():
			results = Business.objects.all().filter(business_name__icontains=request.POST.get('business_name')).filter(business_approved=True)
			
			if request.POST.get('business_type') != '0000':
				results = results.filter(business_type=request.POST.get('business_type'))
			if request.POST.get('business_state') != '00':
				results = results.filter(business_state=request.POST.get('business_state'))

			results = dict_fix(results)
			return render(request, 'directory/search.html', {'form': form, 'results':results})
		else:
			results = dict_fix(results)
			return HttpResponseRedirect('/search/', {'results':results})

	else:
		form = BusinessSearchForm()
		results = dict_fix(results)
		return render(request, 'directory/search.html', {'form': form, 'results':results})

def log_in(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = authenticate(request, username=username, password=password)
	if user is not None:
		# User is authenticated, redirect to approve.
		login(request, user)
		return HttpResponseRedirect('/office/approve/')
	elif username is not '' or password is not '':
		# Incorrect login, update error_message.
		return render(request, 'directory/login.html', {
			'error_message': "Incorrect username/password."
			})

	return render(request, 'directory/login.html')

@login_required
def approve(request):
	new_businesses = Business.objects.filter(business_approved=False)
	edit_businesses = Business.objects.filter(business_edit_approved=False)
	for item in list(new_businesses):
		item.business_type = BUSINESS_TYPE_DICT[item.business_type]
	for item in list(edit_businesses):
		item.business_type = BUSINESS_TYPE_DICT[item.business_type]
		item.business_edit_type = BUSINESS_TYPE_DICT[item.business_edit_type]


	return render(request, 'directory/approve.html', {'new': new_businesses, 'edit': edit_businesses})

@login_required
def statistics(request):
	return render(request, 'directory/statistics.html')

@login_required
def log_out(request):
	logout(request)
	return HttpResponseRedirect('/office/login/')

@login_required
def approve_deny_new(request):
	approved_messages = ('[noreply] Your submission has been approved', 
		'Congratulations, your submission is now viewable in the SCU Alumni Directory.\nThis is an unmonitored email address and any responses will be ignored.', 
		'scudirectory@gmail.com', 
		[])
	denied_messages = ('[noreply] Your submission has been denied', 
		'Your submission to the SCU Alumni Directory was denied. Please ensure that all fields are accurate when submitting again.\nThis is an unmonitored email address and any responses will be ignored.', 
		'scudirectory@gmail.com',
		[])

	# Iterate through data other than CRSF token.
	for choice in list(request.POST.items())[1:]:
		# Fetch the relevant business and alumni from database.
		business = Business.objects.get(id=choice[0])
		alumni = Alumni.objects.get(id=business.business_alumni_id)
		
		if choice[1] in ['approve']:
			# Set flags properly and update the database.
			business.business_approved = True
			alumni.alumni_approved = True
			business.save()
			alumni.save()
			
			# Send a confirmation email.
			approved_messages[3].append(alumni.alumni_personal_email)

		elif choice[1] in ['deny']:
			# Remove the rejected data from the database.
			alumni.delete()
			business.delete()

			# Send a confirmation email.
			denied_messages[3].append(alumni.alumni_personal_email)

	# Send the emails.
	send_mass_mail((approved_messages, denied_messages))

	return HttpResponseRedirect('/office/approve/')

@login_required
def approve_deny_edit(request):
	approved_messages = ('[noreply] Your edit has been approved', 
		'Congratulations, your edit is now viewable in the SCU Alumni Directory.\nThis is an unmonitored email address and any responses will be ignored.', 
		'scudirectory@gmail.com', 
		[])
	denied_messages = ('[noreply] Your edit has been denied', 
		'Your edit to the SCU Alumni Directory was denied. Your original post is still viewable. Please ensure that all fields are accurate when submitting again.\nThis is an unmonitored email address and any responses will be ignored.', 
		'scudirectory@gmail.com',
		[])

	# Iterate through data other than CRSF token.
	for choice in list(request.POST.items())[1:]:
		# Fetch the relevant business and alumni from database.
		business = Business.objects.get(id=choice[0])
		alumni = Alumni.objects.get(id=business.business_alumni_id)
		
		if choice[1] in ['approve']:
			# The new edit is approved. copy over.
			business.business_name = business.business_edit_name
			business.business_type = business.business_edit_type
			business.business_address_one = business.business_edit_address_one
			business.business_address_two = business.business_edit_address_two
			business.business_city = business.business_edit_city
			business.business_state = business.business_edit_state
			business.business_zip = business.business_edit_zip
			business.business_desc = business.business_edit_desc
			business.business_phone = business.business_edit_phone
			business.business_website = business.business_edit_website

			# The business is now editted.
			business.business_edit_approved = True
			business.save()
			
			# Send a confirmation email.
			approved_messages[3].append(alumni.alumni_personal_email)

		elif choice[1] in ['deny']:
			# The edit is no longer valid. Wait to be overwritten.
			business.business_edit_approved = True

			# Send a confirmation email.
			denied_messages[3].append(alumni.alumni_personal_email)

	# Send the emails.
	send_mass_mail((approved_messages, denied_messages))

	return HttpResponseRedirect('/office/approve/')

def edit(request, business_id):
	# Lookup the business in the database.
	business = get_object_or_404(Business, id=business_id)
	if business.business_approved is False:
		return HttpResponseNotFound('<h1>Page not found</h1>')
	alumni = Alumni.objects.get(id=business.business_alumni_id)
	INITIAL_VALUES = {
		'business_edit_name':business.business_name,
		'business_edit_type':business.business_type,
		'business_edit_address_one':business.business_address_one,
		'business_edit_address_two':business.business_address_two,
		'business_edit_city':business.business_city,
		'business_edit_state':business.business_state,
		'business_edit_zip':business.business_zip,
		'business_edit_desc':business.business_desc,
		'business_edit_phone':business.business_phone,
		'business_edit_website':business.business_website
	}

	submitted = False

	if request.method == 'POST':
		form = BusinessEditForm(request.POST)
		if form.is_valid():
			# The correct code was supplied.
			print(request.POST.get('code_check'))
			print(business.business_edit_code)
			if request.POST.get('code_check') == business.business_edit_code:
				# Update relevant fields and save.
				business.business_edit_name = request.POST.get('business_edit_name')
				business.business_edit_type = request.POST.get('business_edit_type')
				business.business_edit_address_one = request.POST.get('business_edit_address_one')
				business.business_edit_address_two = request.POST.get('business_edit_address_two')
				business.business_edit_city = request.POST.get('business_edit_city')
				business.business_edit_state = request.POST.get('business_edit_state')
				business.business_edit_zip = request.POST.get('business_edit_zip')
				business.business_edit_desc = request.POST.get('business_edit_desc')
				business.business_edit_phone = request.POST.get('business_edit_phone')
				business.business_edit_website = request.POST.get('business_edit_website')
				business.business_edit_approved = False
				business.save()

				# Render the page.
				submitted = True
				return render(request, 'directory/edit.html', {'business': business, 'submitted':submitted})

			# The incorrect code was supplied.
			else:
				error_message = 'Verification code is incorrect.'
				form.save(commit=False)
				return render(request, 'directory/edit.html', {'business': business, 'form': form, 'submitted':submitted, 'error_message':error_message})

	else:
		# Send the the verification code to business owner.
		unlock_code = business.business_edit_code
		email = ("[noreply] Edit code for " + business.business_name,
			"The code for " + business.business_name + " is " + unlock_code + ".\nThis is an unmonitored email address and any responses will be ignored.",
			"scudirectory@gmail.com",
			[alumni.alumni_personal_email])
		send_mass_mail((email,))

		
		form = BusinessEditForm(initial=INITIAL_VALUES, instance=business)
		
		return render(request, 'directory/edit.html', {'business': business, 'form': form, 'submitted':submitted})



def admin_delete(request, business_id):
	if request.POST.get('csrfmiddlewaretoken') is None:
		# Was not accessed through the right form.
		return HttpResponseNotFound('<h1>Page not found</h1>')

	else:
		business = Business.objects.get(id=business_id)
		alumni = Alumni.objects.get(id=business.business_alumni_id)
		email = ("[noreply] Your business has been deleted.",
			"An Alumni Office admin has removed your business from the directory. It will no longer be visible in listings.\nThis is an unmonitored email address and any responses will be ignored.",
			"scudirectory@gmail.com",
			[alumni.alumni_personal_email])
		send_mass_mail((email,))
		alumni.delete()
		business.delete()
		return HttpResponseRedirect('/search/')

def delete(request, business_id):
	business = Business.objects.get(id=business_id)
	alumni = Alumni.objects.get(id=business.business_alumni_id)
	deleted = False

	if request.method == 'POST':
		# We need to check the code and then delete business or ask again.
		if request.POST.get('code_check') == business.business_edit_code:
			# The correct code was supplied. Delete the business and send an email.
			email = ("[noreply] Your business has been deleted.",
			"Your business has been removed from the directory. It will no longer be visible in listings.\nThis is an unmonitored email address and any responses will be ignored.",
			"scudirectory@gmail.com",
			[alumni.alumni_personal_email])
			send_mass_mail((email,))
			alumni.delete()
			business.delete()

			deleted = True
			return render(request, 'directory/delete.html', {'business':business, 'deleted':deleted})

		else:
			# The code was incorrect, display an error and prompt again.
			error_message = "Verification code is incorrect."

			return render(request, 'directory/delete.html', {'business':business, 'deleted':deleted, 'error':error_message})

	else:
		# The code is supplied and wait for form to be completed.
		email = ("[noreply] Code to delete " + business.business_name, 
			"The code for " + business.business_name + " is " + business.business_edit_code + ".\nThis is an unmonitored email address and any responses will be ignored.",
			"scudirectory@gmail.com",
			[alumni.alumni_personal_email])
		send_mass_mail((email,))

		return render(request, 'directory/delete.html', {'business':business, 'deleted':deleted})
