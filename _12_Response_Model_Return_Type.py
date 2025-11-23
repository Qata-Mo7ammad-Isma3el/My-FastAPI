# Response Model - Return Type
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#

'''
#> You can declare the type used for the response by annotating the path operation function return type. 
#> You can use type annotations the same way you would for input data in function parameters, you can use 
#> Pydantic models, lists, dictionaries, scalar values like integers, booleans, etc.
'''

## FastAPI will use this return type to:
#> • Validate the returned data. If the data is invalid (e.g. you are missing a field), it means that your app code is 
#>   broken, not returning what it should, and it will return a server error instead of returning incorrect data.
#> • Add a JSON Schema for the response, in the OpenAPI path operation. This will be used by the automatic docs and by 
#>   automatic client code generation tools.
#> • Limit and filter the output data to what is defined in the return type. This is particularly important for security.

#!------------------ Key Concepts ------------------!#
## Return Type Annotations
#> The simplest way to declare a response model is using return type annotations:

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item

@app.get("/items/")
async def read_items() -> list[Item]:
    return [
        {"name": "Portal Gun", "price": 42.0},
        {"name": "Plumbus", "price": 32.0},
    ]
## response_model Parameter
#> In some cases, you need to use the response_model parameter instead of return type annotations:

@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item
#> This is useful when you want to return a dictionary or database object but declare it as a Pydantic model
#> for documentation and validation.

## Data Filtering and Security
#> FastAPI automatically filters the response data to match your declared model. This means if your function returns
#> more data than declared in the response model, the extra data will be filtered out. This is crucial for security - you 
#> won't accidentally expose sensitive data.


#!------------------ Example from the official documentation ------------------!#
#! Note: response_model  have Priority over Return Type Annotations:
#> If you declare both a return type and a response_model, the response_model will take priority and be used by FastAPI.

## Return the same input data
#> Here we are declaring a UserIn model, it will contain a plaintext password:
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

#!!!!!!!!!!! Don't do this in production!
@app.post("/user/")
async def create_user(user: UserIn) -> UserIn:
    return user
#> In this example, the create_user endpoint returns the same UserIn model that includes the password.
#> This is not secure, as it exposes the user's password in the response.
#> To fix this, we can define a separate UserOut model that excludes the password field:

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None

class UserOut(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

@app.post("/user/",
            response_model=UserOut ,
            response_model_include={"username", "email", "full_name"},
            response_model_exclude={"password"}
        )
async def create_user(user: UserIn) -> Any:
    return user
#> Now, the create_user endpoint uses the response_model parameter to specify that it returns a UserOut model.
#> This way, the password field is excluded from the response, enhancing security.

#!------------------ Best Practices ------------------!#
#> • Always use return type annotations when possible for better editor support and type checking
#> • Use the response_model parameter when returning dictionaries or database objects
#> • Create separate input and output models to avoid exposing sensitive data like passwords
#> • Use list[Model] for endpoints that return arrays of objects
#> • FastAPI will automatically generate comprehensive API documentation based on your response models

