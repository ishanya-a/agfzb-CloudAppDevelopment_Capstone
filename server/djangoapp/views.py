from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User,auth
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_request, get_dealer_reviews_from_cf
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
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            auth.login(request, user)
            return redirect('/djangoapp')
        else:
            # If not, return to login page again
            messages.info(request, 'Credentials Invalid')
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)
# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('djangoapp/registration')

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
# @login_required(login_url='signin')
def registration(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['psw']
        # <HINT> Get user information from request.POST
        # <HINT> username, first_name, last_name, password
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
            user.save()
            # <HINT> Login the user and 
            # redirect to course list page
            return redirect("/djangoapp")
        else:
            return render(request, 'djangoapp/registration.html', context)
            
# Update the `get_dealerships` view to render the index page with a list of dealerships
from django.http import HttpResponse
from .restapis import get_dealers_from_cf

def get_dealerships(request):
    if request.method == "GET":
        state = request.GET.get('state', 'california')  # Get the 'state' query parameter from the request
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/4ee50bfd-3284-45d1-8f8b-8fec618ddb96/dealership-package/get-dealership"
        # Get dealers from the URL for the specified state
        dealerships = get_dealers_from_cf(url, state=state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def dealer_details(request):
    return render(request, 'djangoapp/dealer_details.html')

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request):
    return render(request, 'djangoapp/add_review.html')

def car_make(request):
    if request.method == "POST":
        # Get data from the request.POST dictionary
        name = request.POST['name']
        description = request.POST['description']
        founding_year = request.POST['founding_year']
        headquarters = request.POST['headquarters']
        website = request.POST['website']

        # Create a new CarMake object
        car_make = CarMake(
            name=name,
            description=description,
            founding_year=founding_year,
            headquarters=headquarters,
            website=website,
        )

        # Save the CarMake object to the database
        car_make.save()

        # Redirect to the success page or any other page as needed
        return redirect('/djangoapp')  # Replace 'success_page' with the name of your success page URL pattern
    else:
        # Render the form page if the request method is GET
        return render(request, 'djangoapp/car_make.html')

def car_model(request):
    if request.method == "POST":
        # Get data from the request.POST dictionary
        # car_make_id = request.POST['car_make']
        dealer_id = request.POST['dealer_id']
        name = request.POST['name']
        car_type = request.POST['car_type']
        year = request.POST['year']
        engine_capacity = request.POST['engine_capacity']
        transmission = request.POST['transmission']
        price = request.POST['price']
        image = request.FILES.get('image')  # For handling image upload

            # Assuming 'car_make_id' is the ID of the CarMake object to which this CarModel belongs
            # car_make = CarMake.objects.get(id=car_make_id)

            # Create a new CarModel object
        car_model = CarModel(
            dealer_id=dealer_id,
            name=name,
            car_type=car_type,
            year=year,
            engine_capacity=engine_capacity,
            transmission=transmission,
            price=price,
            image=image,
        )

            # Save the CarModel object to the database
        car_model.save()

            # Redirect to the success page or any other page as needed
        return redirect('/djangoapp')  # Replace 'success_page' with the name of your success page URL pattern
    else:
    # Render the form page if the request method is GET
        return render(request, 'djangoapp/car_model.html')


def get_Reviews(request):
    if request.method == "GET":
        dealer_Id = request.GET.get('dealer_Id', 23)  # Get the 'state' query parameter from the request
        url = "https://eu-gb.functions.appdomain.cloud/api/v1/web/4ee50bfd-3284-45d1-8f8b-8fec618ddb96/dealership-package/get-review?dealer_Id=23"
        # Get dealers from the URL for the specified state
        reviews = get_dealer_reviews_from_cf(url, dealer_Id=dealer_Id)
        # Concat all dealer's short name
        # dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(reviews)