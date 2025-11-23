# Path Parameters and Numeric Validations
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ The Path Function  ------------------!#
#> Just like Query for query parameters, FastAPI provides the Path function to add metadata 
#> and validation constraints to path parameters.

## Basic Path vs Advanced Path
### Basic approach:
from fastapi import FastAPI
app = FastAPI()
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}

### Advanced approach with Path:
from fastapi import Path

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}

#!------------------ Numeric Validation Constraints  ------------------!#
## Basic Numeric Constraints
from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}

#> Validation:
#> • /items/1 ✅ Valid (ge=1 means >= 1)
#> • /items/0 ❌ Invalid (less than 1)
#> • /items/-5 ❌ Invalid (less than 1)

## Multiple Constraints
@app.get("/items/{item_id}")
def read_item( item_id: int = 
                Path(
                    title="Item ID", 
                    description="The ID of the item",
                    ge=1,
                    le=1000
                    ) 
                ) -> dict:
    return {"item_id": item_id}

## Available numeric constraints:
#> • ge: Greater than or equal
#> • gt: Greater than
#> • le: Less than or equal
#> • lt: Less than

#!------------------ Official Tutorial Examples ------------------!#
## Example 1: Basic Path Validation
### From the official tutorial:
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=1)):
    return {"item_id": item_id}

## Example 2: Path with Metadata
@app.get("/items/{item_id}")
def read_item( item_id: int = 
                Path(
                    title="Item ID",
                    description="The ID of the item to get",
                    ge=0,
                    le=1000
                    )
                )-> dict:
    return {"item_id": item_id}

## Example 3: Combining Path and Query Validations
@app.get("/items/{item_id}")
def read_item( item_id: int = 
                Path(title="Item ID",
                    description="The ID of the item to get",
                    ge=0, le=1000
                    ),
                q: str | None = Query(default=None, alias="item-query") ):
    return {"item_id": item_id, "q": q}


#!------------------ Path Parameter Features ------------------!#
## Validation Constraints
#> • ge: Greater than or equal (≥)
#> • gt: Greater than (>)
#> • le: Less than or equal (≤)
#> • lt: Less than (<)

## Metadata and Documentation
#> • title: Parameter title in docs
#> • description: Parameter description
#> • deprecated: Mark parameter as deprecated
#> • include_in_schema: Include/exclude from OpenAPI schema
#> • example: Example value for documentation

## Example with Full Metadata
@app.get("/products/{product_id}")
def get_product( product_id: int = 
                Path( 
                        title="Product ID",
                        description="The unique identifier for the product",
                        examples=42,
                        ge=1,
                        le=999999 
                    ) 
                ) -> dict:
    return {"product_id": product_id}

#!------------------ Order Matters: Path Before Query ------------------!#
#! When combining Path and Query parameters, you need to be careful about parameter order:
#> ✅ Correct - Path parameter first
@app.get("/items/{item_id}")
def read_item( item_id: int = Path(ge=1), q: str | None = Query(default=None) ):
    return {"item_id": item_id, "q": q}

#> ❌ Wrong - Query parameter before Path (syntax error)
@app.get("/items/{item_id}")
def read_item( q: str | None = Query(default=None), item_id: int = Path(ge=1)): #> SyntaxError!
    return {"item_id": item_id, "q": q}


### Solution: Use * to Separate or use Annotated from typing
@app.get("/items/{item_id}")
def read_item( 
                *, # This allows any order after the * 
                q: str | None = Query(default=None),
                item_id: int = Path(ge=1)
            ):
    return {"item_id": item_id, "q": q}

#!------------------ Advanced Path Validation ------------------!#
## Float Path Parameters
@app.get("/prices/{price}")
def get_price_info( price: float = Path(gt=0.0, le=10000.0, description="Price in USD") ):
    return {"price": price, "currency": "USD"}

## String Path Parameters with Validation
@app.get("/users/{username}")
def get_user( username: str = 
                Path(
                        min_length=3,
                        max_length=20,
                        regex="^[a-zA-Z0-9_]+$",
                        description="Username (alphanumeric and underscore only)"
                    ) 
                ):
    return {"username": username}

#!------------------ Best Practices ------------------!#
## 1. Use Reasonable Constraints
#> ✅ Good - realistic ID range
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=1, le=999999)):
    pass

#> ❌ Avoid - unrealistic constraints
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=1000000, le=1000001)):
    pass

## 2. Add Helpful Documentation
#> ✅ Good - clear documentation
@app.get("/products/{product_id}")
def get_product( product_id: int = Path( title="Product ID", description="The unique identifier for the product in our catalog", ge=1 ) ):
    pass

## 3. Use Appropriate Data Types
#> ✅ Good - int for IDs
@app.get("/users/{user_id}")
def get_user(user_id: int = Path(ge=1)):
    pass

#> ✅ Good - str for usernames
@app.get("/users/{username}")
def get_user(username: str = Path(min_length=3)):
    pass

#!------------------ Common Beginner Mistakes ------------------!#
## Mistake 1: Wrong Parameter Order
#> ❌ Wrong - Query before Path
@app.get("/items/{item_id}")
def read_item(q: str = Query(), item_id: int = Path()):  # SyntaxError
    pass

#> ✅ Correct - Path first, or use *
@app.get("/items/{item_id}")
def read_item(*, item_id: int = Path(), q: str = Query()):
    pass

## Mistake 2: Forgetting to Import Path
#> ❌ Wrong - Path not imported
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=1)):  # NameError
    pass

#> ✅ Correct - import Path
from fastapi import Path

## Mistake 3: Unrealistic Constraints
#> ❌ Wrong - impossible to satisfy
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=100, le=10)):  # ge > le!
    pass

#> ✅ Correct - logical constraints
@app.get("/items/{item_id}")
def read_item(item_id: int = Path(ge=1, le=1000)):
    pass