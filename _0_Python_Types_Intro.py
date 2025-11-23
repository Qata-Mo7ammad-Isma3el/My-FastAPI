# learning Python Types for FastAPI
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

# pip freeze > requirements.txt

#> Python has support for optional "type hints" (also called "type annotations").
#> These "type hints" or annotations are a special syntax that allow declaring the type of a variable.
#> By declaring types for your variables, editors and tools can give you better support.
#> Let's start with a simple example:

#!------------------ motivation  ------------------!#
def get_full_name(first_name, last_name):
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))

#> The function does the following:
#> • Takes a first_name and last_name.
#> • Converts the first letter of each one to upper case with title().
#> • Concatenates them with a space in the middle.

#!------------------ Add types ------------------!#
#> Let's modify a single line from the previous version.

def get_full_name(first_name: str, last_name: str) -> str:
    full_name = first_name.title() + " " + last_name.title()
    return full_name

print(get_full_name("john", "doe"))

#!------------------ Declaring types ------------------!#
#> More general Example for type hints 
def get_items(item_a: str, item_b: int, item_c: float, item_d: bool, item_e: bytes) -> list:
    return item_a, item_b, item_c, item_d, item_d, item_e #> return will automatically packages those values into a single tuple.

print(get_items('mohammad' , 10, 13.4, True, 12))

#!------------------ Generic types with type parameters ------------------!#
## List
#> For example, let's define a variable to be a list of str.
def process_items(items: list[str]) -> None:
    for item in items:
        print(item)
#> That means: "the variable items is a list, and each of the items in this list is a str".

## Tuple and Set
#> You would do the same to declare tuples and sets:
def process_items(items_t: tuple[int, int, str], items_s: set[bytes]) -> tuple:
    return items_t, items_s
#> This means:
#> • The variable items_t is a tuple with 3 items, an int, another int, and a str.
#> • The variable items_s is a set, and each of its items is of type bytes.

## Dict
#> To define a dict, you pass 2 type parameters, separated by commas.
def process_items(prices: dict[str, float])-> None:
    for item_name, item_price in prices.items():
        print(item_name)
        print(item_price)
#> This means:
#> The variable prices is a dict:
#> • The keys of this dict are of type str (let's say, the name of each item).
#> • The values of this dict are of type float (let's say, the price of each item).

## Union
#> You can declare that a variable can be any of several types, for example, an int or a str
def process_item(item: int | str='Mohammad')-> None:
    print(item)
#> this means that item could be an int or a str.

## Possibly None
#> You can declare that a value could have a type, like str, but that it could also be None.
from typing import Optional
def say_hi(name: Optional[str] = None)-> None:
    if name is not None:
        print(f"Hey {name}!")
    else:
        print("Hello World")
#> Using Optional[str] instead of just str will let the editor help you detect errors where you could be assuming 
#> that a value is always a str, when it could actually be None too.

## Using Union or Optional
#> If you are using a Python version below 3.10, here's a tip from my very subjective point of view:
#> 🚨 Avoid using Optional[SomeType]
#> Instead ✨ use Union[SomeType, None] ✨.
'''
#> Both are equivalent and underneath they are the same, but I would recommend Union instead of Optional 
#> because the word "optional" would seem to imply that the value is optional, and it actually means "it can be None",
#> even if it's not optional and is still required.
'''

## Classes as types
#> You can also declare a class as the type of a variable.
#> Let's say you have a class Person, with a name:
class Person:
    def __init__(self, name: str)-> None:
        self.name = name


def get_person_name(one_person: Person) -> str:
    return one_person.name

#!------------------ Pydantic models ------------------!#

'''
#> • Pydantic is a Python library to perform data validation.
#> • You declare the "shape" of the data as classes with attributes.
#> • And each attribute has a type.
#> • Then you create an instance of that class with some values and it will validate the values,
#>   convert them to the appropriate type (if that's the case) and give you an object with all the data.
#> • And you get all the editor support with that resulting object.
#> • An example from the official Pydantic docs:
'''
from datetime import datetime

from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
    "id": "123",
    "signup_ts": "2017-06-01 12:22",
    "friends": [1, "2", b"3"],
}
user = User(**external_data)
print(user)
#> User id=123 name='John Doe' signup_ts=datetime.datetime(2017, 6, 1, 12, 22) friends=[1, 2, 3]
print(user.id)
#> 123

#!------------------ Type Hints with Metadata Annotations ------------------!#
from typing_extensions import Annotated
def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"

