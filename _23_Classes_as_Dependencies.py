# Classes as Dependencies
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> Before diving deeper into the Dependency Injection system, let's upgrade the previous example.

#> A dict from the Previous Example
#> In the previous example, we were returning a dict from our dependency:
async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

#> But then we get a dict in the parameter commons of the path operation function.
#> • And we know that editors can't provide a lot of support (like completion) for dicts, because they can't know their keys
#>   and value types.
#> We can do better...

#? What Makes a Dependency
#> Up to now you have seen dependencies declared as functions.
#> But that's not the only way to declare dependencies (although it would probably be the more common).
#> The key factor is that a dependency should be a "callable".
#> A "callable" in Python is anything that Python can "call" like a function.
#> So, if you have an object something (that might not be a function) and you can "call" it (execute it) like:
#code: something() or something(some_argument, some_keyword_argument="foo")
#! then it is a "callable".

## Classes as Dependencies
#> You might notice that to create an instance of a Python class, you use that same syntax.
#> For example:

class Cat:
    def __init__(self, name: str):
        self.name = name

fluffy = Cat(name="Mr Fluffy")

#> In this case, fluffy is an instance of the class Cat.
#> And to create fluffy, you are "calling" Cat.
#> So, a Python class is also a callable.
#> Then, in FastAPI, you could use a Python class as a dependency.
#> What FastAPI actually checks is that it is a "callable" (function, class or anything else) and the parameters defined.
#> • If you pass a "callable" as a dependency in FastAPI, it will analyze the parameters for that "callable", and process 
#>   them in the same way as the parameters for a path operation function. Including sub-dependencies.

## Shortcut Syntax
#> FastAPI provides a shortcut for cases where the dependency is specifically a class that FastAPI will "call" to 
#> create an instance of the class itself.

#> Instead of writing:
#code: commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]
#> ...you can write:
#code: commons: Annotated[CommonQueryParams, Depends()]
#> You declare the dependency as the type of the parameter and use Depends() without any parameter, instead of having to
#> write the full class again inside Depends(CommonQueryParams).


from typing import Annotated
from fastapi import Depends, FastAPI

app = FastAPI()


fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

class CommonQueryParams:
    def __init__(self, q: str | None = None, skip: int = 0, limit: int = 100):
        self.q = q
        self.skip = skip
        self.limit = limit


@app.get("/items/")
async def read_items(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response.update({"q": commons.q})
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response.update({"items": items})
    return response


#!------------------ Key Concepts ------------------!#
#> • Callable Dependencies: Functions, classes, or any callable object can be dependencies
#> • Class Dependencies: Provide better type support than dict-based dependencies
#> • Parameter Analysis: FastAPI analyzes __init__ parameters for class dependencies
#> • Type Annotations: Help editors provide better code completion and type checking
#> • Dependency Shortcut: Depends() without parameters when the type annotation matches the class

#!------------------ Best Practices ------------------!#
#> • Use class dependencies for better type support and editor assistance
#> • Keep dependency classes focused on their specific responsibility
#> • Use meaningful parameter names and type hints
#> • Take advantage of FastAPI's shortcut syntax to reduce code repetition

## Tip
#> If the shortcut syntax confuses you more than it helps, ignore it. You don't need it.
#> It is just a shortcut. Because FastAPI cares about helping you minimize code repetition.


