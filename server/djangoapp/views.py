from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .models import CarDealer,CarModel
# from .restapis import related methods
from .restapis import get_dealers_from_cf,get_dealers_by_state,get_dealer_review_from_cf,analyze_review_sentiment,post_request
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


# Create a `contact` view to return a static contact page
#def contact(request):

# Create a `login_request` view to handle sign in request
# def login_request(request):
# ...

# Create a `logout_request` view to handle sign out request
# def logout_request(request):
# ...

# Create a `registration_request` view to handle sign up request
# def registration_request(request):
# ...

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://ab9704cf.us-south.apigw.appdomain.cloud/api/dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealerships_list"] = dealerships
        return render(request,'djangoapp/index.html',context)

def about_us(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)

def contact_us(request):
    context={}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html',context)

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/index.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)



# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...

def get_dealer_details(request, dealerId):
    context = {}
    if request.method == "GET":
        url = "https://ab9704cf.us-south.apigw.appdomain.cloud/api/review"
        dealerships_details = get_dealer_review_from_cf(url,dealerId = dealerId)
        context["dealerships_details"] = dealerships_details
        context["dealerId"]= dealerId
        return render(request,'djangoapp/dealer_details.html',context)

# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

def add_review(request,dealer_id):

    context = {}

    if (request.method == "GET"):

        if (request.user.is_authenticated):

            res = CarModel.objects.filter(dealer_id=dealer_id)

            context["cars"] = res
            context["dealer_id"] = dealer_id

            return render(request, 'djangoapp/add_review.html', context)

    elif (request.method == "POST"):

        idcar = 1

        if 'idcar' in request.POST:
            idcar = int(request.POST["car"])
            
        car = CarModel.objects.filter(id=idcar)

        check = False

        if 'purchasecheck' in request.POST:
            check = True
        else:
            check = False

        json_payload = dict()
        json_payload["id"] = int(dealer_id)
        json_payload["name"] = request.user.username
        json_payload["dealership"] = int(dealer_id)
        json_payload["review"] = request.POST["content"]
        json_payload["purchase"] = check

        if check and ('idcar' in request.POST):
            json_payload["purchase_date"] = request.POST["purchasedate"]
            json_payload["car_make"] = car[0].car_make.name
            json_payload["car_model"] = car[0].name
            json_payload["car_year"] = car[0].year.strftime("%Y")
            
        else:
            json_payload["purchase_date"] = ""
            json_payload["car_make"] = ""
            json_payload["car_model"] = ""
            json_payload["car_year"] = ""

        res = post_request("https://ab9704cf.us-south.apigw.appdomain.cloud/api/review", json_payload, dealerId=dealer_id)

        return redirect("djangoapp:dealer_details", dealerId=dealer_id)








            




#json_payload = dict()
#           json_payload["id"] = 444
#          json_payload["name"] = "Rodrigo"
#          json_payload["dealership"] = dealer_id
#            json_payload["review"] = "The best car ever"
#            json_payload["purchase"] = True
#            json_payload["purchase_date"] = datetime.utcnow().isoformat()
#            json_payload["car_make"] = "Renault"
#            json_payload["car_model"] = "Sedan"
#            json_payload["car_year"] = 2020
#
#            res = post_request("https://ab9704cf.us-south.apigw.appdomain.cloud/api/review", json_payload, dealerId=dealer_id)
#
#            return HttpResponse(res)
