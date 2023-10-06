from django.db import models

# Create your models here.
class User(models.Model):
	usertype = models.CharField(max_length=100,default="customer")
	name = models.CharField(max_length=100)
	email = models.EmailField()
	pswd = models.CharField(max_length=100)

	def __str__(self):
		return self.name+" - "+self.usertype

class Car(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	cartype = models.CharField(max_length=100)
	c_image = models.ImageField(blank=True,null=True,upload_to='images/')
	c_brand = models.CharField(max_length=100)
	c_name = models.CharField(max_length=100)
	c_model = models.CharField(max_length=100)
	c_fuel = models.CharField(max_length=100)
	c_price = models.IntegerField(default=1000)
	c_mileage = models.IntegerField(default=45)
	c_transmission = models.CharField(max_length=100,default="manual")
	c_seats = models.IntegerField(default=5)
	c_luggage = models.IntegerField(default=4)
	c_features = models.CharField(max_length=100,default="all")
	c_description = models.CharField(max_length=1000,default="best car...")

	razorpay_order_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_id=models.CharField(max_length=100,null=True,blank=True)
	razorpay_payment_signature=models.CharField(max_length=100,null=True,blank=True)


	def __str__(self):
		return self.cartype+" - "+self.c_brand+" - "+self.c_name+" - "+self.user.name

class Inquiry(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	car = models.ForeignKey(Car,on_delete=models.CASCADE)
	from_date = models.DateField()
	to_date = models.DateField()
	number_of_cars = models.IntegerField()
	color_of_car = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	contact_number = models.IntegerField()
	email_address = models.EmailField()

	def __str__(self):
		return self.user.name+" - "+self.car.c_name