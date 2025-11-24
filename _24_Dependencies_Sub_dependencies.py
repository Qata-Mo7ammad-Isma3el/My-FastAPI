# Dependencies - Sub-dependencies
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> You can create dependencies that have sub-dependencies.
#> They can be as deep as you need them to be.
#> FastAPI will take care of solving them.
from typing import Annotated
from fastapi import Cookie, Depends, FastAPI
app = FastAPI()

## First Dependency "Dependable"
#> You could create a first dependency ("dependable") like:
def query_extractor(q: str | None = None):
    return q
#> It declares an optional query parameter q as a str, and then it just returns it.
#> This is quite simple (not very useful), but will help us focus on how the sub-dependencies work.

## Second Dependency, "Dependable" and "Dependant"
#> • Then you can create another dependency function (a "dependable") that at the same time declares a dependency 
#>   of its own (so it is a "dependant" too):
def query_or_cookie_extractor( 
                                q: Annotated[str, Depends(query_extractor)],
                                last_query: Annotated[str | None, Cookie()] = None,
                            ):
    if not q:
        return last_query
    return q

#> Let's focus on the parameters declared:
#> • Even though this function is a dependency ("dependable") itself, it also declares another 
#>   dependency (it "depends" on something else).
#> • It depends on the query_extractor, and assigns the value returned by it to the parameter q.
#> • It also declares an optional last_query cookie, as a str.
#> • If the user didn't provide any query q, we use the last query used, which we saved to a cookie before.


## Use the Dependency
#> Then we can use the dependency with:
@app.get("/items/")
async def read_query( query_or_default: Annotated[str, Depends(query_or_cookie_extractor)], ):
    return {"q_or_cookie": query_or_default}
#> • Notice that we are only declaring one dependency in the path operation function, the query_or_cookie_extractor.
#> • But FastAPI will know that it has to solve query_extractor first, to pass the results of that to 
#>   query_or_cookie_extractor while calling it.


## Using the Same Dependency Multiple Times
#> If one of your dependencies is declared multiple times for the same path operation, for example, multiple
#> dependencies have a common sub-dependency, FastAPI will know to call that sub-dependency only once per request.

#!------------------ Key Concepts ------------------!#
#> • Dependable: A function that can be used as a dependency
#> • Dependant: A function that depends on other dependencies
#> • Dependency Chain: A series of dependencies where each depends on the previous one
#> • Dependency Caching: FastAPI's optimization to avoid calling the same dependency multiple times

#!------------------ Best Practices ------------------!#
#> • Use sub-dependencies to break complex logic into smaller, testable pieces
#> • Take advantage of automatic caching for expensive operations
#> • Use use_cache=False only when you specifically need fresh values on each call
#> • Keep dependency functions focused on a single responsibility