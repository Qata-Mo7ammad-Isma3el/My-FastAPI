# Body - Fields
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code code blocks
#// discarded lines

#// example
#! important note example parameter in any function has been described as and replaced with examples  


#!------------------ Import Field  ------------------!#
#> First, you need to import Field from pydantic:
from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field
#> Important: Notice that Field is imported directly from pydantic, not from fastapi like Query, Path, and Body.

#!------------------ Declare Model Attributes with Field ------------------!#
#> You can use Field with model attributes to add validation and metadata:
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None
## Field Parameters
#> Field works the same way as Query, Path, and Body - it accepts the same validation parameters:
#> • Validation constraints: gt, ge, lt, le, min_length, max_length, etc.
#> • Metadata: title, description, examples, etc.
#> • Default values: default, default_factory

#!------------------ Complete Examples ------------------!#
## Following the official FastAPI tutorial:

from typing import Union
from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

#> Request Body Structure
#> With Body(embed=True), the request expects:

'''
{
    "item": {
        "name": "Laptop",
        "description": "High-performance gaming laptop",
        "price": 999.99,
        "tax": 99.99
    }
}
'''

#!------------------ Key Concepts ------------------!#
#? Field vs Function Parameters
#> Notice the similarity between model attributes with Field and function parameters:
## Model attribute with Field:
#code: price: float = Field(gt=0, description="The price must be greater than zero")

## Function parameter with Path:
#code: item_id: int = Path(gt=0, description="The ID of the item")
#> Both follow the same pattern: 
#code: parameter: type = ValidationFunction(constraints)

## Validation Benefits
### Field validation provides:
#> • Automatic validation: Invalid data returns HTTP 422 with detailed error messages
#> • Type conversion: Automatic conversion between compatible types
#> • Documentation: Metadata appears in OpenAPI schema and interactive docs
#> • IDE support: Better autocomplete and type checking 

## Technical Details
#> • Query, Path, Body create objects of subclasses of Param class
#> • Param is a subclass of Pydantic's FieldInfo class
#> • Field returns an instance of FieldInfo directly
#> • All use the same underlying validation system

#!------------------ Best Practices ------------------!#
## Validation Constraints
class Item(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: float = Field(gt=0, le=1000000)  # Positive, reasonable max
    quantity: int = Field(ge=1, le=1000)    # At least 1, reasonable max
    email: str = Field(regex=r'^[\w\.-]+@[\w\.-]+\.\w+$')


## Descriptive Metadata
class User(BaseModel):
    username: str = Field(
        title="Username",
        description="Unique identifier for the user",
        min_length=3,
        max_length=50,
        examples="johndoe"
    )
    age: int = Field(
        title="Age", 
        description="Age in years",
        ge=0,
        le=150,
        examples=25
    )


## Optional Fields with Defaults
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field(
        default=None,
        title="Item Description", 
        max_length=500
    )
    is_active: bool = Field(default=True, description="Whether item is active")

#!------------------ Add Extra Information ------------------!#
#> You can include additional metadata in Field that will appear in the generated JSON Schema:

class Item(BaseModel):
    name: str = Field(
        title="Item Name",
        description="The name of the item",
        examples="Laptop"
    )
    price: float = Field(
        gt=0,
        description="Price in USD",
        examples=999.99
    )
#! Warning: Extra keys passed to Field will be present in the OpenAPI schema. Some OpenAPI tools may not work with non-standard keys.
#!------------------ Validation Examples ------------------!#
'''
## Valid Request
{
    "item": {
        "name": "Gaming Laptop",
        "description": "High-performance laptop for gaming",
        "price": 1299.99
    }
}
#> ✅ Result: Success - all validations pass

## Invalid Requests
### Negative price:
{
    "item": {
        "name": "Laptop",
        "price": -100
    }
}
#> ❌ Result: HTTP 422 - "ensure this value is greater than 0"
### Description too long:
{
    "item": {
        "name": "Laptop", 
        "description": "x".repeat(400),  // Over 300 characters
        "price": 999.99
    }
}
#> ❌ Result: HTTP 422 - "ensure this value has at most 300 characters"
'''

