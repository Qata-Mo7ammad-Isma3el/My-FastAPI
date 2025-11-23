# Query Parameters and String Validations
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Advanced Query Parameter Features ------------------!#
'''
#> While basic query parameters work great with default values, FastAPI provides the Query function 
#> for advanced features like validation, constraints, and documentation. 
'''
## Basic Query vs Advanced Query

### Basic approach:
from fastapi import FastAPI, Query
app = FastAPI()
@app.get("/items/")
def read_items(q: str | None = None):
    return {"q": q}

### Advanced approach with Query:
from fastapi import Query

@app.get("/items/")
def read_items(q: str | None = Query(default=None, max_length=50)):
    return {"q": q}

#!------------------ The Query Function ------------------!#
#> The Query function allows you to add metadata and validation constraints to query parameters.

## Basic Query Usage
from fastapi import FastAPI, Query

app = FastAPI()
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]

@app.get("/items/")
def read_items(q: str | None = Query(default=None, max_length=50)):
    results = []
    if q:
        # Filter items based on query
        results = [item for item in fake_items_db if q.lower() in item["item_name"].lower()]
    else:
        results = fake_items_db
    return {"results": results}

## String Validation Constraints
@app.get("/items/")
def read_items( q: str | None =
                Query( 
                    default=None,
                    min_length=3, #> Minimum 3 characters 
                    max_length=50, #> Maximum 50 characters
                    regex="^[a-zA-Z0-9 ]*$" #> Only letters, numbers, and spaces 
                ) 
            ):
    return {"query": q}

## Numeric Validation Constraints
@app.get("/items/")
def read_items( 
                skip: int = Query(default=0, ge=0),#> Greater than or equal to 0 
                limit: int = Query(default=10, ge=1, le=100) #> Between 1 and 100 
                ):
    return {"skip": skip, "limit": limit}

#!------------------ Official Tutorial Examples ------------------!#
## Example 1: Basic Query Validation
### From the official tutorial:

@app.get("/items/")
def read_items(q: str | None = Query(default=None, max_length=50)):
    results = []
    if q:
        results = [{"item_name": "Foo", "description": "A very nice Item"}]
    return {"q": q, "results": results}

## Example 2: Required Query Parameters
@app.get("/items/")
def read_items(q: str = Query(min_length=3)):
    return {"q": q}
#! Note: When you use Query() without a default, the parameter becomes required.

## Example 3: Query with Multiple Constraints
@app.get("/items/")
def read_items( q: str = 
                Query( 
                    min_length=3,
                    max_length=50,
                    regex="^fixedquery$",
                    description="Query string for the items to search in the database that have a good match",
                    deprecated=False 
                    ) 
                ):
    return {"q": q}

#!------------------ Query Parameter Features ------------------!#
## Validation Constraints
#> • min_length: Minimum string length
#> • max_length: Maximum string length
#> • regex: Regular expression pattern
#> • ge: Greater than or equal (numbers)
#> • le: Less than or equal (numbers)
#> • gt: Greater than (numbers)
#> • lt: Less than (numbers)

## Metadata and Documentation
#> • description: Parameter description in docs
#> • deprecated: Mark parameter as deprecated
#> • include_in_schema: Include/exclude from OpenAPI schema
#> • examples: Example value for documentation

## Example with Full Metadata:
@app.get("/items/")
def read_items( q: str | None = 
                Query(
                    default=None,
                    title="Query string",
                    description="Query string for the items to search in the database",
                    min_length=3,
                    max_length=50,
                    examples="laptop"
                    ) 
                ) -> dict:
    return {"q": q}

#!------------------ List Query Parameters ------------------!#
#> You can also receive multiple values for the same query parameter:
@app.get("/items/")
def read_items(q: list[str] | None = Query(default=None)):
    return {"q": q}
### URL Examples:
#> • /items/?q=foo&q=bar → q = ["foo", "bar"]
#> • /items/ → q = None

## With Validation
@app.get("/items/")
def read_items( q: list[str] = 
                Query(
                    default=["foo", "bar"],
                    title="Query string",
                    description="Query string for the items to search in the database",
                    min_length=3
                    )
                ) -> dict:
    return {"q": q}

#!------------------ Best Practices ------------------!#
## 1. Use Meaningful Constraints
#> ✅ Good - reasonable limits
@app.get("/search/")
def search(q: str = Query(min_length=3, max_length=100)):
    pass

#> ❌ Avoid - unrealistic constraints
@app.get("/search/")
def search(q: str = Query(min_length=50, max_length=51)):
    pass

## 2. Add Helpful Descriptions
#> ✅ Good - clear documentation
@app.get("/items/")
def read_items( q: str | None = Query( default=None, description="Search term to filter items by name", examples="laptop" ) ):
    pass

## 3. Use Appropriate Defaults
#> ✅ Good - sensible defaults
@app.get("/items/")
def read_items( limit: int = Query(default=10, ge=1, le=100) ):
    pass

#!------------------ Common Beginner Mistakes ------------------!#
## Mistake 1: Forgetting to Import Query
#> ❌ Wrong - Query not imported
@app.get("/items/")
def read_items(q: str = Query(max_length=50)):  #> NameError
    pass

#> ✅ Correct - import Query
from fastapi import Query

## Mistake 2: Mixing Query and Default Syntax
#> ❌ Wrong - mixing approaches
@app.get("/items/")
def read_items(q: str | None = None, limit: int = Query(default=10)):
    pass

#> ✅ Correct - consistent approach
@app.get("/items/")
def read_items( q: str | None = Query(default=None), limit: int = Query(default=10) ):
    pass

## Mistake 3: Unrealistic Constraints
#> ❌ Wrong - too restrictive
@app.get("/search/")
def search(q: str = Query(min_length=100)):  #> Too long for search
    pass

#> ✅ Correct - reasonable constraints
@app.get("/search/")
def search(q: str = Query(min_length=3, max_length=50)):
    pass
