import requests
import json
from .models import CarDealer,DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data

def analyze_review_sentiment(dealerreview):
    params = dict()
    params["text"] = dealerreview
    params["version"] = "2021-08-01"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = True
    params["language"] = "en"

    response = requests.get("https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/1dcb84cb-41ed-482c-8247-d92ab1ad2b91/v1/analyze",params = params,headers={'Content-Type': 'application/json'},auth=HTTPBasicAuth('apikey', "Itp6ntlUsznRKL7jPhZSGwNqrbw4Wa5rStluUMf_A7tC") )

    res = json.loads(response.text)

    return res["sentiment"] ["document"] ["label"]
# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

def post_request(url,json_payload,**kwargs):
    try:   
        response = requests.post(url,params=json_payload)
    except:
        print("Network exception occurred")

    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   idcar=dealer["id"], lat=dealer["lat"], lon=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zi=dealer["zip"])

            results.append(dealer_obj)

    return results

def get_dealers_by_state(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,state = kwargs["state"])
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer["address"], city=dealer["city"], full_name=dealer["full_name"],
                                   idcar=dealer["id"], lat=dealer["lat"], lon=dealer["long"],
                                   short_name=dealer["short_name"],
                                   st=dealer["st"], zi=dealer["zip"])
            results.append(dealer_obj)

    return results




# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealer_review_from_cf(url, **kwargs):
    results = []
   
    json_result = get_request(url, dealerId = kwargs["dealerId"])
    if json_result:
        
        dealers = json_result["results"]

        print(dealers)
        
        for dealer in dealers:
            
            dealer_obj = DealerReview(ds=dealer["dealership"], name=dealer["name"], purchase=dealer["purchase"],
                                   review=dealer["review"], purchase_date=dealer["purchase_date"], car_make=dealer["car_make"],
                                   car_model=dealer["car_model"],
                                   car_year=dealer["car_year"], idr=dealer["id"])

            dealer_obj.sentiment = analyze_review_sentiment(dealer_obj.review)

            results.append(dealer_obj)

    return results


# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



