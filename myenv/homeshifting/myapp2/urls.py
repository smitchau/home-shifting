"""
URL configuration for homeshifting project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from myapp2 import views

urlpatterns = [
    path('',views.login,name='tlogin'), 
    path('tlogout/',views.tlogout,name='tlogout'), 
    path('home/',views.home,name='thome'), 
    path('accept/',views.accept,name='accept'), 
    path('reject/',views.reject,name='reject'), 
    path('finishride/',views.finishride,name='finishride'), 
    path('tsignup/',views.signup,name='tsignup'), 
    path('Mywallet/',views.Mywallet,name='Mywallet'), 
    path('tcontact/',views.tcontact,name='tcontact'), 
    path('profile/',views.profile,name='profile'), 
    path('update/',views.update,name='update'), 
    path('Withdrawal_funds/',views.Withdrawal_funds,name='Withdrawal_funds'), 
    path('tpackages/',views.tpackages,name='tpackages'), 
    path('tpayments/',views.tpayments,name='tpayments'), 
    path('pdetail/',views.pdetail,name='pdetail'), 
    path('tsuccess/', views.tsuccess, name='tsuccess'),
    path('changepassword/', views.changepassword, name='changepassword'),
]