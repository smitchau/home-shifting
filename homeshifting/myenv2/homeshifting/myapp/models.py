from django.db import models

# Create your models here.

class User(models.Model):
	u_name = models.CharField(max_length = 30)
	u_email = models.EmailField(unique=True , max_length = 30)
	u_password = models.CharField(max_length = 20)
	u_contact = models.CharField(max_length = 11)

	def __str__(self):
		return self.u_email + " | " + self.u_contact

class Booking(models.Model):
	u_id = models.ForeignKey(User , on_delete = models.CASCADE)
	bname = models.CharField(max_length = 30)
	housetype = models.CharField(max_length = 30)
	Booking_at = models.DateTimeField(auto_now = True)
	source = models.CharField(max_length = 30)
	destination = models.CharField(max_length = 30)
	state = models.CharField(max_length = 30)
	pcode = models.IntegerField()

	def __str__(self):
		return self.bname + " | " + self.u_id.u_contact


class Truckpartner(models.Model):
	b_id = models.ForeignKey(Booking , on_delete = models.CASCADE)
	t_name = models.CharField(max_length = 30)
	t_email = models.EmailField(unique=True , max_length = 30)
	t_password = models.CharField(max_length = 20)
	t_contact = models.CharField(max_length = 11)
	t_address = models.CharField(max_length = 50)
	t_aadharcard_details = models.CharField(max_length = 30 , unique = True)
	t_pancard_details = models.CharField(max_length = 30 , unique = True)
	t_drivinglicence_details = models.CharField(max_length = 30 , unique = True)
	t_bank_details = models.CharField(max_length = 30 , unique = True)
	
"""
class fleet(models.Model):
	t_id = models.ForeignKey(Truckpartner , on_delete = models.CASCADE)
	f_name = models.CharField(max_length = 30)
	f_type = models.CharField(max_length = 30)
	f_packages = models.CharField(max_length = 20)
	f_registration_no = models.CharField(max_length = 11)

class billing(models.Model):
	#id = models.ForeignKey(User,Booking,Truckpartner,fleet , on_delete = models.CASCADE)
	billing_at = models.DateTimeField(auto_now = True)
	tax_amount = models.CharField(max_length = 5)
	total_amount = models.CharField(max_length = 5)

"""