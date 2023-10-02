import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from .models import CarDealer
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions


def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    if api_key:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs, auth=HTTPBasicAuth('apikey', api_key))
    else:
        # If any error occurs
        request.get(url, params=params)

        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
def get_dealers_from_cf(url, **kwargs):
    results = []
    state = kwargs.get("state")

    if state:
        json_result = get_request(url, state=state)
    else:
        json_result = get_request(url)
    # Call get_request with a URL parameter
    
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url, dealerId=dealerId)
    if json_result:
        reviews = json_result
        print(reviews)
        for review in reviews:
            review_obj = DealerReview(
                dealership=review["dealership"],
                name=review["name"],
                purchase=review["purchase"],
                review=review["review"],
                purchase_date=review["purchase_date"],
                car_make=review["car_make"],
                car_model=review["car_model"],
                car_year=review["car_year"],
                sentiment=analyze_review_sentiments(review),
                id=review["id"]
            )
            results.append(review_obj)
    return results

    
# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text

def post_request(url, json_payload, **kwargs):
    '''
     Create a `post_request` to make HTTP POST requests
    '''
    print(kwargs)
    print("POST to {} ".format(url))
    print(json_payload)
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
    except:
        print("Something went wrong")
        return response.status_code
    return response
        
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(dealerreview):
    # get the returned sentiment label such as Positive or Negative return the label
    # get the returned sentiment label such as Positive or Negative
    # return the label
    # authenticator = IAMAuthenticator('A9mE5XKyAsN86hRjokieEUWJY5lvM9se2dOUO53qtrGu')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-03-25',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/418516ec-f40e-4170-9d1e-753554e86dc9')
    response = natural_language_understanding.analyze(
        text=dealerreview.review,
        features=Features(sentiment=SentimentOptions())).get_result()
    print(json.dumps(response, indent=2))
    sentiment = response["sentiment"]["document"]["label"]
    return sentiment
