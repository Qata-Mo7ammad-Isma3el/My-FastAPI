# Response Status Code
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> The same way you can specify a response model, you can also declare the HTTP status code used for the response
#> with the parameter status_code in any of the path operations:

#> • @app.get()
#> • @app.post()
#> • @app.put()
#> • @app.delete()
#> • etc.
#> The status_code parameter receives a number with the HTTP status code.

## HTTP Status Code Ranges
#> In HTTP, you send a numeric status code of 3 digits as part of the response:
#> • 200 - 299 are for "Successful" responses. These are the ones you would use the most.
#> • 200 is the default status code, which means everything was "OK"
#> • 201 "Created" - commonly used after creating a new record in the database
#> • 204 "No Content" - used when there is no content to return to the client


## 400 - 499 are for "Client error" responses
#> • 400 "Bad Request" - for generic client errors
#> • 404 "Not Found" - when a resource doesn't exist
#> • 422 "Unprocessable Entity" - validation errors

## 500 - 599 are for server errors (rarely used directly)

#!------------------ Key Concepts ------------------!#
## Setting Status Codes
from fastapi import FastAPI

app = FastAPI()
@app.post("/items1/", status_code=201)
def create_item_1(name: str):
    return {"name": name}
#! Notice that status_code is a parameter of the "decorator" method (get, post, etc), not of your path operation function.

## Using FastAPI Status Constants
#> Instead of memorizing status codes, you can use convenience variables from fastapi.status:

from fastapi import FastAPI, status

app = FastAPI()

@app.get("/items/", status_code=status.HTTP_201_CREATED)
def create_item(name: str):
    return {"name": name}
#> This provides better code readability and IDE autocomplete support.


#!------------------ Best Practices ------------------!#
#> • Use 201 Created for successful resource creation
#> • Use 204 No Content when you don't need to return data
#> • Use 400 Bad Request for client input errors
#> • Use 404 Not Found when resources don't exist
#> • Use FastAPI status constants instead of magic numbers
#> • Document your status codes in the API documentation

#!------------------ Common Pitfalls ------------------!#
#> • Using wrong status codes: Don't use 200 OK for creation operations - use 201 Created
#> • Hardcoding numbers: Use status.HTTP_201_CREATED instead of 201 for better maintainability
#> • Inconsistent status codes: Be consistent across your API endpoints
#> • Not documenting status codes: Always document what status codes your endpoints return