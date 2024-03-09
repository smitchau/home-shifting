from django.shortcuts import render ,redirect
from .models import *
from django.contrib import messages


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
    return render(request,'myapp/index.html')

def vehical(request):
    return render(request,'myapp/vehical.html')    
 
def services(request):
    return render(request,'myapp/services.html')

def about(request):
    return render(request,'myapp/about.html')

def booking(request):
    if 'email' in request.session:
        if request.POST:
            u_id = User.objects.get(u_email = request.session['email'])
            
            book = Booking.objects.create(
                u_id = u_id,
                bname = request.POST['name'],
                housetype = request.POST['housetype'],
                source = request.POST['movingfrom'],
                destination = request.POST['movingto'],
                state = request.POST['state'],
                pcode = request.POST['pincode']
            )
            msg = 'Your Booking has been placed successfully.'
            messages.success(request,msg)
            return render(request,'myapp/booking.html') 
        else:
            return render(request,'myapp/booking.html')
    else:
        msg= "Please Login to Continue"
        messages.info(request,msg)
        return render(request, 'myapp/booking.html')
 
def contact(request):
    return render(request,'myapp/contact.html')



