# Request Forms and Files
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> You can define files and form fields at the same time using File and Form. This is essential for real-world applications
#> where you need to upload files along with additional metadata like descriptions, categories, or user tokens.

## Import File and Form
from typing import Annotated
from fastapi import FastAPI, File, Form, UploadFile

app = FastAPI()
## Define File and Form Parameters
#> Create file and form parameters the same way you would for Body or Query:
@app.post("/files/")
async def create_file( file: Annotated[bytes, File()], fileb: Annotated[UploadFile, File()], token: Annotated[str, Form()], ):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }
#> The files and form fields will be uploaded as form data and you will receive the files and form fields. 
#> You can declare some of the files as bytes and some as UploadFile.

#!------------------ Key Concepts ------------------!#
#> • Mixed Parameters: You can define both File and Form parameters in the same path operation function
#> • Multipart Encoding: The request body will be encoded as multipart/form-data instead of JSON
#> • Parameter Types: Files can be declared as bytes or UploadFile, while form fields use standard Python types
#> • HTTP Protocol: This is a standard feature of HTTP, not a FastAPI-specific limitation

#!------------------ Best Practices ------------------!#
#> • Install python-multipart dependency for handling form data and files
#> • Use UploadFile for larger files as it's more memory efficient than bytes
#> • Don't mix Body parameters with File/Form parameters in the same endpoint
#> • Validate both file and form data appropriately
#> • Consider file size limits and security implications

#!------------------ Important Warning ------------------!#
#> You can declare multiple File and Form parameters in a path operation, but you cannot also declare Body fields
#> that you expect to receive as JSON, as the request will have the body encoded using multipart/form-data instead
#> of application/json.
#> This is not a limitation of FastAPI, it's part of the HTTP protocol.