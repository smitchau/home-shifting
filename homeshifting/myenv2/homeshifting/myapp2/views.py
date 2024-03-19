from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse
from .models import *
from myapp.models import *
from myapp.views import *
from django.contrib import messages
from django.conf import settings
import razorpay
from django.utils import timezone
# Create your views here.

def home(request):
    try:
        u_email = request.session.get('email')
        user = get_object_or_404(User, u_email=u_email)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
        truckpartner = Truckpartner.objects.get(t_email=request.session['temail'])
        if truckpartner.status == True:
            if booking.statuscheck == False:
                if booking.status != 'finish':
                    u_email = request.session.get('email')
                    user = get_object_or_404(User, u_email=u_email)
                    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
                    if booking.htype in ['1 BHK', '2 BHK'] and truckpartner.package_type in ['silver', 'gold']:
                        return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner})
                    elif booking.htype in ['1 BHK', '2 BHK', '3 BHK', '4 BHK'] and truckpartner.package_type == 'platinum':
                        return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
    except:
        pass
    return render(request,"home.html")

def accept(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        
        u_email = request.session.get('email')
        user = get_object_or_404(User, u_email=u_email)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

        truckpartner.on_work = True
        truckpartner.save()

        booking.statuscheck = True
        booking.save()

        u_email = request.session.get('email')
        user = get_object_or_404(User, u_email=u_email)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
        print("------------------",booking.finish_active)
        return render(request,"accept.html",{'user':user , "booking":booking})
    except Exception as e:
        print('============---------------',e)
        pass
    return render(request,"home.html")
        
    
def reject(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
    truckpartner.on_work = False
    truckpartner.save()
    return redirect('thome')

def finishride(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
    truckpartner.on_work = False
    
    u_email = request.session.get('email')
    user = get_object_or_404(User, u_email=u_email)
    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
    booking.statuscheck == False
    booking.status = 'finish'
    truckpartner.save()
    booking.save()
    print("------------------------------",booking.finish_active)
    return redirect('thome')

def signup(request):
    if request.POST:
            try:
                print(">>>>>>>>>>>>>page loade")
                truckpartner = Truckpartner.objects.get(t_email = request.POST['email'])

                if request.session['tpemail'] == request.POST['email']:
                    print(">>>>>>>>>>>truckpartner",truckpartner)
                    messages.error(request,'Email alredy exists!!!')
                    return redirect('tlogin')
                else:
                    return redirect('tpackages')
                
            except:
                if request.POST['password'] == request.POST['cpassword']:
                    truckpartner = Truckpartner.objects.create(
                        t_name=request.POST['name'],
                        t_email=request.POST['email'],
                        t_password=request.POST['password'],
                        t_contact=request.POST['contact'],
                        t_rcnumber=request.POST['rcn'],
                        t_aadharcard_details=request.POST['adhaar'],
                        t_pancard_details=request.POST['pan'],
                        t_drivinglicence_details=request.POST['driving'],
                    )
                    print(">>>>>>user ",truckpartner.t_name)
                    msg="Sign Up Successful"
                    messages.success(request,msg)
                    return redirect('pdetail')

                else:
                    msg1="Password and Confim Password Does Not Matched !!!"
                    messages.error(request,msg1)
                    return redirect('tsignup')
    else:
        return render(request,"tsignup.html")

def tpackages(request):
    if request.POST:
        try:
            truck =Truckpartner.objects.get(t_email = request.POST['email'])

            price = int(request.POST.get('price'))
            
            truck.price = price
            truck.package_type = request.POST['ptype']
            truck.truck_type = request.POST['vtype']
            truck.start_date = timezone.now().date()
            truck.end_date = truck.start_date + timezone.timedelta(days=30)
            print('==========truckprice',truck.price)

            #request.session['email'] = request.POST['email']

            client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRET))
            payment = client.order.create({'amount': truck.price * 100, 'currency': 'INR', 'payment_capture': 1})
            truck.razorpay_order_id = payment['id']  
            truck.save()

            request.session['tpemail']= request.POST['email']
            #print(p)
            context = {
                    'payment': payment,
                    'truck':truck,  # Ensure the amount is in paise
                }
            print(context)
            return render(request,'tpayments.html',context)

        except Exception as e:
            print("===================================",e)
            return render(request,"tpackages.html")
    else:
        return render(request,"tpackages.html")
    
def tpayments(request):
    #truck =Truckpartner.objects.get(t_email = request.POST['temail'])
    return render(request,"tpayments.html")

def pdetail(request):
    return render(request,'pdetail.html')

def tsuccess(request):
    try:
        truck = Truckpartner.objects.get(t_email = request.session['tpemail'])

        print('========================================',truck.t_email)

        truck.razorpay_payment_id = request.GET.get('razorpay_payment_id')

        print('========================================',truck.razorpay_payment_id)
        truck.save()
        return render(request,'tsuccess.html')
    except Exception as e:
        print(e)
        return render(request,'tsuccess.html')
    
 
def contact(request):
    return render(request,'contact.html')

def login(request):
    if request.POST:
            print(">>>>>>>>>>>>>>>>>page loade login")
            try:
                truckpartner = Truckpartner.objects.get(t_email = request.POST['email'] , t_password = request.POST['pass'])
                print('hello')
                if truckpartner.razorpay_payment_id:
                    print('hello')
                    request.session['temail']=truckpartner.t_email
                    request.session['tpassword']=truckpartner.t_password
                    request.session['tname']=truckpartner.t_name
                    request.session['tpicture'] = truckpartner.t_picture.url
                    request.session['tcontact'] = truckpartner.t_contact
                    truckpartner.status = True
                    truckpartner.save()
                    print('login status truck',truckpartner.status)
                    
                    print(">>>>>>>>>session start : ",request.session['temail'])
                    msg1 = "login succesfully done"
                    messages.success(request,msg1)
                    return render(request,'home.html')
                else:
                    return redirect('tpackages')
            except: 
                msg="Your email or password is not match !!!!"
                messages.error(request,msg)
                return render(request,'login.html')
    else:
        return render(request,'login.html')

def tlogout(request):
    if 'temail' in  request.session:
        try:
            truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
            truckpartner.status = False
            truckpartner.save()
            del request.session['temail']
            del request.session['tpassword']
            del request.session['tname']
            del request.session['tpicture']
            del request.session['tcontact']
            return redirect('tsignup')
        except Exception as e:
            print(e)
            return redirect('tsignup')
    else:
        return render(request,'login.html')
    
def Mywallet(request):
    return render(request,'Mywallet.html')

def update(request):
    if request.POST:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        truckpartner.t_name = request.POST['name']
        truckpartner.t_contact = request.POST['number']
        if 'picture' in request.FILES:
            truckpartner.t_picture = request.FILES['picture']
        
        truckpartner.save()

        request.session['tname'] = truckpartner.t_name
        request.session['tpicture'] = truckpartner.t_picture.url
        request.session['tcontact'] = truckpartner.t_contact
        
        msg ="profile successfully update"
        messages.success(request,msg)
        return redirect('profile')
    else:
        return render(request,"update.html")

def profile(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
    return render(request,'profile.html',{"truckpartner":truckpartner})

def Withdrawal_funds(request):
    return render(request,'Withdrawal_funds.html')

