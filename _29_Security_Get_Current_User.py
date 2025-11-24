# Security - Get Current User
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> In the previous chapter the security system (which is based on the dependency injection system) was giving the path operation function
#> a token as a str. But that is still not that useful.

#> Let's make it give us the current user.

## Create a User Model
#> First, let's create a Pydantic user model. The same way we use Pydantic to declare bodies, we can use it anywhere else:
from typing import Union
from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing_extensions import Annotated

app = FastAPI()

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None


## Get the User
#> • get_current_user will use a (fake) utility function we created, that takes a token as a str and returns our
#>   Pydantic User model:


def fake_decode_token(token: str) -> User:
    return User(
        username=token + "fakedecoded", email="john@example.com", full_name="John Doe"
    )

## Create a get_current_user Dependency
#> Let's create a dependency get_current_user. 
#! Remember that dependencies can have sub-dependencies
#> • get_current_user will have a dependency with the same oauth2_scheme we created before. 
#> • The same as we were doing before in the path operation directly, our new dependency get_current_user will
#> • receive a token as a str from the sub-dependency oauth2_scheme:

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user

## Inject the Current User
#> So now we can use the same Depends with our get_current_user in the path operation:

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
#! Notice that we declare the type of current_user as the Pydantic model User. 
#! This will help us inside of the function with all the completion and type checks.

#!------------------ Key Concepts ------------------!#
#> • User Models: Pydantic models that represent user data in your application
#> • Dependency Chains: Dependencies that have sub-dependencies for complex workflows
#> • Current User Pattern: A common security pattern where endpoints receive the authenticated user
#> • Type Safety: Using proper type annotations helps with code completion and validation
#> • 

#!------------------ Best Practices ------------------!#
#> • Create separate user models for different contexts (UserInDB vs User response)
#> • Use meaningful function names like get_current_user
#> • Leverage FastAPI's dependency injection for security concerns
#> • Keep security logic separate from business logic
#> • Use type annotations for better development experience