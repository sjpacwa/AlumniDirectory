from django.forms import ModelForm
from .models import Business, Alumni

class BusinessForm(ModelForm):
	class Meta:
		model = Business
		fields = ('business_name', 'business_type', 'business_address_one', 'business_address_two', 'business_city', 'business_state',
					'business_zip')

class AlumniForm(ModelForm):
	class Meta:
		model = Alumni
		fields = ('alumni_first_name', 'alumni_last_name', 'alumni_major', 'alumni_grad',
		'alumni_school_id', 'alumni_personal_email', 'alumni_school_email', 'alumni_approved')

