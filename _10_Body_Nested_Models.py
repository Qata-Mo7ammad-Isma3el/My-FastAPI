# Body - Nested Models
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ 1. List Fields ------------------!#
#> You can define an attribute to be a Python list:

from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list = []  # Basic list without type specification

#> This makes tags a list, but doesn't specify the type of elements inside the list.

#!------------------ 2. List Fields with Type Parameters ------------------!#
#> Python has a specific way to declare lists with internal types using "type parameters":
from typing import List, Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: list[str] = []  # List of strings or use list 

## Request body example:

'''
{
    "name": "Laptop",
    "description": "Gaming laptop",
    "price": 999.99,
    "tags": ["electronics", "computers", "gaming"]
}
'''
#!------------------ 3. Set Fields ------------------!#
#> You can use Set types for collections of unique items:

from typing import Set, Union
from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()  # Set of unique strings
#> Benefits of Sets:
#> • Automatically removes duplicates
#> • Validates uniqueness
#> • More efficient for membership testing

## Request body example:
'''
{
    "name": "Laptop",
    "price": 999.99,
    "tags": ["electronics", "computers", "electronics"]
}
'''
#> Result: tags will be {"electronics", "computers"} (duplicate removed)

#!------------------ 4. Nested Models ------------------!#
#> You can define a Pydantic model as the type of an attribute:
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

class Image(BaseModel):
    url: HttpUrl  # Special Pydantic type for URLs
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None  # Nested model

## Request body example:
'''
{
    "name": "Laptop",
    "price": 999.99,
    "tags": ["electronics", "computers"],
    "image": {
        "url": "https://example.com/laptop.jpg",
        "name": "Laptop Image"
    }
}
'''
## Special Pydantic Types
#> • HttpUrl: Validates that the string is a valid HTTP URL
#> • EmailStr: Validates email addresses (requires email-validator)
#> • UUID: Validates UUID strings
#> • datetime: Handles datetime objects

#!------------------ 5. Lists of Nested Models ------------------!#
#> You can have lists containing nested models:
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: List[Image] = []  # List of nested models

## Request body example:
'''
{
    "name": "Gaming Setup",
    "price": 1999.99,
    "images": [
        {
            "url": "https://example.com/setup1.jpg",
            "name": "Main Setup"
        },
        {
            "url": "https://example.com/setup2.jpg", 
            "name": "Side View"
        }
    ]
}
'''

#!------------------ 6. Deeply Nested Models ------------------!#
#> You can create arbitrarily deep nesting:
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    images: List[Image] = []

class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: List[Item]  # Nested list of items with their own nested images

## Request body example:
'''
{
    "name": "Holiday Sale",
    "price": 2999.99,
    "items": [
        {
            "name": "Gaming Setup",
            "price": 1999.99,
            "images": [
                {
                    "url": "https://example.com/setup1.jpg",
                    "name": "Main Setup"
                }
            ]
        },
        {
            "name": "Office Setup",
            "price": 999.99,
            "images": [
                {
                    "url": "https://example.com/office1.jpg",
                    "name": "Office View"
                }
            ]
        }
    ]
}
'''
#!------------------ 7. Dict Fields ------------------!#
#> You can use Dict for key-value mappings:
from typing import Dict
from fastapi import FastAPI

app = FastAPI()

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights

## Request body example:
'''
{
    "1": 0.5,
    "2": 1.0,
    "3": 0.75
}
'''
### Response:

'''
{
    "1": 0.5,
    "2": 1.0,
    "3": 0.75
}
'''
#!------------------  Key Concepts ------------------!#

## Type Safety Benefits
### Nested models provide:

#> • Automatic validation at every level
#> • Type conversion for compatible types
#> • Clear error messages showing exactly which nested field failed
#> • IDE support with autocomplete for nested attributes
#> • Automatic documentation in OpenAPI schema

## Validation Flow
#> • Top-level validation: Main model fields are validated
#> • Nested validation: Each nested model validates its own fields
#> • Collection validation: Lists/Sets validate each element
#> • Type conversion: Automatic conversion where possible
#> • Error aggregation: All validation errors collected and returned

## Performance Considerations
#> • Validation overhead: Deeper nesting = more validation work
#> • Memory usage: Nested objects use more memory
#> • Serialization cost: Complex structures take longer to serialize/deserialize
#> • Network payload: Larger JSON payloads 

#!------------------  Best Practices ------------------!#

from pydantic import EmailStr
## Model Organization
# Organize from simple to complex
class Address(BaseModel):
    street: str
    city: str
    country: str

class User(BaseModel):
    name: str
    email: EmailStr
    address: Address  # Simple nesting

class Order(BaseModel):
    id: int
    user: User        # Nested user
    items: List[Item] # List of nested items
    total: float

## Validation Constraints
from pydantic import Field

class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    tags: Set[str] = Field(max_items=10)  # Limit set size
    images: List[Image] = Field(max_items=5)  # Limit list size

class Category(BaseModel):
    id: int
    name: str

# Optional vs Required Nesting
class Item(BaseModel):
    name: str
    # Optional nested model
    image: Union[Image, None] = None
    # Required nested model
    category: Category
    # Optional list (can be empty)
    tags: List[str] = []
#!------------------ Complete Example ------------------!#
from typing import Dict, List, Set, Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: Set[str] = set()
    image: Union[Image, None] = None

class ItemWithImages(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    images: List[Image] = []

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results

@app.put("/items/{item_id}/images")
async def update_item_with_images(item_id: int, item: ItemWithImages):
    results = {"item_id": item_id, "item": item}
    return results

@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return weights
