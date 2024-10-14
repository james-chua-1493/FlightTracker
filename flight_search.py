import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

TOKEN_ENDPOINT = "https://test.api.amadeus.com/v1/security/oauth2/token"
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v2/shopping/flight-offers"

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self._api_key = os.environ["AMADEUS_API_KEY"]
        self._api_secret = os.environ["AMADEUS_SECRET"]
        self._token = self.get_new_token()

    def get_new_token(self):

        header = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        body = {
            'grant_type': 'client_credentials',
            'client_id': self._api_key,
            'client_secret': self._api_secret
        }

        response = requests.post(url=TOKEN_ENDPOINT, headers=header, data=body)

        print(f"Your token is {response.json()['access_token']}")
        print(f"Your token expires in {response.json()['expires_in']} seconds")
        return response.json()['access_token']

    def get_destination_code(self, city_name):
        header = {"Authorization": f"Bearer {self._token}"}
        query = {
            "keyword": city_name,
            "max": "2",
            "include": "AIRPORTS",
        }
        response = requests.get(url=IATA_ENDPOINT,params=query, headers=header )

        try:
            destination_code = response.json()["data"][0]["iataCode"]

        except IndexError:
            print(f"IndexError: No airport code found for {city_name}.")
            return "N/A"

        except KeyError:
            print(f"KeyError: No airport code found for {city_name}.")
            return "Not Found"

        return destination_code


    def check_flights(self, originCode, destinationCode, departureDate, returnDate):
        header = {"Authorization": f"Bearer {self._token}"}
        query = {
            "originLocationCode": originCode,
            "destinationLocationCode": destinationCode,
            "departureDate": departureDate.strftime("%Y-%m-%d"),
            "returnDate": returnDate.strftime("%Y-%m-%d"),
            "adults": 1,
            "nonStop": "true",
            "currencyCode": "GBP",
            "max": "10",
        }
        response = requests.get(url=FLIGHT_ENDPOINT, params=query, headers=header)
        if response.status_code != 200:
            print("N/A")

        return response.json()





