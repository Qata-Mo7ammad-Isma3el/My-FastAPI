# Security - First Steps
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#

#> Let's imagine that you have your backend API in some domain and you have a frontend in another domain or in a different
#> path of the same domain (or in a mobile application). You want to have a way for the frontend to authenticate with the
#> backend, using a username and password.

#> We can use OAuth2 to build that with FastAPI. Let's use the tools provided by FastAPI to handle security.

## OAuth2PasswordBearer
#> FastAPI provides OAuth2PasswordBearer to handle OAuth2 with Bearer tokens. When you create an instance:

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordBearer
from typing_extensions import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

#> • This parameter tokenUrl="token" refers to a relative URL token that the client (frontend running in the user's browser) 
#>   will use to send the username and password in order to get a token.

## Using the Security Dependency
#> Now you can pass that oauth2_scheme in a dependency with Depends:

@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

#> This dependency will:
#> • Look for an Authorization header in the request
#> • Check if the value is Bearer plus a token
#> • Return the token as a str
#> • If no Authorization header is found, or the value doesn't have a Bearer token, it will respond with a 401 status 
#>   code error (UNAUTHORIZED) directly

## Automatic API Documentation
#> When you go to the interactive API docs at /docs, you'll see that your API now has an "Authorize" button. 
#> When you click it, you can type a token, and all requests will include that token in the Authorization header.


#!------------------ Key Concepts ------------------!#
#> • Bearer Token: A token passed in the Authorization: Bearer <token> header
#> • OAuth2PasswordBearer: FastAPI class that handles Bearer token extraction
#> • tokenUrl: URL where clients send credentials to get tokens (declared but not implemented yet)
#> • Security Dependency: Use Depends(oauth2_scheme) to protect endpoints
#> • Automatic Documentation: FastAPI generates interactive docs with "Authorize" button

#!------------------ Best Practices ------------------!#
#> • Use relative URLs for tokenUrl to work with proxies
#> • Don't implement actual token validation yet - this is just the first step
#> • The oauth2_scheme is both a class instance and a callable dependency
#> • Protected endpoints automatically get security documentation


