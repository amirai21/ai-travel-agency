import os

import serpapi
from langchain_core.tools import tool

from ai_travel_agency.data_types.flights_input import FlightsInputSchema, FlightsInput

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

# https://serpapi.com/search.json?engine=google_flights&api_key=9f35208499449c305f71578d29e4d80a6ad744735f66bd36de2d8a9dd0efab5f&departure_id=PEK&arrival_id=AUS&outbound_date=2024-12-12&return_date=2024-12-14&currency=USD&hl=en

@tool(args_schema=FlightsInputSchema)
def search_flights(params: FlightsInput):
    '''
    Find flights using the Google Flights engine.

    Returns:
        dict: Flight search results.
    '''

    query = {
        'api_key': SERPAPI_API_KEY,
        'engine': 'google_flights',
        'hl': 'en',
        'gl': 'us',
        'departure_id': params.departure_airport,
        'arrival_id': params.arrival_airport,
        'type': params.type.value,
        'outbound_date': params.outbound_date,
        'return_date': params.return_date,
        'currency': 'USD',
        'adults': params.adults,
        'infants_in_seat': params.infants_in_seat,
        # 'stops': '1',
        'infants_on_lap': params.infants_on_lap,
        'children': params.children
    }

    print(query)

    try:
        search = serpapi.search(query)
        results = search.data.get('best_flights', [])
        if not results:
            return "No flights found."
    except Exception as e:
        results = str(e)
    return results