# Extra Data Types
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Supported Extra Data Types ------------------!#
#> FastAPI supports many additional Python data types with the same great features:
#> • Great editor support
#> • Data conversion from incoming requests
#> • Data conversion for response data
#> • Data validation
#> • Automatic annotation and documentation

#!------------------ UUID ------------------!#
## Universally Unique Identifier, common as an ID in databases and systems.
#> In requests/responses: Represented as a str
#> Example: "550e8400-e29b-41d4-a716-446655440000"

#!------------------ datetime.datetime ------------------!#
## Python datetime.datetime objects.
#> In requests/responses: Represented as ISO 8601 format string
#> Example: "2008-09-15T15:53:00+05:00"

#!------------------  datetime.date ------------------!#
## datetime.date
### Python datetime.date objects.
#> In requests/responses: Represented as ISO 8601 date string
#> Example: "2008-09-15"

#!------------------ datetime.time ------------------!#
## Python datetime.time objects.
#> In requests/responses: Represented as ISO 8601 time string
#> Example: "14:23:55.003"

#!------------------ datetime.timedelta ------------------!#
## Python datetime.timedelta objects.
#> In requests/responses: Represented as float of total seconds
#> Example: 3600 (for 1 hour)
#> Alternative: ISO 8601 time diff encoding (see Pydantic docs)

#!------------------ frozenset ------------------!#
## Immutable set type.
#> In requests: List is read, duplicates eliminated, converted to set
#> In responses: Set is converted to list
#> Schema: Specifies unique items using JSON Schema's uniqueItems

#!------------------ bytes ------------------!#
## Standard Python bytes.
#> In requests/responses: Treated as str
#> Schema: Specified as str with binary format

#!------------------ Decimal ------------------!#
## Standard Python Decimal for precise decimal arithmetic.
#> In requests/responses: Handled the same as float
#> Use case: Financial calculations requiring precision

#!------------------ Complete Example ------------------!#
#> Following the official FastAPI tutorial with modern Annotated syntax:

from datetime import datetime, time, timedelta
from typing import Annotated, Union
from uuid import UUID
from fastapi import Body, FastAPI

app = FastAPI()

@app.put("/items/{item_id}")
async def read_items( 
                        item_id: UUID,
                        start_datetime: Annotated[datetime, Body()],
                        end_datetime: Annotated[datetime, Body()],
                        process_after: Annotated[timedelta, Body()],
                        repeat_at: Annotated[Union[time, None], Body()] = None,
                    ):
    # Perform normal date manipulations
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "process_after": process_after,
        "repeat_at": repeat_at,
        "start_process": start_process,
        "duration": duration,
    }

## Request Example
#> URL: PUT /items/550e8400-e29b-41d4-a716-446655440000
## Request Body:
'''
{
    "start_datetime": "2024-01-15T10:30:00",
    "end_datetime": "2024-01-15T15:30:00", 
    "process_after": 3600,
    "repeat_at": "14:30:00"
}
'''
## Response:
'''
{
    "item_id": "550e8400-e29b-41d4-a716-446655440000",
    "start_datetime": "2024-01-15T10:30:00",
    "end_datetime": "2024-01-15T15:30:00",
    "process_after": 3600.0,
    "repeat_at": "14:30:00",
    "start_process": "2024-01-15T11:30:00",
    "duration": 14400.0
}
'''

#!------------------ Automatic Conversions ------------------!#

## UUID Conversion
#> Path parameter: /items/550e8400-e29b-41d4-a716-446655440000
#> Automatically converted to UUID object
item_id: UUID  #> <UUID('550e8400-e29b-41d4-a716-446655440000')>

## DateTime Conversion
#> JSON: "2024-01-15T10:30:00"
#> Automatically converted to datetime object
start_datetime: datetime  #> datetime(2024, 1, 15, 10, 30)

## Timedelta Conversion
#> JSON: 3600 (seconds)
#> Automatically converted to timedelta object
process_after: timedelta  #> timedelta(seconds=3600)

## Time Conversion
#> JSON: "14:30:00"
#> Automatically converted to time object
repeat_at: time  #> time(14, 30)

