# First_Steps.py
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ The simplest FastAPI file could look like this ------------------!#
from fastapi import FastAPI
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#> Run the live server with:
#> fastapi dev First_Steps.py
#> to see the API use -> http://127.0.0.1:8000
#> Interactive API docs -> http://127.0.0.1:8000/docs
#> Interactive API docs -> http://127.0.0.1:8000/redoc

#!------------------ OpenAPI ------------------!#
#> FastAPI generates a "schema" with all your API using the OpenAPI standard for defining APIs.

## "Schema"
#> A "schema" is a definition or description of something. Not the code that implements it, but just an abstract description.

## API "schema"
#> In this case, OpenAPI is a specification that dictates how to define a schema of your API.
#> This schema definition includes your API paths, the possible parameters they take, etc.

## Data "schema"
#> The term "schema" might also refer to the shape of some data, like a JSON content.
#> In that case, it would mean the JSON attributes, and data types they have, etc.

## OpenAPI and JSON Schema
#> OpenAPI defines an API schema for your API. And that schema includes definitions (or "schemas")
#> of the data sent and received by your API using JSON Schema, the standard for JSON data schemas.

## Check the openapi.json¶
#> If you are curious about how the raw OpenAPI schema looks like,
#> FastAPI automatically generates a JSON (schema) with the descriptions of all your API.
#> You can see it directly at: http://127.0.0.1:8000/openapi.json

## What is OpenAPI for
#> • The OpenAPI schema is what powers the two interactive documentation systems included.
#> • And there are dozens of alternatives, all based on OpenAPI. You could easily add any of 
#>   those alternatives to your application built with FastAPI.
#> • You could also use it to generate code automatically, for clients that communicate with your API.
#>   For example, frontend, mobile or IoT applications.

## Deploy your app (optional) 
#> visit https://fastapicloud.com/ for more details 
#> use in bash -> fastapi login 
#> then use -> fastapi deploy

#!------------------ Recap, step by step ------------------!#
## Step 1: import FastAPI
#> FastAPI is a Python class that provides all the functionality for your API.
#! Note: FastAPI is a class that inherits directly from Starlette.
from fastapi import FastAPI

## Step 2: create a FastAPI "instance"
#> Here the app variable will be an "instance" of the class FastAPI.
#> This will be the main point of interaction to create all your API.
app = FastAPI()

## Step 3: create a path operation
#* Path
#> "Path" here refers to the last part of the URL starting from the first '/'.
'''
#> So, in a URL like: https://example.com/items/foo
#> ...the path would be: /items/foo
#! Note: A "path" is also commonly called an "endpoint" or a "route".
#> While building an API, the "path" is the main way to separate "concerns" and "resources".

#* Operation 
#> "Operation" here refers to one of the HTTP "methods".
#> One of:
#> • POST
#> • GET
#> • PUT
#> • DELETE
#> ...and the more exotic ones:
#> OPTIONS
#> • HEAD
#> • PATCH
#> • TRACE
#! Note: In the HTTP protocol, you can communicate to each path using one (or more) of these "methods".
#> When building APIs, you normally use these specific HTTP methods to perform a specific action.
#> Normally you use:
#> • POST: to create data.
#> • GET: to read data.
#> • PUT: to update data.
#> • DELETE: to delete data.
#> So, in OpenAPI, each of the HTTP methods is called an "operation".
#! Note: We are going to call them "operations" too.
'''

#> The @app.get("/") tells FastAPI that the function right below is in charge of handling requests that go to:
#> • the path /
#> • using a get operation

'''
#! Note: 
#> @decorator Info
#> That @something syntax in Python is called a "decorator".
#> You put it on top of a function. Like a pretty decorative hat (I guess that's where the term came from).
#> A "decorator" takes the function below and does something with it.
#> In our case, this decorator tells FastAPI that the function below corresponds to the path / with an operation get.
#> It is the "path operation decorator".
#> You can also use the other operations:
#> • @app.post()
#> • @app.put()
#> • @app.delete()
#> And the more exotic ones:
#> • @app.options()
#> • @app.head()
#> • @app.patch()
#> • @app.trace()

#> Tip:
#> • You are free to use each operation (HTTP method) as you wish.
#> • FastAPI doesn't enforce any specific meaning.
#> • The information here is presented as a guideline, not a requirement.
#> • For example, when using GraphQL you normally perform all the actions using only POST operations.
'''



## Step 4: define the path operation function
#> This is our "path operation function":
#> • path: is '/'.
#> • operation: is get.
#> • function: is the function below the "decorator" (below @app.get("/")).
@app.get("/")
async def root():
    return {"message": "Hello World"} ## Step 5: return the content

#* async def root():
#> This is a Python function.
#> It will be called by FastAPI whenever it receives a request to the URL "/" using a GET operation.
#> In this case, it is an async function.



