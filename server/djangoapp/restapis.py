# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")

# ----------------------------
# GET request to backend
# ----------------------------
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"

    # Remove trailing '&' if any
    params = params.rstrip("&")
    request_url = backend_url + endpoint
    if params:
        request_url += "?" + params

    print(f"GET from {request_url}")

    try:
        response = requests.get(request_url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Network exception occurred: {e}")
        return None

# ----------------------------
# Future additions
# ----------------------------

# def analyze_review_sentiments(text):
#     request_url = sentiment_analyzer_url + "analyze/" + text
#     # Add code for retrieving sentiments
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"label": "neutral", "score": 0}

# def post_review(data_dict):
#     # Add code for posting review
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return {"status": 500, "message": "Failed to connect to backend"}
