from django.db import models


class Business(models.Model):
	# Business name and type.
	business_name = models.CharField(max_length=200)
	business_type = models.CharField(max_length=200)
	
	# Business address.
	business_address_one = models.CharField(max_length=200)
	business_address_two = models.CharField(max_length=200)
	business_city = models.CharField(max_length=200)
	business_state = models.CharField(max_length=2)
	business_zip = models.CharField(max_length=5)

	# Other.
	business_desc = models.TextField()
	business_phone = models.CharField(max_length=10)
	business_end_date = models.DateField()
	business_website = models.URLField()

	# Internal database stuff.
	business_num_visit = models.PositiveIntegerField()
	business_approved = models.BooleanField()
	business_alumni = models.ForeignKey('Alumni', on_delete=models.CASCADE)


class Alumni(models.Model):
	# Alumni name.
	alumni_first_name = models.CharField(max_length=200)
	alumni_last_name = models.CharField(max_length=200)
	
	# Alumni school info.
	alumni_major = models.CharField(max_length=30)
	alumni_grad = models.CharField(max_length=4)
	alumni_school_id = models.CharField(max_length=15)

	# Alumni emails.
	alumni_personal_email = models.EmailField()
	alumni_school_email = models.EmailField()

	# Internal database stuff.
	alumni_approved = models.BooleanField()
