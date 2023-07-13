from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User,auth
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from django.contrib.auth.decorators import login_required
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
#def contact(request):

def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login(request):
    return render(request, 'djangoapp/login.html')
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
# @login_required(login_url='signin')
def signup(request):

    if request.method == 'POST':
        # form = UserForm(request.POST)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        
        # if form.is_valid():
        if password == confirmpassword:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('djangoapp/signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('djangoapp/signup')
            elif len(password) < 8:
                messages.info(request, 'Password too short')
                return redirect('djangoapp/signup')
            elif not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric!!")
                return redirect('djangoapp/signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('djangoapp/login')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('djangoapp/signup')
        
    else:
        return render(request, 'djangoapp/signup.html')

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

