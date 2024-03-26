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
    ORDERSTATUS = (
    	("house-type","house-type"),
        ("Booking","Booking"),
        ("payment-status","payment-status"),
        ("on-the-way","on-the-way"),
        ("cancel","Cancle"),
        ("finish","finish process"))
    htype = models.CharField(max_length=40,null=True)
    userid = models.ForeignKey(User,on_delete=models.CASCADE)
    bname = models.CharField(max_length=40)
    movefrom = models.CharField(max_length=40)
    moveto = models.CharField(max_length=40)
    state = models.CharField(max_length=40)
    zipcode = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
    razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=20,choices = ORDERSTATUS,default="Booking")
    statuscheck = models.BooleanField(default = False)


    house_type_active = models.BooleanField(default=False)
    booking_active = models.BooleanField(default=False)
    payment_status_active = models.BooleanField(default=False)
    on_the_way_active = models.BooleanField(default=False)
    cancel_active = models.BooleanField(default=False)
    finish_active = models.BooleanField(default=False)

    def get_all_processes(self):
        return [status[0] for status in self.ORDERSTATUS]

    def save(self, *args, **kwargs):
        # Set flags based on the current status
        current_status = self.status
        self.house_type_active = current_status == 'house-type'
        self.booking_active = current_status == 'Booking'
        self.payment_status_active = current_status == 'payment-status'
        self.on_the_way_active = current_status == 'on-the-way'
        self.cancel_active = current_status == 'cancel'
        self.finish_active = current_status == 'finish'

        super().save(*args, **kwargs)

    def __str__(self):
        return  self.bname + " || " + self.htype

class Contact(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	number = models.CharField(max_length=50)
	message = models.TextField(max_length=1000)
	
	def __str__(self):
		return self.name   

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