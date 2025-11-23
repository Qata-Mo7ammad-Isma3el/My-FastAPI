# Request Forms
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#

#> When you need to receive form fields instead of JSON, you can use Form. This is particularly useful when dealing
#> with HTML forms or when integrating with systems that send data as form-encoded rather than JSON.

#? Why Form Data?
#> HTML forms (<form></form>) send data to the server using a "special" encoding that's different from JSON. This encoding
#> is called application/x-www-form-urlencoded (or multipart/form-data for file uploads).

#> For example, in OAuth2 "password flow", the specification requires sending username and password as form fields,
#> not JSON.

## Import Form
#> First, import Form from fastapi:

from fastapi import FastAPI, Form
app = FastAPI()

## Define Form Parameters
#> Create form parameters the same way you would for Body or Query:

@app.post("/login/")
def login(username: str = Form(), password: str = Form()):
    return {"username": username}

#!------------------ Key Concepts ------------------!#
## Form vs JSON
#> • JSON data: Content-Type: application/json
#code: {"username": "john", "password": "secret"}
#> • Form data: Content-Type: application/x-www-form-urlencoded
#code: username=john&password=secret


## Form Class Features
#> Form is a class that inherits directly from Body, so you can use the same configurations:
#> • Validation
#> • Examples
#> • Aliases (e.g., user-name instead of username)
#> • Documentation

from fastapi import FastAPI, Form

app = FastAPI()

@app.post("/login/")
def login( username: str = Form(min_length=3, max_length=20), password: str = Form(min_length=8) ):
    return {"username": username}

## Explicit Form Declaration
#> To declare form bodies, you need to use Form explicitly. Without it, the parameters 
#> would be interpreted as query parameters or body (JSON) parameters.
#!------------------ Best Practices ------------------!#
#> • Use form data for HTML form submissions
#> • Use form data when integrating with OAuth2 password flow
#> • Use JSON for API-to-API communication
#> • Always validate form data with appropriate constraints
#> • Use descriptive parameter names that match HTML form field names
#> • Consider using form data for simple key-value pairs

#!------------------ Common Pitfalls ------------------!#
#> • Forgetting to use Form(): Without Form(), parameters become query parameters
#> • Mixing form and JSON: Don't mix form fields and JSON body in the same endpoint
#> • Wrong Content-Type: Ensure clients send application/x-www-form-urlencoded
#> • Missing validation: Always add appropriate validation to form fields
#> • Security concerns: Never log or expose passwords in responses


