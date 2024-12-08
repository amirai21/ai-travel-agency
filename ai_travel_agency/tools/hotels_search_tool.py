import os

import serpapi
from langchain_core.tools import tool

from ai_travel_agency.data_types.hotels_input import HotelsInputSchema, HotelsInput

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY')

@tool(args_schema=HotelsInputSchema)
def search_hotels(params: HotelsInput):
    """
    Find hotels using the Google Hotels engine.

    Returns:
        dict: Hotel search results.
    """

    print(params)

    params = {
        'api_key': SERPAPI_API_KEY,
        'engine': 'google_hotels',
        'hl': 'en',
        'gl': 'us',
        'q': params.q,
        'check_in_date': params.check_in_date,
        'check_out_date': params.check_out_date,
        'currency': 'ILS',
        'adults': params.adults,
        'children': params.children,
        'children_ages': params.children_ages,
        'rooms': params.rooms,
        'sort_by': params.sort_by,
        'hotel_class': params.hotel_class,
        'num': 30,
    }

    search = serpapi.search(params)
    results = search.data
    return results['properties']