# views.py
# Contains all the rendering functions for each page and function in the website.

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden, Http404, HttpResponseRedirect, HttpResponseNotFound
from .models import Business, Alumni
from .forms import BusinessForm, AlumniForm, BusinessEditForm
from django.core.mail import send_mail, send_mass_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from .choice import BUSINESS_TYPE_DICT, BUSINESS_TYPE_CHOICES, STATE_CHOICES, REVERSE_BUSINESS_TYPE_DICT, REVERSE_STATE_DICT
from random import random

#Heroku hosting URL: http://scu-directory.herokuapp.com

def index(request):
	'''
	index
	Params:
		request: All the meta data of the request for this page.
	Description:
		Provides the render for the index page.
	Returns:
		A render of the templated file index.html.
	'''
	return render(request, 'directory/index.html')

def submit(request):
	'''
	submit
	Params:
		request: All the meta data of the request for this page.
	Description:
		Handles POST and provides the needed information to render the submit page.
	Returns:
		A render of the templated file submit.html with all needed info.
	'''
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
	'''
	detail
	Params:
		request: All the meta data of the request for this page.
		business_id: The business ID for the specific business to display.
	Description:
		Looks up the business and provides needed info to render detail page.
	Returns:
		A render of the templated file detail.html with all needed info.
	'''
	business = get_object_or_404(Business, id=business_id)
	if business.business_approved is False:
		return HttpResponseNotFound('<h1>Page not found</h1>')
	
	business.business_num_visit = business.business_num_visit + 1
	business.save()
	
	business.business_type = BUSINESS_TYPE_DICT[business.business_type]
	alumni = Alumni.objects.get(pk=business.business_alumni_id)

	return render(request, 'directory/detail.html', {'business': business, 'alumni':alumni})

def search(request):
	'''
	search
	Params:
		request: All the meta data of the request for this page.
	Description:
		Handles search POST request and provides needed info to search page.
	Returns:
		A render of the templated file search.html with all needed info.
	'''
	def dict_fix(results):
		'''
		dict_fix
		Params:
			results: A list of all results for a certain search.
		Description:
			Converts the business type from code to human-readable format.
		Returns:
			The same list inputted with business type changed.
		'''
		for item in list(results):
			item.business_type = BUSINESS_TYPE_DICT[item.business_type]
		return results

	# Get all business that have been apprived.
	results = Business.objects.all().filter(business_approved=True)
	if request.method == "POST":
		# Filter by business name if supplied.
		if request.POST.get('business_name') != '':
			results = results.filter(business_name__icontains=request.POST.get('business_name'))
		
		# Filter by business type if supplied.
		if request.POST.get('type') != '---':
			results = results.filter(business_type=REVERSE_BUSINESS_TYPE_DICT[request.POST.get('type')])

		# Filter by business state if supplied.
		if request.POST.get('state') != '---':
			results = results.filter(business_state=REVERSE_STATE_DICT[request.POST.get('state')])

		results = dict_fix(results)
		return render(request, 'directory/search.html', {'filled_name':request.POST.get('business_name'),
			'chosen_type':request.POST.get('type'),
			'chosen_state':request.POST.get('state'),
			'results':results, 
			'types':BUSINESS_TYPE_CHOICES, 
			'state':STATE_CHOICES})

	else:
		results = dict_fix(results)
		return render(request, 'directory/search.html', {'results':results, 'types':list(BUSINESS_TYPE_CHOICES), 'state':STATE_CHOICES})

def log_in(request):
	'''
	log_in
	Params:
		request: All the meta data of the request for this page.
	Description:
		Handles the login process and reroutes user if authenticated.
	Returns:
		A render of the templated file login.html or a redirect to approve if login successful.
	'''
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
	'''
	approve
	Params:
		request: All the meta data of the request for this page.
	Description:
		Collects all of the businesses that have not beed approved or are edited. User must be logged in to access.
	Returns:
		A render of the templated file approve.html with all needed info.
	'''
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
	'''
	statistics
	Params:
		request: All the meta data of the request for this page.
	Description:
		Collects all website statistics and prepares it to be templated. User must be logged in to access.
	Returns:
		A render of the templated file statistics.html with all needed info.
	'''
	# Get number of businesses curently submitted.
	all_business = Business.objects.all()
	all_business_count= len(all_business)

	# Get number of approved businesses.
	approved_business = all_business.filter(business_approved=True)
	approved_business_count = len(approved_business)

	# Get total business visits.
	business_visit_count = 0
	businesses = []
	for business in approved_business:
		business_visit_count = business_visit_count + business.business_num_visit
		alumni = Alumni.objects.get(pk=business.business_alumni_id)
		businesses.append((business.business_name, 
			business.business_num_visit, 
			alumni.alumni_first_name,
			alumni.alumni_last_name,
			alumni.alumni_personal_email))

	businesses.sort(key=lambda business: business[1])

	return render(request, 'directory/statistics.html', {"unapproved_business_count": (all_business_count - approved_business_count), 
		"businesses": businesses[::-1], 
		"approved_business_count": approved_business_count,
		"business_visit_count": business_visit_count})

@login_required
def log_out(request):
	'''
	log_out
	Params:
		request: All the meta data of the request for this page.
	Description:
		Logs the current user out. Must be logged in to access.
	Returns:
		A redirect to the login page.
	'''
	logout(request)
	return HttpResponseRedirect('/office/login/')

@login_required
def approve_deny_new(request):
	'''
	approve_deny_new
	Params:
		request: All the meta data of the request for this page.
	Description:
		Handles the approval of all business postings that are new and emails the user with results. Must be logged in to access.
	Returns:
		A redirect to the approval page.
	'''
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
	'''
	approve_deny_edit
	Params:
		request: All the meta data of the request for this page.
	Description:
		Handles the approval of all business postings that have been edited and emails the user with results. Must be logged in to access.
	Returns:
		A redirect to the approval page.
	'''
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
	'''
	edit
	Params:
		request: All the meta data of the request for this page.
		business_id: The ID of the business that should be edited.
	Description:
		Handles the POST for edited businesses and ensures the proper authentication code was inserted.
	Returns:
		A render of the templated file edit.html with all needed info.
	'''
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

@login_required
def admin_delete(request, business_id):
	'''
	admin_delete
	Params:
		request: All the meta data of the request for this page.
		business_id: The ID of the business that should be deleted.
	Description:
		Deletes the business that is given from the database. Must be logged in to access.
	Returns:
		A redirect to the search page.
	'''
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
	'''
	delete
	Params:
		request: All the meta data of the request for this page.
		business_id: The ID of the business that should be deleted.
	Description:
		Checks that the proper verification code has been entered and then deletes the business from the database.
	Returns:
		A render of the templated page delete.html with all needed info.
	'''
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
