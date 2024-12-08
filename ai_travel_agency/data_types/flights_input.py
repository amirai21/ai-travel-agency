from typing import Optional
from langchain.pydantic_v1 import BaseModel, Field
from enum import Enum

class FlightType(Enum):
    RoundTrip = 1
    OneWay = 2
    MultiCity = 3

class FlightsInput(BaseModel):
    departure_airport: str = Field(description='Departure airport code (IATA)')
    arrival_airport: str = Field(description='Arrival airport code (IATA)')
    type: FlightType = Field(description='Flight type. Options: RoundTrip (1), OneWay (2), MultiCity (3)')
    outbound_date: str = Field(description='Parameter defines the outbound date. The format is YYYY-MM-DD. e.g. 2024-06-22')
    return_date: Optional[str] = Field(description='Parameter defines the return date. The format is YYYY-MM-DD. e.g. 2024-06-28')
    adults: Optional[int] = Field(1, description='Parameter defines the number of adults. Default to 1.')
    children: Optional[int] = Field(0, description='Parameter defines the number of children. Default to 0.')
    infants_in_seat: Optional[int] = Field(0, description='Parameter defines the number of infants in seat. Default to 0.')
    infants_on_lap: Optional[int] = Field(0, description='Parameter defines the number of infants on lap. Default to 0.')


class FlightsInputSchema(BaseModel):
    params: FlightsInput