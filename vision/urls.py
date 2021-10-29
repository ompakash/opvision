from django.urls import path
from vision.views import home,about,blog,contact,login,signup

urlpatterns=[
path('',home,name='home'),
path('about',about,name='about'),
path('blog',blog,name='blog'),
path('contact',contact,name='contact'),
path('login',login,name='login'),
path('signup',signup,name='signup'),
]