# Security - Simple OAuth2
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> Now let's build from the previous chapter and add the missing parts to have a complete security flow.
#> Get the username and password
#> We are going to use FastAPI security utilities to get the username and password.
#> OAuth2 specifies that when using the "password flow" (that we are using) the client/user must send a username and password
#> fields as form data.
#> And the spec says that the fields have to be named like that. So user-name or email wouldn't work.
#> But don't worry, you can show it as you wish to your final users in the frontend. And your database models can use any 
#> other names you want. 
#> But for the login path operation, we need to use these names to be compatible with the spec 
#> (and be able to, for example, use the integrated API documentation system).
#> The spec also states that the username and password must be sent as form data (so, no JSON here).
#> Code to get the username and password
#> Now let's use the utilities provided by FastAPI to handle this:

from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    user = UserInDB(**user_dict)
    hashed_password = fake_hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user

#> The OAuth2PasswordRequestForm is a class dependency that declares a form body with:
#> • The username
#> • The password
#> • An optional scope field as a big string, composed of strings separated by spaces
#> • An optional grant_type

#!------------------ Key Concepts ------------------!#
#> • Form Data Authentication: OAuth2 password flow requires form data, not JSON
#> • Token Endpoint: Returns access tokens in standardized format
#> • Password Verification: Check hashed passwords (never store plaintext)
#> • User Status: Verify user is active before granting access
#> • Bearer Tokens: Use "Bearer" token type for authorization headers

#!------------------ Best Practices ------------------!#
#> • Always hash passwords, never store plaintext
#> • Return consistent error messages for security
#> • Include WWW-Authenticate header for 401 responses
#> • Validate user is active before granting access
#> • Use proper OAuth2 response format