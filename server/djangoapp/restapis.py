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
    apikey = kwargs.get('apikey')
    try:
        # Call get method of requests library with URL and parameters
        if apikey:
            response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', apikey))
        else:
            response = requests.get(url, params=kwargs)
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

def post_request(url, json_payload):
    try:
        # Call post method of requests library with URL and JSON payload
        response = requests.post(url, json=json_payload)
    except requests.exceptions.RequestException as e:
        # If any error occurs (e.g., network or HTTP-related errors)
        print("Network exception occurred:", e)
        return None

    status_code = response.status_code
    print("With status {} ".format(status_code))

    if status_code == 200:
        json_data = response.json()
        print(json_data)
        return json_data  # Return the JSON response data on successful response
    else:
        print("Error: Unable to add review")
        return None  # Return None if there's an error or unsuccessful response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list


# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list

def get_dealers_from_cf(url, state, apikey):
    results = []
    # Call get_request with a URL parameter and state parameter
    json_result = get_request(url, state=state, apikey=apikey)
    if json_result and "result" in json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], state=dealer_doc["state"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results



# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative

from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def analyze_review_sentiments(review_text, api_key, service_url):
    authenticator = IAMAuthenticator(api_key)
    nlp_service = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )

    nlp_service.set_service_url(service_url)

    # Specify the features you want to extract (sentiment analysis in this case)
    features = Features(sentiment=SentimentOptions())

    response = nlp_service.analyze(
        text=review_text,
        features=features
    ).get_result()

    sentiment_score = response['sentiment']['document']['score']
    sentiment_label = response['sentiment']['document']['label']

    return sentiment_score, sentiment_label



def get_dealer_reviews_from_cf(url, dealer_Id, apikey):
    reviews_list = []
    dealer_Id=int(dealer_Id)
    # Call get_request with a URL parameter
    json_result = get_request(url, dealer_Id=dealer_Id, apikey=apikey)
    if json_result and "matched_reviews" in json_result:
        # Get the list of reviews
        reviews = json_result["matched_reviews"]
        # For each review object in the list
        for review in reviews:
            # Create a DealerReview object with values in the review dictionary
            review_obj = DealerReview(
                id=int(review.get("id", 0)),  # Use 0 as the default value if "id" is missing
                name=review.get("name", ""),  # Use an empty string as the default value if "name" is missing
                dealership=int(review.get("dealership", 0)),  # Use 0 as the default value if "dealership" is missing
                review=review.get("review", ""),  # Use an empty string as the default value if "review" is missing
                purchase=review.get("purchase", False),  # Use False as the default value if "purchase" is missing
                purchase_date=review.get("purchase_date", ""),  # Use an empty string as the default value if "purchase_date" is missing
                car_make=review.get("car_make", ""),  # Use an empty string as the default value if "car_make" is missing
                car_model=review.get("car_model", ""),  # Use an empty string as the default value if "car_model" is missing
                car_year=int(review.get("car_year", 0)),  # Use 0 as the default value if "car_year" is missing
                sentiment=None
            )
            if len(review_obj.review.strip()) >= 10:  # Set an appropriate minimum length (e.g., 10 characters)
                # Perform sentiment analysis and update review_obj.sentiment
                sentiment_score, sentiment_label = analyze_review_sentiments(
                    review_obj.review,'PD07eyJ57AlcLTq2jM-m34rJhndDmEhrlwe40c3b_Pni', 'https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/533419e3-c83c-4be0-aaa6-fe818004a6f0'
                )
                review_obj.sentiment = {
                    'score': sentiment_score,
                    'label': sentiment_label
                }
            else:
                # Handle reviews with insufficient text (optional)
                review_obj.sentiment = {
                    "label": "Unknown",
                    "score": 0.0
                }
            reviews_list.append(review_obj)

    return reviews_list
