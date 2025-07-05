# Uncomment the required imports before adding the code
from .restapis import get_request, analyze_review_sentiments, post_review
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .models import CarMake, CarModel
from .populate import initiate  # ✅ Import the populate function

# Get an instance of a logger
logger = logging.getLogger(__name__)

# -------------------------------
# Authentication Views
# -------------------------------

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug(f"{username} is a new user.")

    if not username_exist:
        user = User.objects.create_user(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password,
                                        email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})

# -------------------------------
# Get Cars
# -------------------------------

@csrf_exempt
def get_cars(request):
    count = CarMake.objects.count()

    if count == 0:
        initiate()  # Automatically populate the database

    car_models = CarModel.objects.select_related('car_make')

    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})


# -------------------------------
# Step 1, 2, 3: Dealer Views
# -------------------------------

def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealer_details = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealer_details})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        if reviews:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail.get('review', ''))
                sentiment = response.get('label') or response.get('sentiment') or "neutral"
                review_detail['sentiment'] = sentiment
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# -------------------------------
# Step 4: Add Review View
# -------------------------------

@csrf_exempt
def add_review(request):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "response": response})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
# Uncomment the required imports before adding the code
from .restapis import get_request, analyze_review_sentiments, post_review
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
import logging
import json

from .models import CarMake, CarModel
from .populate import initiate  # ✅ Import the populate function

# Get an instance of a logger
logger = logging.getLogger(__name__)

# -------------------------------
# Authentication Views
# -------------------------------

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)


def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)


@csrf_exempt
def registration(request):
    context = {}
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']

    username_exist = False
    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug(f"{username} is a new user.")

    if not username_exist:
        user = User.objects.create_user(username=username,
                                        first_name=first_name,
                                        last_name=last_name,
                                        password=password,
                                        email=email)
        login(request, user)
        return JsonResponse({"userName": username, "status": "Authenticated"})
    else:
        return JsonResponse({"userName": username, "error": "Already Registered"})

# -------------------------------
# Get Cars
# -------------------------------

@csrf_exempt
def get_cars(request):
    count = CarMake.objects.count()

    if count == 0:
        initiate()  # Automatically populate the database

    car_models = CarModel.objects.select_related('car_make')

    cars = []
    for car_model in car_models:
        cars.append({
            "CarModel": car_model.name,
            "CarMake": car_model.car_make.name
        })

    return JsonResponse({"CarModels": cars})


# -------------------------------
# Step 1, 2, 3: Dealer Views
# -------------------------------

def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})


def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        dealer_details = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": dealer_details})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        if reviews:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail.get('review', ''))
                sentiment = response.get('label') or response.get('sentiment') or "neutral"
                review_detail['sentiment'] = sentiment
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})


# -------------------------------
# Step 4: Add Review View
# -------------------------------

@csrf_exempt
def add_review(request):
    if request.user.is_anonymous == False:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "response": response})
        except:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
