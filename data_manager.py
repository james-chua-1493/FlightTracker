import os
import requests
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth

load_dotenv()

SHEETY_USERNAME="jameschua"
SHEETY_PASSWORD="invalid7"
SHEETY_ENDPOINT = "https://api.sheety.co/dfea04fba7fa8b5dc6ea4e143aa9e1c1/flightDeals/sheet1"

class DataManager:
    #This class is responsible for talking to the Google Sheet.

    def __init__(self):
        self._username = os.environ["SHEETY_USERNAME"]
        self._password = os.environ["SHEETY_PASSWORD"]
        self.authorization = HTTPBasicAuth(self._username, self._password)
        self.destination_data = {}

    def get_destination_data(self):
        response = requests.get(url=SHEETY_ENDPOINT, auth=self.authorization)
        data = response.json()
        self.destination_data = data['sheet1']

        return self.destination_data

    def update_destination_codes(self):
        for city in self.destination_data:
            new_data = {
                "price": {
                    "iataCode": city["iataCode"]
                }
            }
            response = requests.put(
                url=f"{SHEETY_ENDPOINT}/{city['id']}",
                auth=self.authorization,
                json=new_data
            )
            # print(response.text)


