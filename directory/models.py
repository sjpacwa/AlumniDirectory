from django.db import models
from datetime import date
from .choice import BUSINESS_TYPE_CHOICES, STATE_CHOICES


class Business(models.Model):
	# These fields are what will be displayed.
	# Business name and type.
	business_name = models.CharField(max_length=200)
	business_type = models.CharField(max_length=4,
		choices=BUSINESS_TYPE_CHOICES, default='0000')
	
	# Business address.
	business_address_one = models.CharField(max_length=200)
	business_address_two = models.CharField(max_length=200, blank=True)
	business_city = models.CharField(max_length=200)
	business_state = models.CharField(max_length=2, choices=STATE_CHOICES, default='00')
	business_zip = models.CharField(max_length=5)

	# Other.
	business_desc = models.TextField(blank=True)
	business_phone = models.CharField(blank=True, max_length=10)
	business_submit_date = models.DateField(default=date.today)
	business_website = models.URLField(blank=True)

	# Internal database stuff.
	business_num_visit = models.PositiveIntegerField()
	business_approved = models.BooleanField()
	business_alumni = models.ForeignKey('Alumni', on_delete=models.CASCADE)
	business_edit_code = models.CharField(max_length=6)

	# These fields will be used to hold information for edits.
	# Business name and type.
	business_edit_name = models.CharField(max_length=200, default=business_name)
	business_edit_type = models.CharField(max_length=4,
		choices=BUSINESS_TYPE_CHOICES, default=business_type)

	# Business address.
	business_edit_address_one = models.CharField(max_length=200, default=business_address_one)
	business_edit_address_two = models.CharField(max_length=200, default=business_address_two)
	business_edit_city = models.CharField(max_length=200, default=business_city)
	business_edit_state = models.CharField(max_length=2, choices=STATE_CHOICES, default=business_state)
	business_edit_zip = models.CharField(max_length=5, default = business_zip)

	# Other.
	business_edit_desc = models.TextField(blank=True, default=business_desc)
	business_edit_phone = models.CharField(blank=True, max_length=10, default=business_phone)
	business_edit_date = models.DateField(default=date.today)
	business_edit_website = models.URLField(blank=True, default=business_website)

	# Internal database stuff.
	business_edit_approved = models.BooleanField(default=True)
	

class Alumni(models.Model):
	# Alumni name.
	alumni_first_name = models.CharField(max_length=200)
	alumni_last_name = models.CharField(max_length=200)
	
	# Alumni school info.
	alumni_major = models.CharField(max_length=30)
	alumni_grad = models.CharField(max_length=4)
	alumni_school_id = models.CharField(max_length=15, blank=True)

	# Alumni emails.
	alumni_personal_email = models.EmailField()
	alumni_school_email = models.EmailField(blank=True)

	# Internal database stuff.
	alumni_approved = models.BooleanField()
