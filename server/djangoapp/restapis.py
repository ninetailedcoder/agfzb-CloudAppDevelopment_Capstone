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
    api_key = "5JjvPHXLotX_DKM6rvgtoIC4eHy0_k-3f-pJKX_0KiRu"
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
    # Update the URL to include the 'id' parameter
    params = {'id': dealerId}
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        json_result = response.json()
        if json_result:
            reviews = json_result
            print(reviews)
            for review in reviews:
                dealership= get_dealer_reviews_from_cf(url, dealerId)
                sentiment = analyze_review_sentiments(review['review'])  # Pass the review text to the sentiment analysis function
                review_obj = DealerReview(
                    dealership=dealership,
                    name=review["name"],
                    purchase=review["purchase"],
                    review=review["review"],
                    purchase_date=review["purchase_date"],
                    car_make=review["car_make"],
                    car_model=review["car_model"],
                    car_year=review["car_year"],
                    sentiment=sentiment,
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
import json
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def analyze_review_sentiments(review_text):
    # Create an authenticator using your API key
    authenticator = IAMAuthenticator('A9mE5XKyAsN86hRjokieEUWJY5lvM9se2dOUO53qtrGu')

    # Create a Natural Language Understanding instance
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-03-25',
        authenticator=authenticator
    )

    # Set the service URL for your specific NLU instance
    natural_language_understanding.set_service_url('https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/418516ec-f40e-4170-9d1e-753554e86dc9')

    # Analyze the sentiment of the review text
    response = natural_language_understanding.analyze(
        text=review_text,
        features=Features(sentiment=SentimentOptions())
    ).get_result()

    # Extract the sentiment label
    sentiment = response["sentiment"]["document"]["label"]
    
    return sentiment

