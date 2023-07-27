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
        if 'PD07eyJ57AlcLTq2jM-m34rJhndDmEhrlwe40c3b_Pni':
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', 'PD07eyJ57AlcLTq2jM-m34rJhndDmEhrlwe40c3b_Pni'))
        else:
            response = requests.get(url, params=params)
    except:
        # If any error occurs
        print("Network exception occurred")
        return None

    status_code = response.status_code
    print("With status {} ".format(status_code))

    if status_code == 200:
        json_data = json.loads(response.text)
        print(json_data)
        return json_data
    else:
        print("Error: Unable to fetch data")
        return None


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)

import requests

def post_request(url, json_payload, **kwargs):
    try:
        # Call post method of requests library with URL and JSON payload
        response = requests.post(url, json=json_payload, **kwargs)
    except requests.exceptions.RequestException as e:
        # If any error occurs
        print("Network exception occurred:", e)
        return None

    status_code = response.status_code
    print("With status {} ".format(status_code))

    if status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print("Error: Unable to add review")
        return None

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealers_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter and state parameter
    json_result = get_request(url, state=state)
    if json_result and "rows" in json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

def analyze_review_sentiments(DealerReview):
    params = dict()
    params["text"] = kwargs["text"]
    params["version"] = kwargs["version"]
    params["features"] = kwargs["features"]
    params["return_analyzed_text"] = kwargs["return_analyzed_text"]
    response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', 'PD07eyJ57AlcLTq2jM-m34rJhndDmEhrlwe40c3b_Pni'))



def get_dealer_reviews_from_cf(url, dealer_Id):
    reviews_list = []
    # Call get_request with a URL parameter
    json_result = get_request(url, dealer_Id=int(dealer_Id))
    if json_result and "rows" in json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["rows"]
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            review_doc = review["review"]
            # Create a CarDealer object with values in `doc` object
            review_obj = DealerReview(
                id=review_doc["id"],
                name=review_doc["name"],
                dealership=review_doc["dealership"],
                review=review_doc["review"],
                purchase=review_doc["purchase"],
                purchase_date=review_doc["purchase_date"],
                car_make=review_doc["car_make"],
                car_model=review_doc["car_madel"],
                car_year=review_doc["car_year"],
                sentiment=None 
            )
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            reviews_list.append(review_obj)

    return reviews_list