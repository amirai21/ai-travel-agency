from typing import Optional, List

from pydantic import BaseModel, Field


class HotelSearchResult(BaseModel):
    name: str = Field(description='The name of the hotel')
    description: str = Field(description='The description of the hotel')
    price_per_night: str = Field(description='The price per night of the hotel')
    total_price: Optional[str] = Field(8, description='The total price of the hotel')
    overall_rating: Optional[str] = Field(1, description='The overall rating of the hotel')
    website_links: Optional[List[str]] = Field(0, description='Links to the hotel website')
    hotel_class: Optional[str] = Field(
        None, description='Parameter defines to include only certain hotel class in the results. for example- 2,3,4')


class HotelsSearchResults(BaseModel):
    hotels: List[HotelSearchResult] = Field(description='List of hotel search results')