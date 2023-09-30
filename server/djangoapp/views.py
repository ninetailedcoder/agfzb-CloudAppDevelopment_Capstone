from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel,CarDealer
from .restapis import get_dealers_from_cf, get_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    context = {"dealerships": CarDealer.objects.all()}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
#def contact(request):
def contact(request):
    context={}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...
def login_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return redirect("djangoapp:index") 

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...
def logout_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/index.html', context)
    if request.method == "POST":
        logout(request)
        return redirect("djangoapp:index")
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...
def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        return redirect("djangoapp:index")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = " https://torydemaio-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        url = " https://torydemaio-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/get"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # Concat all dealer's short name
        review_names = ' '.join([review.name for review in reviews])
        # Return a list of dealer short name
        return HttpResponse(review_names)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# check if the user is authenticated
# ...
def add_review(request, dealer_id):
    if request.method == "GET":
        url = " https://torydemaio-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context = {"dealerships": dealerships}
        return render(request, 'djangoapp/add_review.html', context)
    if request.method == "POST":
        if request.user.is_authenticated:
            review = {}
            review["name"] = request.user.first_name + " " + request.user.last_name
            review["dealership"] = dealer_id
            review["review"] = request.POST["content"]
            review["purchase"] = request.POST.get("purchasecheck")
            if review["purchase"] == "on":
                review["purchase"] = True
            else:
                review["purchase"] = False
            review["purchase_date"] = request.POST["purchasedate"]
            car = {}
            car["car_make"] = request.POST["car_make"]
            car["car_model"] = request.POST["car_model"]
            car["car_year"] = request.POST["car_year"]
            review["car"] = car
            json_payload = {"review": review}
            url = " https://torydemaio-3000.theiadocker-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/post"
            response = post_request(url, json_payload)
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        else:
            return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
        
        