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
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('vehical/',views.vehical,name='vehical'),
    path('services/',views.services,name='services'),
    path('about/',views.about,name='about'),
    path('booking/',views.booking,name='booking'),
    path('contact/',views.contact,name='contact'),
    path('payments/',views.payments,name='payments'),
    path('success/',views.success,name='success'),
    path('mybookings/',views.mybookings, name='mybookings'),
    path('utrack/ <int:pk>/',views.utrack, name="utrack"),
    path('cancle/ <int:pk>/',views.cancle, name="cancle"),
    
]