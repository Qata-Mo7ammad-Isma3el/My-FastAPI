# Body - Multiple Parameters
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ 1. Mix Path, Query and Body Parameters ------------------!#
#> FastAPI allows you to freely mix different parameter types. You can make body parameters optional by 
#> setting default to None:

from typing import Union
from fastapi import FastAPI, Path
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.put("/items/{item_id}/basic")
async def update_item_basic( 
                            *, 
                            item_id: int = Path(title="The ID of the item to get", ge=0, le=1000),
                            q: Union[str, None] = None,
                            item: Union[Item, None] = None, ):
    results = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    return results
#> Request examples:
#> • PUT /items/42/basic (no query, no body)
#> • PUT /items/42/basic?q=search (with query, no body)
#> • PUT /items/42/basic with JSON body (no query, with body)
#! Note that instead od using Union you can use | for example Union[str, None] is equivalent to str | None. 

#!------------------ 2. Multiple Body Parameters ------------------!#
#> When you declare multiple Pydantic models as parameters, FastAPI expects a JSON body with keys for each model:
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results
#> Expected request body:
'''
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    }
}
'''
#> FastAPI automatically converts the request so item receives its content and user receives its content.

#!------------------ 3. Singular Values in Body ------------------!#
#> Use Body() to add singular values (not Pydantic models) to the request body:
from fastapi import Body

@app.put("/items/{item_id}/importance")
async def update_item_importance( item_id: int, item: Item, user: User, importance: int = Body() ):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results

#> Expected request body:
'''
{
    "item": {
        "name": "Foo",
        "description": "The pretender", 
        "price": 42.0,
        "tax": 3.2
    },
    "user": {
        "username": "dave",
        "full_name": "Dave Grohl"
    },
    "importance": 5
}
'''
#> Without Body(), FastAPI would treat importance as a query parameter.

#!------------------ 4. Multiple Body Parameters and Query ------------------!#
#> You can combine body parameters with query parameters. Singular values without Body() become query parameters:
@app.put("/items/{item_id}/full")
async def update_item_full( 
                            *,
                            item_id: int, #* that's a path parameter
                            item: Item, #* that's a body parameter by schema
                            user: User, #* that's a body parameter by schema
                            importance: int = Body(gt=0), #* that's a body parameter by singular value
                            q: str | None = None, #* that's a query parameter
                        ):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    if q:
        results.update({"q": q})
    return results

#> URL: PUT /items/42/full?q=search
#> Request body:
'''
{
    "item": {"name": "Foo", "price": 42.0},
    "user": {"username": "dave"},
    "importance": 5
}
'''

#!------------------ 5. Embed Single Body Parameter ------------------!#
#> For a single body parameter, FastAPI normally expects the model content directly. Use Body(embed=True)
#> to wrap it in a JSON object:
@app.put("/items/{item_id}/embed")
async def update_item_embed(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results

'''
## With embed=True, expects:
{
    "item": {
        "name": "Foo",
        "description": "The pretender",
        "price": 42.0,
        "tax": 3.2
    }
}
## Without embed=True, would expect:
{
    "name": "Foo",
    "description": "The pretender", 
    "price": 42.0,
    "tax": 3.2
}
'''

#!------------------ Key Concepts ------------------!#

## Parameter Detection Rules:
#> • Path parameters: Declared in URL path with {parameter_name}
#> • Query parameters: Singular values with defaults, not in path
#> • Body parameters: Pydantic models or values with Body()

## Request Body Structure:
#> • Single Pydantic model: Direct model content (unless embed=True)
#> • Multiple Pydantic models: JSON object with model names as keys
#> • Mixed with Body(): Singular values added as additional keys

## Validation Benefits:
#> • All parameters validated according to their types
#> • Pydantic models provide rich validation and serialization
#> • Body() supports validation constraints (e.g., gt=0)
#> • Automatic OpenAPI documentation generation

#!------------------ Best Practices ------------------!#
## Import Organization
from typing import Union
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel
## Parameter Order
@app.put("/items/{item_id}/example")
async def example( 
                    *, # Force keyword-only arguments
                    item_id: int, # Path parameter 
                    item: Item, # Body parameter (Pydantic model) 
                    user: User, # Body parameter (Pydantic model)
                    importance: int = Body(gt=0), # Body parameter (singular) 
                    q: Union[str, None] = None, # Query parameter
                    ):
    pass

## Model Design
#> • Use Union[Type, None] for optional fields
#> • Provide sensible defaults for optional parameters
#> • Add validation constraints where appropriate
#> • Use descriptive field names and model names
