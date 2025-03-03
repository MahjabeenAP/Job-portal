from django.shortcuts import render,redirect,HttpResponse
# from .models import Employer,JobSeeker,Job,JobApplication
# from .models import CustomUser, Employer, JobSeeker
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

#   figma designs
def homefn(request):
    return render(request,'index.html')

def viewfn(request):
    return render(request,'view.html')

def jobsfn(request):
    return render(request,'job.html')

def myfn(request):
    return render(request,'my.html')

#  registration
