
FLIGHT_ENDPOINT = "https://test.api.amadeus.com/v1/shopping/flight-offers"

class FlightData:
    #This class is responsible for structuring the flight data.

    def __init__(self, price, departure_airport_code, arrival_airport_code, departure_date, arrival_date, departure_time, arrival_time):
        self.price = price
        self.departure_airport_code = departure_airport_code
        self.arrival_airport_code = arrival_airport_code
        self.departure_date = departure_date
        self.arrival_date = arrival_date
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        pass

def find_cheapest_flight(data):

    if data is None or not data['data']:
        print("No flight data found.")
        return FlightData("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")

    first_flight = data["data"][0]
    lowest_price = float(first_flight["price"]["grandTotal"])
    departure_airport_code = first_flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
    arrival_airport_code = first_flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
    departure_date = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
    arrival_date = first_flight["itineraries"][0]["segments"][0]["arrival"]["at"].split("T")[0]
    departure_time = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[1]
    arrival_time = first_flight["itineraries"][0]["segments"][0]["arrival"]["at"].split("T")[1]

    cheapest_flight = FlightData(lowest_price,departure_airport_code,arrival_airport_code,departure_date, arrival_date, departure_time,arrival_time)

    for flight in data['data']:
        price = float(flight["price"]["grandTotal"])
        if price < lowest_price:
            lowest_price = price
            departure_airport_code = flight["itineraries"][0]["segments"][0]["departure"]["iataCode"]
            arrival_airport_code = flight["itineraries"][0]["segments"][0]["arrival"]["iataCode"]
            departure_date = flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[0]
            arrival_date = flight["itineraries"][0]["segments"][0]["arrival"]["at"].split("T")[0]
            departure_time = first_flight["itineraries"][0]["segments"][0]["departure"]["at"].split("T")[1]
            arrival_time = first_flight["itineraries"][0]["segments"][0]["arrival"]["at"].split("T")[1]
            cheapest_flight = FlightData(lowest_price, departure_airport_code, arrival_airport_code, departure_date, arrival_date, departure_time,
                                         arrival_time)
    print(f"The cheapest flight to {arrival_airport_code} is priced at £{lowest_price}, which leaves at {departure_date}  on {departure_time} from {departure_airport_code},"
          f" and arrives at {arrival_date} on {arrival_time}.")
    return cheapest_flight