# forms.py
# Contains classes that represent the different forms used on the website so they can be interpreted by Django.

from django.forms import ModelForm, CharField
from crispy_forms.helper import FormHelper
from .models import Business, Alumni

class BusinessForm(ModelForm):
	class Meta:
		model = Business
		fields = ('business_name',
			'business_type', 
			'business_address_one', 
			'business_address_two', 
			'business_city', 
			'business_state',
			'business_zip', 
			'business_desc', 
			'business_phone', 
			'business_website'
		)

		labels = {'business_name':'Business Name*',
			'business_type':'Business Type*', 
			'business_address_one':'Address One*', 
			'business_address_two':'Address Two', 
			'business_city':'City*', 
			'business_state':'State*',
			'business_zip':'Zip Code*', 
			'business_desc':'Description', 
			'business_phone':'Phone Number', 
			'business_website':'Website URL'
		}

	def __init__(self, *args, **kwargs):
		# __init__
		# Utilizes Django crispy forms to help them display nicely.
		super(BusinessForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()


class AlumniForm(ModelForm):
	class Meta:
		model = Alumni
		fields = ('alumni_first_name', 
			'alumni_last_name', 
			'alumni_major', 
			'alumni_grad',
			'alumni_school_id', 
			'alumni_personal_email', 
			'alumni_school_email'
		)

		labels = {'alumni_first_name':'First Name*', 
			'alumni_last_name':'Last Name*', 
			'alumni_major':'Major*', 
			'alumni_grad':'Graduation Date*',
			'alumni_school_id':'SCU ID', 
			'alumni_personal_email':'Personal Email*', 
			'alumni_school_email':'SCU Email'
		}

	def __init__(self, *args, **kwargs):
			# Utilizes Django crispy forms to help them display nicely.
			super(AlumniForm, self).__init__(*args, **kwargs)
			self.helper = FormHelper()


class BusinessEditForm(ModelForm):
	code_check = CharField(label='Verification Code*')

	class Meta:
		model = Business
		fields = ('business_edit_name',
			'business_edit_type',
			'business_edit_address_one',
			'business_edit_address_two',
			'business_edit_city',
			'business_edit_state',
			'business_edit_zip',
			'business_edit_desc',
			'business_edit_phone',
			'business_edit_website'
		)

		labels = {'business_edit_name':'Business Name*',
			'business_edit_type':'Business Type*',
			'business_edit_address_one':'Address One*',
			'business_edit_address_two':'Address Two',
			'business_edit_city':'City*',
			'business_edit_state':'State*',
			'business_edit_zip':'Zip Code*',
			'business_edit_desc':'Description',
			'business_edit_phone':'Phone Number',
			'business_edit_website':'Website URL'
		}

	def __init__(self, *args, **kwargs):
		# Utilizes Django crispy forms to help them display nicely.
		super(BusinessEditForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()
