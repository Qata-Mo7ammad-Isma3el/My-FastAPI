# Path Operation Configuration
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> Important: Notice that these parameters are passed directly to the path operation decorator, not to your path
#> operation function. 
#> There are several parameters that you can pass to your path operation decorator to configure it. 

## Response Status Code
#> You can define the (HTTP) status_code to be used in the response of your path operation.
#> You can pass directly the int code, like 404.
#> But if you don't remember what each number code is for, you can use the shortcut constants in status:
from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: set[str] = set()

@app.post("/items1/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    return item

#> That status code will be used in the response and will be added to the OpenAPI schema.

## Tags
#> You can add tags to your path operation, pass the parameter tags with a list of str (commonly just one str):
@app.get("/items2/", tags=["items"])
async def read_items():
    return [{"name": "Foo", "price": 42}]

@app.get("/users/", tags=["users"])
async def read_users():
    return [{"username": "johndoe"}]
#> They will be added to the OpenAPI schema and used by the automatic documentation interfaces.


## Tags with Enums
#> If you have a big application, you might end up accumulating several tags, and you would want to make sure you always use the same tag for related path operations.
#> In these cases, it could make sense to store the tags in an Enum.
#> FastAPI supports that the same way as with plain strings:

from enum import Enum

class Tags(Enum):
    items = "items"
    users = "users"

@app.get("/elements1/", tags=[Tags.items])
async def read_elements():
    return ["Portal gun", "Plumbus"]

## Summary and description
#> You can add a summary and description:

@app.post( "/items3/",
            response_model=Item,
            summary="Create an item",
            description="Create an item with all the information, name, description, price, tax and a set of unique tags", )
async def create_item(item: Item):
    return item

## Description from docstring
#> • As descriptions tend to be long and cover multiple lines, you can declare the path operation description 
#>   in the function docstring and FastAPI will read it from there.
#> • You can write Markdown in the docstring, it will be interpreted and displayed correctly 
#>   (taking into account docstring indentation).

@app.post("/items4/", response_model=Item, summary="Create an item")
async def create_item(item: Item):
    """ 
    Create an item with all the information: 
    - **name**: each item must have a name 
    - **description**: a long description 
    - **price**: required 
    - **tax**: if the item doesn't have tax, you can omit this 
    - **tags**: a set of unique tag strings for this item 
    """
    return item

## Deprecate a path operation
#> If you need to mark a path operation as deprecated, but without removing it, pass the parameter deprecated:
@app.get("/elements2/", tags=["items"], deprecated=True)
async def read_elements():
    return [{"item_id": "Foo"}]
#! It will be clearly marked as deprecated in the interactive docs.

#!------------------ Key Concepts ------------------!#
#> • Status Constants: Use status.HTTP_201_CREATED instead of 201
#> • Tags: Organize endpoints into logical groups
#> • Docstrings: Multi-line descriptions with Markdown support
#> • Deprecation: Mark endpoints as obsolete without removing them

## Recap
#> You can configure and add metadata for your path operations easily by passing parameters to the path operation decorators.

#!------------------ Best Practices ------------------!#
#> • Always use status constants for better code readability
#> • Group related endpoints with consistent tags
#> • Use docstrings for complex endpoint descriptions
#> • Mark deprecated endpoints instead of immediately removing them
#> • Keep response descriptions specific and helpful


