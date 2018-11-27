# test.py
# Contains all of the tests that can be run automatically with manage.py.

from django.test import TestCase
from .models import Business, Alumni

class BusinessTestCase(TestCase):
	def setUp(self):
		Business.objects.create(business_name="Restauranttest123", 
			business_address_one="1234", 
			business_city="SCU", 
			business_state="CA", 
			business_zip="12345")

	def test_business(self):
		restaurant = Business.objects.get(business_name="Restauranttest123")
		restaurant.assertEqual(restaurant.business_name=="Restauranttest123")
		restaurant.assertEqual(restaurant.business_address_one=="1234")
		restaurant.assertEqual(restaurant.business_city=="SCU")
		restaurant.assertEqual(restaurant.business_state=="CA")
		restaurant.assertEqual(restaurant.business_zip=="12345")

class AlumniTestCase(TestCase):
	def setUp(self):
		Alumni.objects.create(alumni_first_name="Johntest123", 
			alumni_last_name="Doe", 
			alumni_major="COEN", 
			alumni_grad="2019")

	def test_alumni(self):
		john = Alumni.objects.get(alumni_first_name="Johntest123")
		john.assertEqual(john.alumni_first_name=="Johntest123")
		john.assertEqual(john.alumni_last_name=="Doe")
		john.assertEqual(john.alumni_major=="COEN")
		john.assertEqual(john.alumni_grad=="2019")