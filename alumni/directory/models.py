from django.db import models


class Business(models.Model):
	# Business name and type.
	business_name = models.CharField(max_length=200)
	BUSINESS_TYPE_CHOICES = ( #from https://developer.paypal.com/docs/classic/adaptive-accounts/integration-guide/ACBusinessCategories/
		('1000','Arts, crafts, and collectibles'),
		('1001','Baby'),
		('1002','Beauty and fragrances'),
		('1003','Books and magazines'),
		('1004','Business to business'),
		('1005','Clothing, accessories, and shoes'),
		('1006','Computers, accessories, and services'),
		('1007','Education'),
		('1008','Electronics and telecom'),
		('1009','Entertainment and media'),
		('1010','Financial services and products'),
		('1011','Food retail and service'),
		('1012','Gifts and flowers'),
		('1013','Government'),
		('1014','Health and personal care'),
		('1015','Home and garden'),
		('1016','Nonprofit'),
		('1017','Pets and animals'),
		('1018','Religion and spirituality (for profit)'),
		('1019','Retail (not elsewhere classified)'),
		('1020','Services - other'),
		('1021','Sports and outdoors'),
		('1022','Toys and hobbies'),
		('1023','Travel'),
		('1024','Vehicle sales'),
		('1025','Vehicle service and accessories.'),
	)
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
