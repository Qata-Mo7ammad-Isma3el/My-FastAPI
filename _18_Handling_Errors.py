# Handling Errors
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> There are many situations in which you need to notify an error to a client that is using your API. 
#> This client could be a browser with a frontend, a code from someone else, an IoT device, etc.

## You could need to tell the client that:

#> • The client doesn't have enough privileges for that operation
#> • The client doesn't have access to that resource
#> • The item the client was trying to access doesn't exist

#> • In these cases, you would normally return an HTTP status code in the range of 400 (from 400 to 499). This is similar
#>   to the 200 HTTP status codes (from 200 to 299). Those "200" status codes mean that somehow there was a "success" in 
#>   the request. The status codes in the 400 range mean that there was an error from the client.

## Use HTTPException
#> To return HTTP responses with errors to the client you use HTTPException.

### Import HTTPException
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
#> Raise an HTTPException in your code
#> HTTPException is a normal Python exception with additional data relevant for APIs. 
#> Because it's a Python exception, you don't return it, you raise it
app = FastAPI()

#> Sample data (following official docs naming)
items = {"foo": "The Foo Wrestlers"}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail=" 404 Item not found")
    return {"item": items[item_id]}

## Add custom headers
#> There are some situations where it's useful to be able to add custom headers to the HTTP error. 
#> For example, for some types of security.

@app.get("/items-header/{item_id}")
async def read_item_header(item_id: str):
    if item_id not in items:
        raise HTTPException(
            status_code=404,
            detail="Item not found",
            headers={"X-Error": "There goes my error"},
        )
    return {"item": items[item_id]}

## Install custom exception handlers
#> You can add custom exception handlers with the same exception utilities from Starlette. 
#> Let's say you have a custom exception UnicornException that you (or a library you use) might raise.

class UnicornException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."},
    )

#!------------------ Key Concepts ------------------!#
#> • HTTPException: A Python exception with HTTP-specific data
#> • Status Codes: Numeric codes that indicate request outcomes
#> • Detail Messages: Human-readable error descriptions
#> • Custom Headers: Additional metadata for error responses
#> • Exception Handlers: Global error handling functions

#!------------------ Best Practices ------------------!#
#> • Use appropriate HTTP status codes (404 for not found, 400 for bad data)
#> • Provide clear, helpful error messages in the detail field
#> • Don't expose internal system information in error messages
#> • Use custom exception handlers for application-specific errors
#> • Consider security implications when returning error details