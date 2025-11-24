# Body - Updates
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> • Data updates are a critical part of any API. FastAPI provides robust support for both full and partial updates using
#>   standard HTTP methods. Understanding the difference between PUT and PATCH is essential for building reliable APIs

## Full Updates with PUT
#> • The HTTP PUT method is designed for complete resource replacement. When you use PUT, you're saying 
#>   "replace the entire resource with this new data."

### Example Scenario:
# Current item in database
{"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2}
# PUT request body
{"name": "Barz", "price": 3, "description": None}
# Result after PUT (tax reverted to default!)
{"name": "Barz", "price": 3, "description": None, "tax": 10.5}
#! Critical Warning: Missing fields in PUT requests will use their model defaults, potentially overwriting valuable data.
#! In the example above, the custom tax: 20.2 was lost and reverted to the default 10.5.

## Partial Updates with PATCH
#> • The HTTP PATCH method is designed for partial modifications. When you use PATCH, you're saying 
#>   "only change these specific fields, leave everything else alone."

### Example Scenario:
# Current item in database
{"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2}
# PATCH request body (only price)
{"price": 25.99}
# Result after PATCH (other fields preserved!)
{"name": "Bar", "description": "The bartenders", "price": 25.99, "tax": 20.2}

#> • Key Advantage: PATCH preserves existing data while only updating the fields you specify. 
#>   This prevents accidental data loss.

#? When to Use Each Method
## Use PUT when:
#> • You have the complete, updated resource
#> • You want to replace all fields intentionally
#> • You're implementing "save" functionality where users edit all fields

## Use PATCH when:
#> • You only want to update specific fields
#> • You're implementing incremental updates
#> • You want to preserve existing data you don't have access to
#> • You're building mobile apps with limited bandwidth

## Real-World Considerations
#> PATCH Adoption: While PATCH is technically superior for partial updates, many development teams use only PUT 
#> for simplicity. FastAPI supports both approaches equally well, so choose what fits your team's needs.
#> API Design: Consider your client applications. Mobile apps often prefer PATCH to save bandwidth, while admin 
#> interfaces might use PUT for complete form submissions.
#!------------------ Key Concepts ------------------!#

## Pydantic Integration

### exclude_unset Parameter: The secret to safe partial updates lies in Pydantic's exclude_unset parameter:
#> Only gets fields that were explicitly set in the request
#code: update_data = item.dict(exclude_unset=True)
#> This excludes fields that weren't provided in the request, preventing default values from overwriting existing data.

### Model Copying: Pydantic's .copy() method safely merges updates:
#>  Create updated model without mutating the original
#code: updated_item = stored_item_model.copy(update=update_data)

### JSON Encoding: Always use jsonable_encoder for database storage:
#> Converts Pydantic models to JSON-compatible dictionaries
#code: encoded_item = jsonable_encoder(updated_item)

### Response Models
#> Always specify response_model=Item to ensure consistent API responses and automatic OpenAPI documentation generation.

#!------------------ Best Practices ------------------!#
#> • Use PUT for complete resource replacement
#> • Use PATCH for partial updates to avoid data loss
#> • Always validate that the resource exists before updating
#> • Use exclude_unset=True to only get explicitly set fields
#> • Handle 404 errors gracefully for non-existent resources
#> • Use response_model to ensure consistent API responses


#!------------------ Complete Example ------------------!#
#> from official FastAPI tutorials
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None
    tax: float = 10.5
    tags: list[str] = []


items = {
    "foo": {"name": "Foo", "price": 50.2},
    "bar": {"name": "Bar", "description": "The bartenders", "price": 62, "tax": 20.2},
    "baz": {"name": "Baz", "description": None, "price": 50.2, "tax": 10.5, "tags": []},
}


@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str):
    return items[item_id]


@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    print('*'*150)
    print(f"items before:{item}")
    update_item_encoded = jsonable_encoder(item)
    print(f"items after:{update_item_encoded}")
    print('*'*150)
    items[item_id] = update_item_encoded
    return update_item_encoded

@app.patch("/items/{item_id}", response_model=Item)
async def update_item(item_id: str, item: Item):
    print('*'*150)
    stored_item_data = items[item_id]
    print(f"stored_item_data={stored_item_data}")
    
    stored_item_model = Item(**stored_item_data)
    print(f"stored_item_model={stored_item_model}")
    
    update_data = item.model_dump(exclude_unset=True)
    print(f"update_data={update_data}")
    
    updated_item = stored_item_model.model_copy(update=update_data)
    print(f"updated_item={updated_item}")
    
    print('*'*150)
    items[item_id] = jsonable_encoder(updated_item)
    return updated_item