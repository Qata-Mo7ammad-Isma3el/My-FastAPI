# Dependencies - Path Operation Decorators
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> In some cases you don't really need the return value of a dependency inside your path operation function.
#> Or the dependency doesn't return a value.
#> But you still need it to be executed/solved.
#> • For those cases, instead of declaring a *path operation function parameter with Depends*, you can add a list of 
#>   dependencies to the *path operation decorator*.
#> Add dependencies to the Path Operation Decorator
#> The path operation decorator receives an optional argument dependencies.
#> It should be a list of Depends():
from typing import Annotated

from fastapi import Depends, FastAPI, Header, HTTPException

app = FastAPI()
async def verify_token(x_token: Annotated[str, Header()]):
    if x_token != "fake-super-secret-token":
        raise HTTPException(status_code=400, detail="X-Token header invalid")


async def verify_key(x_key: Annotated[str, Header()]):
    if x_key != "fake-super-secret-key":
        raise HTTPException(status_code=400, detail="X-Key header invalid")
    return x_key

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item": "Foo"}, {"item": "Bar"}]

#> • These dependencies will be executed/solved the same way as normal dependencies. But their value (if they return any) 
#>   won't be passed to your path operation function.
#> • Tip: Some editors check for unused function parameters, and show them as errors. Using these dependencies in the 
#>   path operation decorator you can make sure they are executed while avoiding editor/tooling errors.
#> • It might also help avoid confusion for new developers that see an unused parameter in your code and could think 
#>   it's unnecessary.


## Dependencies Errors and Return Values
#> You can use the same dependency functions you use normally.

## Dependency Requirements
#> They can declare request requirements (like headers) or other sub-dependencies:
async def verify_token(x_token: Annotated[str, Header()]):
    pass

async def verify_key(x_key: Annotated[str, Header()]):
    pass

## Raise Exceptions
#> These dependencies can raise exceptions, the same as normal dependencies:
#code: if x_token != "fake-super-secret-token":
#code:    raise HTTPException(status_code=400, detail="X-Token header invalid")

## Return Values
#> And they can return values or not, the values won't be used.
#> So, you can reuse a normal dependency (that returns a value) you already use somewhere else, and even though
#> the value won't be used, the dependency will be executed.

#!------------------ Key Concepts ------------------!#

## Decorator Dependencies
#> Add dependencies to the decorator using a list of Depends() calls:

@app.get("/items/", dependencies=[Depends(verify_token), Depends(verify_key)])
async def read_items():
    return [{"item_id": "Foo"}]

## Execution Without Return Values
#> Dependencies in decorators:
#> • Execute normally and can raise exceptions
#> • Can access request data (headers, query params, etc.)
#> • Return values are ignored (not passed to the function)
#> • Still validate requirements and sub-dependencies

## Common Use Cases
#> • Security checks without needing user data in function
#> • Header validation for API keys or custom headers
#> • Request logging or monitoring
#> • Rate limiting or quota checks

#!------------------ Best Practices ------------------!#
#> • Use decorator dependencies when you don't need the return value
#> • Combine with function parameters when you need some dependency values
#> • Reuse existing dependencies - the same dependency function can be used in both places
#> • Handle exceptions - dependencies can still raise HTTPExceptions
#> • Editor-friendly - avoids unused parameter warnings



