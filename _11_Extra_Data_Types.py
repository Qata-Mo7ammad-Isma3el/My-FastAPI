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

#!------------------ Modern Annotated Syntax ------------------!#
#> The official FastAPI documentation now recommends using Annotated for better type hints and IDE support:

from typing import Annotated, Union

# Modern approach (recommended)
start_datetime: Annotated[Union[datetime, None], Body()]

# Older approach (still works)
start_datetime: datetime | None = Body()

## Annotated
'''
#> The Annotated type hint, introduced in Python 3.9, allows you to attach additional metadata to a type hint.
#> This metadata doesn't influence the type checking directly but can be used for various other purposes, such 
#> as validation, documentation, or other custom behaviors.
'''
#> At its core, Annotated takes a type and any number of metadata element:

from typing import Annotated
Age = Annotated[int, "value should be between 0 and 120"]
#> In the above example, Age is essentially an int, but it carries additional information that the value 
#> should be between 0 and 120.

### Validation
#> You can use the metadata in Annotated to perform runtime validation of values:

def validate_age(value: Age) -> None:
    _, metadata = Age.__metadata__
    if not (0 <= value <= 120):
        raise ValueError(f"Invalid age. {metadata}")

### Documentation
#> Metadata can be used to provide additional documentation for developers:

Coordinate = Annotated[tuple, "A tuple representing (x, y) coordinates on a 2D plane"]

### Serialization and Deserialization
#> When working with data serialization, Annotated can provide hints on how to process the data:

DateStr = Annotated[str, {"format": "YYYY-MM-DD"}]


def serialize_date(date: datetime.date) -> DateStr:
    format_str = DateStr.__metadata__[1]["format"]
    return date.strftime(format_str)

### Framework-specific Behaviors
#> Some frameworks might use the metadata in Annotated to influence behavior. For instance,
#> a web framework might use it to parse query parameters or request bodies:

QueryParam = Annotated[str, {"required": True}]

### Multiple Metadata
#> Annotated can also hold multiple metadata elements:

Price = Annotated[float, "The price of an item in USD", {"min_value": 0.0}]

## Benefits of Annotated:
#> • Better IDE Support: More precise type information
#> • Cleaner Separation: Type and metadata are clearly separated
#> • Future-Proof: Aligns with Python's type annotation evolution
#> • Explicit: Makes the relationship between type and validation clear

#!------------------ Key Benefits ------------------!#
## Type Safety
#> • Full IDE support with autocomplete
#> • Type checking catches errors at development time
#> • Clear function signatures show expected types

## Automatic Validation
#> • Invalid UUIDs return HTTP 422 with clear error messages
#> • Invalid datetime formats are automatically rejected
#> • Type conversion happens transparently

## Documentation Generation
#> • OpenAPI schema includes proper type information
#> • Interactive docs show expected formats
#> • Examples are automatically generated
## Natural Python Operations
#> You can perform normal Python operations
#> datetime + timedelta
#code: start_process = start_datetime + process_after  
#> datetime - datetime
#code: duration = end_datetime - start_process         
#code: is_same_day = start_datetime.date() == end_datetime.date()

#!------------------ Best Practices ------------------!#
## UUID Usage
from uuid import UUID, uuid4
from pydantic import BaseModel
from fastapi import HTTPException
#> Path parameter
@app.get("/users/{user_id}")
async def get_user(user_id: UUID):
    #> user_id is automatically validated as UUID
    return {"user_id": user_id}

#> Generate new UUIDs
new_id = uuid4()  #> Generate random UUID


## DateTime Handling
from datetime import datetime, timezone
#> Always use timezone-aware datetimes for APIs
@app.post("/events/")
async def create_event( start_time: datetime, end_time: datetime ):
    # Validate time range
    if end_time <= start_time:
        raise HTTPException(400, "End time must be after start time")
    
    return {"duration": end_time - start_time}


## Decimal for Financial Data
from decimal import Decimal

class Product(BaseModel):
    name: str
    price: Decimal  #> Use Decimal for money to avoid floating-point errors
    tax_rate: Decimal = Decimal('0.08')  #> 8% tax
    
    def total_price(self) -> Decimal:
        return self.price * (1 + self.tax_rate)

## Bytes for Binary Data
@app.post("/upload/")
async def upload_file( file_content: bytes = Body(), filename: str = Body() ):
    #> file_content is automatically decoded from base64 string
    return {"size": len(file_content), "filename": filename}

#!------------------ Validation Examples ------------------!#
## Valid Requests
'''
### UUID:
#> "550e8400-e29b-41d4-a716-446655440000"  ✅

### DateTime:
#> "2024-01-15T10:30:00"     ✅ ISO format
#> "2024-01-15T10:30:00Z"    ✅ UTC timezone
#> "2024-01-15T10:30:00+05:00"  ✅ With timezone

### Timedelta:
#> 3600        ✅ Seconds as number
#> "01:00:00"  ✅ ISO duration format (if supported)
'''

## Invalid Requests
'''
### Invalid UUID:
#> "not-a-uuid"  ❌ HTTP 422: "value is not a valid uuid"

### Invalid DateTime:
#> "2024-13-45"  ❌ HTTP 422: "invalid datetime format"
#> "not-a-date"  ❌ HTTP 422: "value is not a valid datetime"

### Invalid Time:
#> "25:30:00"    ❌ HTTP 422: "hour must be in 0..23"
'''
#!------------------ Advanced Usage ------------------!#
## Combining Types in Models
from datetime import datetime
from uuid import UUID
from decimal import Decimal
from typing import List, Dict, Union
from pydantic import BaseModel

class Order(BaseModel):
    id: UUID
    created_at: datetime
    amount: Decimal
    items: List[str]
    metadata: Dict[str, Union[str, int]]

## Custom Validation
from pydantic import field_validator
class Event(BaseModel):
    id: UUID
    start_time: datetime
    end_time: datetime

#// the validator function has been replaced with field_validator
@field_validator('end_time')
def end_after_start(cls, v, values):
    if 'start_time' in values and v <= values['start_time']:
        raise ValueError('end_time must be after start_time')
    return v

#! Note: go back for these lessons in the official FastAPI documentation for more details
#> • Cookie Parameters
#> • Header Parameters
#> • Cookie Parameter Models
#> • Header Parameter Models
