#Dependencies - First Steps
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> • FastAPI has a very powerful but intuitive Dependency Injection system. It is designed to be very simple to use, 
#>   and to make it very easy for any developer to integrate other components with FastAPI.

#? What is "Dependency Injection"
#> • "Dependency Injection" means that there is a way for your code (your path operation functions) to declare 
#>    things that it requires to work and use: "dependencies". FastAPI will take care of providing your code with 
#>    those needed dependencies ("inject" the dependencies).
#> This is very useful when you need to:
#> • Have shared logic (the same code logic again and again)
#> • Share database connections
#> • Enforce security, authentication, role requirements, etc.
#> • And many other things...
#! All these, while minimizing code repetition.

#!------------------ Key Concepts ------------------!#

## Creating a Dependency
#> A dependency is just a function that can take all the same parameters that a path operation function can take:

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}
#> It has the same shape and structure as your path operation functions, but without the decorator.

## Using Dependencies
#> You use Depends in your path operation parameters:
from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()
@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

## How it Works
#> When a request arrives, FastAPI will:

#> • Call your dependency function with the correct parameters
#> • Get the result from your function
#> • Assign that result to the parameter in your path operation function

## Sharing Dependencies
#> You can use the same dependency in multiple path operations:

@app.get("/items/")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons

@app.get("/users/")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
#> This way you write shared code only once, and FastAPI takes care of calling it for your path operations.

#!------------------ Best Practices ------------------!#
#> • Keep dependencies simple: Focus on single responsibilities
#> • Use type annotations: They help with editor support and validation
#> • Share common dependencies: Reuse the same dependency across multiple endpoints
#> • Async compatibility: You can mix async def and def dependencies freely




