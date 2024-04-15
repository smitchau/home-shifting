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
    if request.session["temail"]:
        try:
            u_email = request.session.get('email')
            user = get_object_or_404(User, u_email=u_email)
            booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
            truckpartner = Truckpartner.objects.get(t_email=request.session['temail'])
            if truckpartner.status == True:
                if booking.statuscheck == False:
                    if booking.status != 'finish' and  booking.status != 'cancle':
                        # u_email = request.session.get('email')
                        # user = get_object_or_404(User, u_email=u_email)
                        # booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')
                        if booking.htype in ['2 BHK'] and truckpartner.package_type in ['silver', 'gold','platinum']:
                            return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner})
                        elif booking.htype in ['1 BHK'] and truckpartner.package_type in ['silver', 'platinum']:
                            return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
                        elif booking.htype in ['3 BHK'] and truckpartner.package_type in ['gold', 'platinum']:
                            return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
                        elif booking.htype in ['1 BHK', '2 BHK', '3 BHK', '4 BHK'] and truckpartner.package_type == 'platinum':
                            return render(request, "home.html", {'user': user, "booking": booking, "truckpartner": truckpartner}) 
        except Exception as e:
            print(e)
            return render(request,'home.html')
        return render(request,"home.html")
    else:
        return redirect('tlogin')
def accept(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        
        u_email = request.session.get('email')
        user = get_object_or_404(User, u_email=u_email)
        booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

        truckpartner.on_work = True
        truckpartner.save()

        booking.status = "on-the-way"

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
    reject_status = False
    if truckpartner.on_work == False:
        reject_status =True
        msg = "Ride Rejected successfully."
        messages.success(request,msg)
        return render (request,'home.html',{'reject_status':reject_status})
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

    #----------------------------------------------------
    u_email = request.session.get('email')
    user = get_object_or_404(User, u_email=u_email)
    booking = Booking.objects.filter(userid=user).latest('razorpay_order_id')

    
    # Check if the last ride was more than 24 hours ago
    ride = Rides.objects.get(truckpartner=truckpartner)

    if ride.today_earning == 0:
        ride.start_time =  timezone.now()
        ride.expiry_time = ride.start_time + timedelta(days=1)
        ride.save()

    current_datetime = timezone.now()

    if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
        ride.today_earning = 0
        ride.save()

        # Update total_trip and total_earning
    ride.total_trip += 1
    ride.today_earning += booking.price
    ride.total_earning += booking.price
    ride.save()

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

        ride = Rides.objects.create(

            truckpartner = truck
        
        )
        print("---------------create ride for truckpartners",ride)

        return render(request,'tsuccess.html')
    except Exception as e:
        print(e)
        return render(request,'tsuccess.html')
    
 
def tcontact(request):
    if request.POST:
        tcontact = Tcontact.objects.create(
            name = request.POST['name'],
            email = request.POST['email'],
            number = request.POST['number'],
            message = request.POST['msg']
        )
        return render(request,'home.html')
    else:
        return render(request,'tcontact.html')

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
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        ride = Rides.objects.get(truckpartner = truckpartner)
        print("============",ride)
        transactions = Transactions.objects.filter(truckpartner = truckpartner)
        a = 0
        for i in transactions:
            a += i.amount
        
        print("============",transactions)
        current_datetime = timezone.now()

        if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
            ride.today_earning = 0
            ride.save()

        return render(request,'Mywallet.html',{'ride':ride,'transactions':transactions,'a':a})
    except Exception as e:
        print(e)
        return render(request,'Mywallet.html')

def update(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        if request.POST:
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
    except:
        pass

def profile(request):
    truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
    ride = Rides.objects.get(truckpartner = truckpartner)
    current_datetime = timezone.now()

    if ride.expiry_time is not None:
        if current_datetime >= ride.expiry_time:
            # If last ride was more than 24 hours ago, reset today's earnings to 0
            ride.today_earning = 0
            ride.save()
        print(ride.today_earning)
        return render(request,'profile.html',{"truckpartner":truckpartner , 'ride':ride})
    else:
        return render(request,'profile.html',{"truckpartner":truckpartner , 'ride':ride})
   
def Withdrawal_funds(request):
    try:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        ride = Rides.objects.get(truckpartner = truckpartner)

        if request.POST:
            print("==========post")
            if request.POST['accountno'] == request.POST["caccountno"]:
                print("==========first",type(ride.total_earning))
                print("==========first",type(request.POST["amount"]))
                if ride.total_earning >= int(request.POST["amount"]):
                    print("==========second")
                    transactions = Transactions.objects.create(
                        truckpartner = truckpartner,
                        rides = ride,
                        account_holder_name = request.POST['hname'],
                        account_number = request.POST['accountno'],
                        ifsc_code = request.POST['ifsc_code'],
                        amount = request.POST['amount'],
                    )
                    return redirect('Mywallet')
                else:
                    msg="inficiunce Balance!!"
                    messages.error(request,msg)
                    return render(request,'Withdrawal_funds.html')
            else:
                msg="account number and confirm account number does not match !!"
                messages.error(request,msg)
                return render(request,'Withdrawal_funds.html')
        else:
            return render(request,'Withdrawal_funds.html')
        
    except Exception as e:
        print(e)
        return render(request,'Withdrawal_funds.html')
    
def changepassword(request):
    if request.POST:
        truckpartner = Truckpartner.objects.get(t_email = request.session['temail'])
        if truckpartner.t_password == request.POST["current_pass"]:
            if request.POST["new_pass"] == request.POST["c_pass"]:

                truckpartner.t_password = request.POST["new_pass"]
                truckpartner.save()

                del request.session['temail']
                del request.session['tpassword']
                del request.session['tname']
                del request.session['tpicture']
                del request.session['tcontact']
                return redirect('tsignup')
            else:
                msg = "new password and confirm password does not match !!"
                messages.error(request,msg)
                return render(request,'changepassword.html')
        else:
            msg = "current password does not match !!"
            messages.error(request,msg)
            return render(request,'changepassword.html')
    else:
        return render(request,'changepassword.html')