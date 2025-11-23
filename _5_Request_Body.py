#
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ What are Request Bodies?  ------------------!#

'''
#? What are Request Bodies?
#> A request body is data sent by the client to your API. Unlike query parameters that go in the URL, 
#> request bodies can contain large amounts of structured data like JSON objects.

#? When to Use Request Bodies?
#> • Creating data: POST requests to create new items
#> • Updating data: PUT/PATCH requests to modify existing items
#> • Complex data: When you need to send more than simple parameters
#> • Sensitive data: Data that shouldn't appear in URLs
## Real-World Examples
#> • User registration: Sending user details (name, email, password)
#> • Creating posts: Sending blog post content and metadata
#> • File uploads: Sending file data and descriptions
#> • API calls: Sending complex query parameters to search APIs
## Pydantic Models
#> FastAPI uses Pydantic models to define the structure of request bodies. This provides automatic validation, 
#> serialization, and documentation.
'''
## Basic Model Definition
### From the official tutorial:
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

### Key features:
#> Type hints: Define the expected data types
#> • Optional fields: Use | None = None for optional fields
#> • Automatic validation: FastAPI validates the data automatically
#> • JSON conversion: Automatically converts to/from JSON

### Using the Model
from fastapi import FastAPI

app = FastAPI()
@app.post("/items/")
def create_item(item: Item):
    return item

### What happens:
#> 1. Client sends JSON data
#> 2. FastAPI validates it against the Item model
#> 3. Creates an Item instance
#> 4. Passes it to your function
#> 5. Automatically converts the response back to JSON


#!------------------ Official Tutorial Examples ------------------!#

## Example 1: Basic Request Body

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

@app.post("/items/")
def create_item(item: Item):
    return item
'''
#> Test with JSON:
#> {
#>     "name": "Foo",
#>     "description": "A very nice Item",
#>     "price": 10.5,
#>     "tax": 1.5
#> }
'''
## Example 2: Request Body + Path Parameters
@app.post("/items/{item_id}")
def create_item_with_id(item_id: int, item: Item):
    return {"item_id": item_id, **item.model_dump()}

#// dict()
#> use should use model.dump() to convert model to dictionary instead of dict() method 
#> URL: POST /items/123 Body: Same JSON as above Response: Includes both the item_id and all item fields

## Example 3: Request Body + Path + Query Parameters
@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item, q: str | None = None):
    result = {"item_id": item_id, **item.model_dump()}
    if q:
        result.update({"q": q})
    return result
#> URL: PUT /items/123?q=search Body: Item JSON Response: Combines all three parameter types

#!------------------ Advanced Pydantic Features ------------------!#

## Field Validation
from pydantic import BaseModel, Field

class Item(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)
    price: float = Field(..., gt=0)  # Greater than 0
    tax: float | None = Field(None, ge=0)  # Greater than or equal to 0

## Nested Models
class Image(BaseModel):
    url: str
    name: str

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    images: list[Image] | None = None

## Model Configuration
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }

#!------------------ Best Practices ------------------!#
## 1. Use Descriptive Model Names
#> ✅ Good - clear purpose
class UserRegistration(BaseModel):
    username: str
    email: str
    password: str

#> ❌ Avoid - generic names
class Data(BaseModel):
    field1: str
    field2: str

## 2. Add Field Descriptions
#> ✅ Good - documented fields
class Item(BaseModel):
    name: str = Field(..., description="The name of the item")
    price: float = Field(..., gt=0, description="The price must be greater than zero")

## 3. Use Appropriate Defaults
#> ✅ Good - sensible defaults
class Item(BaseModel):
    name: str
    description: str | None = None  # Optional description
    price: float
    tax: float | None = None        # Optional tax
    active: bool = True             # Default to active

#!------------------ Common Beginner Mistakes ------------------!#
## Mistake 1: Forgetting to Import BaseModel
#> ❌ Wrong - missing import
class Item:  # Should inherit from BaseModel
    name: str
    price: float

## Mistake 2: Wrong Optional Syntax
#> ❌ Wrong - old syntax
from typing import Optional

class Item(BaseModel):
    description: Optional[str] = None

#> ✅ Correct - modern syntax
class Item(BaseModel):
    description: str | None = None

## Mistake 3: Not Using the Model Parameter
#> ❌ Wrong - expecting raw dict
@app.post("/items/")
def create_item(data: dict):  # Should use Pydantic model
    return data

#> ✅ Correct - using Pydantic model
@app.post("/items/")
def create_item(item: Item):
    return item

## Mistake 4: Wrong HTTP Method
#> ❌ Wrong - using GET for data creation
@app.get("/items/") # Should be POST
def create_item(item: Item):
    return item

#> ✅ Correct - using POST for creation
@app.post("/items/")
def create_item(item: Item):
    return item

#!------------------ How FastAPI Handles Request Bodies ------------------!#
#? How FastAPI Handles Request Bodies?
'''
## Automatic Validation

#> FastAPI automatically:
#> • Reads the request body as JSON
#> • Validates the data against your Pydantic model
#> • Converts to the appropriate types
#> • Creates an instance of your model
#> • Passes it to your function
#> Error Handling
#> If validation fails, FastAPI automatically returns a detailed error response:
{
    "detail": [
        {
            "loc": ["body", "price"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}

## Interactive Documentation
#> FastAPI automatically generates interactive docs that show:
#> • The expected request body structure
#> • Field types and requirements
#> • Example values
#> • Try-it-out functionality
'''
