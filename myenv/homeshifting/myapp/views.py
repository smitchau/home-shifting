from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.http import JsonResponse
import random
import requests
from django.conf import settings
from django.urls import reverse
import razorpay
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.
def signup(request):
        if request.POST:
            try:
                print(">>>>>>>>>>>>>page loade")
                user = User.objects.get(u_email = request.POST['email'])
                print(">>>>>>>>>>>user",user)
                messages.error(request,'Email alredy exists!!!')
                return redirect('home')
                
            except:
                if request.POST['password'] == request.POST['cpassword']:
                    user = User.objects.create(
                        u_name=request.POST['name'],
                        u_email=request.POST['email'],
                        u_contact=request.POST['contact'],
                        u_password=request.POST['password'],
                    )
                    print(">>>>>>user ",user.u_name)
                    msg="Sign Up Successful"
                    messages.success(request,msg)
                    return redirect('home')

                else:
                    msg1="Password and Confim Password Does Not Matched !!!"
                    messages.error(request,msg1)
                    return redirect('home')
        else:
            return render(request,"myapp/index.html")

def login(request):
    if request.POST:
        print(">>>>>>>>>>>>>>>>>page loade login")
        try:
            user = User.objects.get(u_email=request.POST['email'] , u_password=request.POST['password'])
            request.session['email']=user.u_email
            request.session['password']=user.u_password
            print(">>>>>>>>>session start : ",request.session['email'])
            msg1 = "login succesfully done"
            messages.success(request,msg1)
            return redirect('home')
        except: 
            msg="Your email or password is not match !!!!"
            messages.error(request,msg)
            return redirect('home')
    else:
       return redirect('home')

def logout(request):
    if "email" in request.session:
        del request.session['email']
        del request.session['password']
        return redirect('home')   
    else:
        return render(request, 'myapp/index.html')

def changepassword(request):
    if 'email' in request.session:
        if request.POST:
            print('>>>>>>>>>>>>>page loded',request.session['password'])
            if request.session['password'] == request.POST['cu_password']:
                if request.POST['npassword'] == request.POST['cpassword']:
                    user = User.objects.get(u_email=request.session['email'])
                    user.u_password = request.POST['npassword']
                    print(">>>>>>>>>>>>>>>>>>>confirm pass: ",user.u_password)
                    user.save()
                    del request.session['email']
                    del request.session['password']
                    request.session['password']= user.u_password 
                
                    msg = 'Successfully password change'
                    messages.success(request,msg)
                    return redirect('home')
                else:
                    msg = 'new password and Confirm New Password does not match !!'
                    messages.error(request,msg)
                    return redirect('home')
            else:
                msg = 'current password does not exist !!'
                messages.error(request,msg)
                return redirect('home')
            
        else: 
            return render(request, 'myapp/index.html')
    else:
        return render(request, 'myapp/index.html')


def home(request):
    if request.POST:
        if 'email' in request.session:
            user = User.objects.get(u_email = request.session['email'])
            #booking = Booking.objects.filter(userid = user).latest('razorpay_order_id')
            book = Booking.objects.filter(userid = user)
            #booking = [order.razorpay_order_id for order in book]
        
            for booking in book:
                print("======================",booking.razorpay_order_id)
                if booking.razorpay_order_id == request.POST['order_id']:
                    print("hello")
                    booking = get_object_or_404(Booking, pk=booking.pk)
                    print(booking)
                    context = {'booking': booking}
                    return render(request, "myapp/utrack.html",context)
            else:
                msg = "invalid"
                messages.error(request,msg)
                return render(request,'myapp/index.html')
        else:
            msg = "email is not register !!"
            messages.error(request,msg)
            return render(request,'myapp/index.html')
    else:
        return render(request,'myapp/index.html')

#def home(request):
#    return render(request,'myapp/index.html')   
 
def vehical(request):
    return render(request,'myapp/vehical.html')    
 
def services(request):
    return render(request,'myapp/services.html')

def about(request):
    return render(request,'myapp/about.html')

def booking(request):
    if 'email' in request.session:
        if request.POST:
            userid = User.objects.get(u_email=request.session['email'])
            price = int(request.POST.get('price'))
            book = Booking.objects.create(
                htype=request.POST['htype'],
                userid=userid,
                bname=request.POST['name'],
                movefrom=request.POST['moving_from'],
                moveto=request.POST['moving_to'],
                state=request.POST['state'],
                zipcode=request.POST['zipcode'],
                price=price
            )
            
            print(type(book.price))
            print("=================================")
    
            client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': book.price * 100, 'currency': 'INR', 'payment_capture': 1})
            book.razorpay_order_id = payment['id']  
            book.save()

            request.session['name']= book.bname
            print(request.session['name'])

            context = {
                    'payment': payment,
                    'book':book,  # Ensure the amount is in paise
                }
            
            print("=======================",context)
            print("&7777777777777777777777",payment)


            
            return render(request, 'myapp/payments.html',context)
        else:
            return render(request, "myapp/booking.html")
    else:
        messages.info(request, "Please login now.........")
        return render(request, "myapp/booking.html")
    
def payments(request):
    return render(request,"myapp/payments.html")

def mymail(subject, template, to, context,order_id):
    subject = subject
    template_str = 'myapp/' + template +'.html'
    context['order_id'] = order_id
    html_message = render_to_string(template_str, context)
    plain_message = strip_tags(html_message)
    from_email = 'smitchauhan2712@gmail.com'
    send_mail(
        subject,
        plain_message,
        from_email,
        [to],
        html_message=html_message,
        fail_silently=False,
    )
    
def success(request):
   u_email = request.session.get('email')

   if u_email:
        user = get_object_or_404(User, u_email=u_email)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

        razorpay_payment_id = request.GET.get('razorpay_payment_id')

        if razorpay_payment_id:
            # Update the booking instance with the Razorpay payment ID
            booking.razorpay_payment_id = razorpay_payment_id
            booking.save()

            subject = 'booking successfully'
            template = "etemplate"
            to = user.u_email
            context = {'user':user.u_name}
            order_id = booking.razorpay_order_id
            mymail(subject, template, to, context,order_id)
            print('======================send otp successfully')

        return render(request,'myapp/success.html')
   else:
        msg= "Please login....."
        messages.info(request,msg)
        return render(request,"myapp/index.html")

def contact(request):
    if request.POST:
        contact = Contact.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            number = request.POST['number'],
            message = request.POST['msg']
        )
        msg = "message successfully send"
        messages.success(request,msg)
        return render(request,'myapp/index.html')
    else:
        return render(request,'myapp/contact.html')

def mybookings(request):
    user = User.objects.get(u_email = request.session['email'])
    user_bookings = Booking.objects.filter(userid=user)
    return render(request,"myapp/mybookings.html",{'user_bookings': user_bookings})


def utrack(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    context = {'booking': booking}
    print(context)
    return render(request, "myapp/utrack.html", context)

def cancle(request,pk):
    booking = Booking.objects.get(pk=pk)
    u_email = request.session.get('email')
    user = get_object_or_404(User, u_email=u_email)

    # Check if the booking is not already canceled
    if booking.status != 'cancel':
        # Set the status to 'cancel'
        booking.status = 'cancel'
        booking.save()

        subject = 'booking cancel successfully'
        template = "ctemplate"
        to = user.u_email
        context = {'user':user.u_name}
        order_id = booking.razorpay_order_id
        mymail(subject, template, to, context,order_id)
        print('======================send otp successfully')

    # Redirect back to the user's bookings page
        msg = "cancel bookin successfully"
        messages.success(request,msg)
        return redirect('mybookings')
    else:
        msg = "olready cancel bookin"
        messages.error(request,msg)
        return redirect('mybookings')


