from django.shortcuts import render,redirect
from .models import User,Car,Inquiry
from django.conf import settings
from django.core.mail import send_mail
import random
import razorpay

# Create your views here.
def index(request):
	car=Car.objects.all()
	return render(request,'index.html',{'car':car})

def seller_index(request):
	car=Car.objects.all()
	return render(request,'seller_index.html',{'car':car})

def about(request):
	return render(request,'about.html')

def services(request):
	return render(request,'services.html')

def car(request):
	car=Car.objects.all()
	return render(request,'car.html',{'car':car})

def contact(request):
	return render(request,'contact.html')

def signup(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			msg1 = "email already exist..."
			return render(request,'signup.html',{'msg1':msg1})
		except:
			if request.POST['pswd']==request.POST['cpswd']:
				User.objects.create(
					usertype=request.POST['usertype'],
					name=request.POST['name'],
					email=request.POST['email'],
					pswd=request.POST['pswd'],
				)
				msg = "Signup Done..."
				return render(request,'login.html',{'msg':msg})
			else:
				msg1 = "password and confirm password does not matched..."
				return render(request,'signup.html',{'msg1':msg1})
	else:
			return render(request,'signup.html')

def e_verify(request):
	email=request.GET.get('email')
	print(">>>>>>>>>>>>>>>>AJAX DATA : ",email)
	data={'is_taken':User.objects.filter(email__iexact=email).exists()}
	return JsonResponse(data)

def login(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'],pswd=request.POST['pswd'])
			msg="login successful..."
			request.session['email']=user.email
			request.session['pswd']=user.pswd
			if user.usertype=="manager":
				print(">>>>>>>>>>>MAnager")
				return render(request,'seller_index.html')
			else:
				print(">>>>>>>>>>>CUstomer")
				return redirect('index')
		except:
			msg1 = "email does not exist"
			return render(request,'login.html',{'msg1':msg1})
	else:
		return render(request,'login.html')

def logout(request):
	del request.session['email']
	return redirect('login')

def fpswd(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST['email'])
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>working till user")

			subject = 'forgot password otp'
			otp = random.randint(1000,9999)
			message = f'Hi {user.name}, thank you for registering in my app, your otp is :- '+str(otp)
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>working till otp")

			email_from = settings.EMAIL_HOST_USER
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>working till host user")

			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )
			print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>working till now")
			return render(request, 'verify_otp.html',{'email':user.email,'otp':str(otp)})

		except:
			msg1 = "you are not registered user..."
			return render(request,'fpswd.html',{'msg1':msg1})

	else:
		return render(request,'fpswd.html')

def verify_otp(request):
	email=request.POST['email']
	uotp=request.POST['uotp']
	otp=request.POST['otp']
	if request.method=='POST':
		
		if uotp==otp:
			return render(request,'set_pswd.html',{'email':email})
		else:
			msg1 = "otp doesn't matched!!!"
			return render(request,'verify_otp.html',{'msg1':msg1})
	else:
		return render(request,'verify_otp.html')

def set_pswd(request):
	if request.method=="POST":
		email=request.POST['email']
		npswd=request.POST['npswd']
		cnpswd=request.POST['cnpswd']
		if npswd==cnpswd:
			user=User.objects.get(email=email)
			user.pswd=npswd
			user.save()
			return redirect('login')
		else:
			msg1="pasword and confirm password does not matched..."
			return render(request,'set_pswd.html',{'msg1':msg1})
	else:
		return render(request,'set_pswd.html')

def our_services(request):
	return render(request,'our_services.html')

def add_car(request):
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		Car.objects.create(
			user=user,
			cartype = request.POST['cartype'],
			c_image = request.FILES['c_image'],
			c_brand = request.POST['c_brand'],
			c_name = request.POST['c_name'],
			c_model = request.POST['c_model'],
			c_fuel = request.POST['c_fuel'],
			c_price = request.POST['c_price'],
			c_mileage = request.POST['c_mileage'],
			c_transmission = request.POST['c_transmission'],
			c_seats = request.POST['c_seats'],
			c_luggage = request.POST['c_luggage'],
			c_features = request.POST['c_features'],
			c_description = request.POST['c_description'],
			)
		msg = "Car Added Successfully..."
		return render(request,'add_car.html',{'msg':msg})
	else:
		return render(request,'add_car.html')

def cars(request):
	seller=User.objects.get(email=request.session['email'])
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>by method",seller)
	car=Car.objects.filter(user=seller)
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",car)
	return render(request,'cars.html',{'car':car})

def update_car(request,pk):
	seller=User.objects.get(email=request.session['email'])
	car=Car.objects.get(pk=pk,user=seller)
	if request.method=="POST":
		car.user=seller
		car.cartype =request.POST['cartype']
		car.c_image =request.FILES['c_image']
		car.c_brand =request.POST['c_brand']
		car.c_name =request.POST['c_name']
		car.c_model =request.POST['c_model']
		car.c_fuel =request.POST['c_fuel']
		car.c_price =request.POST['c_price']
		c_mileage =request.POST['c_mileage']
		c_transmission =request.POST['c_transmission']
		c_seats =request.POST['c_seats']
		c_luggage =request.POST['c_luggage']
		c_features =request.POST['c_features']
		c_description =request.POST['c_description']
		car.save()
		return redirect('cars')
	else:
		return render(request,'update_car.html',{'car':car})

def delete_car(request,pk):
	seller=User.objects.get(email=request.session['email'])
	car=Car.objects.get(pk=pk,user=seller)

	car.delete()
	return redirect("seller_index")

def car_details(request,pk):
	seller=User.objects.get(email=request.session['email'])
	car=Car.objects.get(pk=pk,user=seller)
	return render(request,'car_details.html',{'car':car})

def inquiry(request,pk):
	car=Car.objects.get(pk=pk)
	if request.method=="POST":
		user=User.objects.get(email=request.session['email'])
		Inquiry.objects.create(
				user=user,
				car=car,
				from_date=request.POST['from_date'],
				to_date=request.POST['to_date'],
				number_of_cars=request.POST['number_of_cars'],
				color_of_car=request.POST['color_of_car'],
				location=request.POST['location'],
				contact_number=request.POST['contact_number'],
				email_address=request.POST['email_address']
			)
		return redirect('index')
	else:
		return render(request,'inquiry.html',{'car':car})

def view_inq(request):
	inq=Inquiry.objects.all()
	return render(request,'view_inq.html',{'inq':inq})

def c_details(request,pk):
	car=Car.objects.get(pk=pk)
	total=car.c_price
	client = razorpay.Client(auth = (settings.KEY_ID,settings.KEY_SECRET))
	payments=client.order.create({'amount':total*100, 'currency':'INR','payment_capture':1})
	print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",payments)
	car.razorpay_order_id=payments['id']
	car.save()

	return render(request,'c_details.html',{'total':total,'car':car})

