from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel, CarDealer
from .restapis import get_dealers_from_cf, get_request, get_dealer_reviews_from_cf, post_request
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
    if request.method == "GET":
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
# def contact(request):
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...


def login_request(request):
    context = {}

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return redirect("djangoapp:login")
    else:
        return redirect(request, 'djangoapp:login', context)

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...


def logout_request(request):
    print("Log out the user `{}`".format(request.user.username))
    logout(request)
    return redirect("djangoapp:index")
# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.debug('{} is new user'.format(username))
        if not user_exist:

            user = User.objects.create_user(
                username=username, password=password, first_name=first_name, last_name=last_name)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            return redirect("djangoapp:registration", context)

# Update the `get_dealerships` view to render the index page with a list of dealerships


def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://torydemaio-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        context["dealerships"] = get_dealers_from_cf(url)
        # Concat all dealer's short name
        print(context["dealerships"])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...


def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        url = "https://torydemaio-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/get_reviews"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        url2 = "https://torydemaio-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealers= get_dealers_from_cf(url2)
        context["dealers"] = dealers
        context["reviews"] = reviews
        print(context["reviews"])
        for dealer in dealers:
            if dealer.id == dealer_id:
                context["dealer"] = dealer
        # get dealer by id
        
        # Concat all dealer's short name
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# check if the user is authenticated
# ...


def add_review(request, dealer_id):
    context = {}
    cars = CarModel.objects.all()
    context["cars"] = cars
    if request.method == "GET":
        url = "https://torydemaio-3000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        for dealer in dealerships:
            if dealer.id == dealer_id:
                context["dealer"] = dealer
        return render(request, 'djangoapp/add_review.html', {'dealer_id': dealer_id, 'context': context})
    elif request.method == "POST":
        form = request.POST
        review = {}
        review["name"] = request.user.first_name + " " + request.user.last_name
        review["dealership"] = dealer_id
        review["review"] = form["content"]
        review["purchase"] = form.get("purchasecheck") is not None
        review["purchase_date"] = datetime.strptime(
            form["purchasedate"], "%m/%d/%Y").isoformat()
        car = CarModel.objects.get(pk=form["car"])
        review["car_make"] = car.make.name
        review["car_model"] = car.name
        review["car_year"] = car.year.strftime("%Y")
        json_payload = {"review": review}
        url = "https://torydemaio-5000.theiadocker-3-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/api/post_review"
        post_request(url, json_payload, dealerId=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)