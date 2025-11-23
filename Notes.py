
#!------------------ What is model_dump? ------------------!#
'''
#? What is model_dump?
#> In Pydantic V2, model_dump() is the standard method used to convert a Pydantic model instance into a
#> standard Python dictionary.
#> • Input: A Pydantic Model instance (with validation and types).
#> • Output: A Python dict (e.g., {'key': 'value'}).

#! Note: In Pydantic V1, this was known as .dict(). In V2, it has been renamed to .model_dump().
'''
## 1. Basic Usage
#> This is the most common scenario: converting your validated data into a dictionary to pass to another function or library.
from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    username: str
    signup_ts: datetime = None

#> 1. Create an instance
user = User(id=1, username="Mohammad", signup_ts=datetime.now())

#> 2. Convert to dictionary
user_dict = user.model_dump()

print(type(user_dict)) 
#> Output: <class 'dict'>

print(user_dict)
#> Output: {'id': 1, 'username': 'Mohammad', 'signup_ts': datetime.datetime(...)}

## 2. model_dump_json vs model_dump
#> While model_dump returns a Python dictionary, model_dump_json returns a string formatted as JSON.
#> • model_dump(): Keeps Python types (e.g., datetime objects remain datetime objects).
#> • model_dump_json(): Converts everything to strings/numbers suitable for HTTP responses.

# Returns a string
json_data = user.model_dump_json()
json2_data = user.model_dump(mode="json")
print(type(json_data))
# Output: <class 'str'>

print(json_data)
print(f"this is with mode:\n{json2_data}")
# Output: '{"id":1,"username":"Mohammad","signup_ts":"2023-11-23T10:00:00.123456"}'

## 3. Advanced Features (Filtering)
#> The documentation you shared highlights powerful features to control what gets exported. 
#> You often need to hide sensitive data (like passwords) or only send specific fields.

### Exclude / Include
class Account(BaseModel):
    username: str
    password: str
    email: str

account = Account(username="admin", password="secret_password", email="admin@example.com")

#> Exclude sensitive data
safe_data = account.model_dump(exclude={'password'})
print(safe_data)
#> Output: {'username': 'admin', 'email': 'admin@example.com'}

#> Include only specific data
public_profile = account.model_dump(include={'username'})
print(public_profile)
#> Output: {'username': 'admin'}

## 4. Handling Aliases (by_alias)
#> In Python, we use snake_case (e.g., first_name), but APIs (JavaScript) often expect camelCase (e.g., firstName).
#> Pydantic handles this using aliases.
from pydantic import Field

class Profile(BaseModel):
    #> 'name' internally, but serialized as 'fullName'
    name: str = Field(serialization_alias='fullName') 

p = Profile(name="Jordan Doe")

#> Default dump (uses internal Python name)
print(p.model_dump())
#> Output: {'name': 'Jordan Doe'}

#> Dump using alias (for external APIs)
print(p.model_dump(by_alias=True))
#> Output: {'fullName': 'Jordan Doe'}
## 5. using Python's "Unpacking" operator.
from pydantic import BaseModel, EmailStr

#> Model A: What the user sends us (Input)
class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str 

#> Model B: What we save in DB (Has extra fields like 'id' and 'is_active')
class UserInDB(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True

#> --- The Logic ---

#> 1. User sends data
incoming_data = UserSignUp(username="Ahmad", email="ahmad@test.com", password="secret123")

#> 2. We want to create a DB entry. 
#> Instead of typing: username=incoming_data.username, email=incoming_data.email...
#> We use Unpacking to copy common fields, then we add the new specific fields manually.

#> Note: We exclude password because UserInDB doesn't have a 'password' field
common_data = incoming_data.model_dump(exclude={'password'})

# This line says: "Take username and email from common_data, and I will give you id manually"
user_db = UserInDB(**common_data, id=55)

print(user_db)
# Output: id=55 username='Ahmad' email='ahmad@test.com' is_active=True


#!------------------ What is Annotated? ------------------!#
#? What is Annotated?
#> Introduced in Python 3.9, Annotated allows you to attach metadata (extra information) to a type, without changing
#> the type itself.
#> Think of it like putting a sticky note on a folder.
#> Python sees the folder (the Type) and ignores the note.

#> Tools (like Pydantic or FastAPI) read the note and do something special based on what is written on it.

## The Syntax:

#> Python
#code: Annotated[ MainType, Metadata1, Metadata2, ... ]

#? Why do we use it?
#> In the modern Python ecosystem (especially FastAPI and Pydantic V2), Annotated is used for two main reasons: 
#> Reusability and Cleaner Code.

## 1. Pydantic Validation (Reusable Types)
#> Instead of defining validation logic every time you use a field, you can package the Type and the Logic together into
#> a new, reusable type.

## Without Annotated (Repetitive):
class Product(BaseModel):
    #> You have to write the Field logic inside the model
    price: float = Field(gt=0)
    
class Order(BaseModel):
    #> You have to repeat it here
    total: float = Field(gt=0) 

#> With Annotated (Reusable):
from typing import Annotated
from pydantic import BaseModel, Field

#> 1. Define the type ONCE
#> "It is a float, AND it must be greater than 0"
PositiveFloat = Annotated[float, Field(gt=0)]

#> 2. Use it everywhere
class Product(BaseModel):
    price: PositiveFloat

class Order(BaseModel):
    total: PositiveFloat

#!------------------ FastAPI Input Tools ------------------!#
from fastapi import FastAPI, Body, Query, Path, File, UploadFile, Form
#> These tell FastAPI where to look for data in an HTTP request.

## Path:
#> Where: Used for variables inside the URL itself (e.g., /users/{user_id}).
#> Use Case: Mandatory ID lookups.
#> Example: user_id: int = Path(gt=0) (Must be in the URL and greater than 0).

## Query:
#> Where: Used for variables after the ? in the URL (e.g., /users?page=2&search=john).
#> Use Case: Filtering, sorting, pagination.
#> Example: page: int = Query(default=1) (If the user doesn't send it, it's 1).

## Body:
#> Where: Inside the JSON body of the request.
#> Note: Usually, you don't import this often because if you use a Pydantic BaseModel, FastAPI automatically assumes it
#>       is a Body. You use this when you want a single value (like just a string) in the body, not a full object.

## File:
#> What: Tells FastAPI to expect a file upload as bytes.
#> Downside: It loads the entire file into RAM. If someone uploads a 1GB video, your server might crash.

## UploadFile (The Better Version):
#> What: A wrapper around the file. It uses a "spooled" file (stored on disk/temp memory), so it doesn't crash RAM.
#> Features: You can get the filename, content_type, and read it in chunks. Always prefer this over File.

## Form:
#> Where: Used for form data (application/x-www-form-urlencoded or multipart/form-data).
#> Use Case: HTML form submissions, OAuth2 password flow.
#!------------------ Pydantic Core (The Data Structure) ------------------!#

#> These are used to define what your data looks like and validate it.

## BaseModel:
#> What: The parent class for all your data models.
#> Function: It handles all the magic: validation, serialization (model_dump), and type checking.

## Field:
#> What: Used to add rules to a specific attribute inside a model.
#> Use Case: Setting default values, descriptions (for docs), or constraints (min_length, max_value).
#> Example: name: str = Field(min_length=3, description="User's full name")

## EmailStr:
#> What: A specialized string type.
#> Magic: It automatically checks if the value looks like user@domain.com. If the user sends "hello",
#>        Pydantic raises an error automatically.

## HttpUrl:
#> What: A specialized type for URLs.
#> Magic: Ensures the string starts with http:// or https:// and has a valid domain structure.
#!------------------ Typing & Advanced Validation ------------------!#
#> These are Python standard types or Pydantic helpers for complex logic.

## Any:
#> What: A Python type that means "I don't care what this is."
#> Use Case: When a variable could be a string, a number, or a list, and you want to disable type checking for it.

## Annotated:
#> What: As explained before, it acts like a "sticky note" to attach metadata (like Path or Query) to a type.
#> Example: user_id: Annotated[int, Path(gt=0)].

## model_validator:
#> What: Used when you need to validate multiple fields at the same time.
#> Scenario: Field validation checks one item (e.g., "is age > 18?"). model_validator checks relationships 
#>           (e.g., "Does password match confirm_password?").


## Putting it all together in Code
from typing import Annotated, Any, Self
from fastapi import FastAPI, Path, Query, UploadFile
from pydantic import BaseModel, Field, EmailStr, HttpUrl, model_validator

app = FastAPI()

# --- Pydantic Part (Data Definition) ---
class UserProfile(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr                        # Validates email format
    website: HttpUrl | None = None         # Validates URL format
    password: str
    confirm_password: str
    metadata: Any = None                   # Could be anything (dict, list, int)

    # Validating two fields together
    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

#> --- FastAPI Part (The Route) ---
@app.post("/users/{user_id}/upload")
async def update_user_profile(
    #> PATH: Extracts user_id from URL
    user_id: Annotated[int, Path(gt=0)], 
    
    #> QUERY: Looks for ?notify=true in URL
    notify: Annotated[bool, Query()] = False,
    
    #> UPLOADFILE: Handles the file upload safely
    avatar: UploadFile | None = None,
    
    #> BODY: The UserProfile model (automatically detected as Body)
    profile_data: UserProfile | None = None 
):
    return {
        "user_id": user_id,
        "email_saved": profile_data.email,
        "avatar_filename": avatar.filename if avatar else "No file"
    }