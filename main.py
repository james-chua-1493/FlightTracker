import time
from data_manager import DataManager
from flight_search import FlightSearch
from pprint import pprint
from flight_data import find_cheapest_flight
from datetime import datetime, timedelta
from notification_manager import NotificationManager

data_manager = DataManager()
flight_search = FlightSearch()
notification_manager = NotificationManager()

ORIGIN_CITY_CODE = "LON"

sheet_data = data_manager.get_destination_data()
pprint(sheet_data)

for row in sheet_data:
    if row['iataCode'] == "":
        row['iataCode'] = flight_search.get_destination_code(row['city'])
        time.sleep(2)
pprint(sheet_data)

data_manager.destination_data = sheet_data
data_manager.update_destination_codes()

tomorrow = datetime.now() + timedelta(days=1)
date_after_6_months = datetime.now() + timedelta(days=(6*30))

for destination in sheet_data:
    print(f"Getting flights for {destination['city']}...")
    flights = flight_search.check_flights(
        ORIGIN_CITY_CODE,
        destination["iataCode"],
        departureDate=tomorrow,
        returnDate=date_after_6_months
    )
    cheapest_flight = find_cheapest_flight(flights)
    if cheapest_flight.price != "N/A" and cheapest_flight.price < destination["lowestPrice"]:
        notification_manager.send_sms(
            message_body=f"Low price alert! Only £{cheapest_flight.price} to fly "
                         f"from {cheapest_flight.departure_airport_code} to {cheapest_flight.arrival_airport_code}, "
                         f"on {cheapest_flight.departure_date} until {cheapest_flight.arrival_date},"
                         f"at {cheapest_flight.departure_time} until {cheapest_flight.arrival_time}."
        )

    time.sleep(2)





