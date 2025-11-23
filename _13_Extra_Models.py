# Extra Models
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#

#> It will be common to have more than one related model. This is especially the case for user models, because:
#> • The input model needs to be able to have a password.
#> • The output model should not have a password.
#> • The database model would probably need to have a hashed password.
#!!! Never store user's plaintext passwords. Always store a "secure hash" that you can then verify.

#!------------------ Key Concepts ------------------!#
## Multiple Models for Different Use Cases
#> Here's how the models could look like with their password fields and the places where they are used:
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

class UserInDB(BaseModel):
    username: str
    hashed_password: str
    email: EmailStr
    full_name: str | None = None

## Model Unpacking and Data Conversion
#> You can create a Pydantic model from the contents of another using the model_dump() method and unpacking:

def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password

def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    #>>>>>>>>>>>>>>>>>>>> ** Python's "Unpacking" operator. <<<<<<<<<<<<<<<<<<<<
    user_in_db = UserInDB(**user_in.model_dump(), hashed_password=hashed_password)
    return user_in_db

@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved

## Reducing Code Duplication with Inheritance
#> You can declare a UserBase model that serves as a base for other models. Then make subclasses that inherit its attributes:

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None

class UserIn(UserBase):
    password: str

class UserOut(UserBase):
    pass

class UserInDB(UserBase):
    hashed_password: str

## Union Types for Flexible Responses
#> You can declare a response to be the Union of two or more types:

from typing import Union

class BaseItem(BaseModel):
    description: str
    type: str


class CarItem(BaseItem):
    type: str = "car"


class PlaneItem(BaseItem):
    type: str = "plane"
    size: int

@app.get("/items/{item_id}")
async def read_item(item_id: str) -> Union[PlaneItem, CarItem]:
    #> Return either a PlaneItem or CarItem based on logic
    pass
