#
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

from fastapi import FastAPI
app = FastAPI()

#!------------------ What are Path Parameters?  ------------------!#
'''
#? What are Path Parameters?
#> Think of path parameters like variables in your URL. Instead of having fixed paths like /user1, /user2, /user3,
#> you can have one dynamic path like /users/{user_id} that works for any user ID.
## Real-World Examples:
#> You see path parameters everywhere on the web:
#> • YouTube: youtube.com/watch?v=VIDEO_ID
#> • GitHub: github.com/USERNAME/REPOSITORY
#> • Online stores: store.com/products/PRODUCT_ID
#> • Social media: twitter.com/USERNAME
'''
#!------------------ How Path Parameters Work  ------------------!#
## Basic Syntax
@app.get("/users/{user_id}")
def get_user(user_id):
    return {"user_id": user_id}
'''
## Key parts:
#> {user_id} in the path defines the parameter
#> user_id function parameter captures the value
#> The names must match exactly!
## URL Examples:
#> With the endpoint above, these URLs would work:
#> • /users/123 → user_id = "123"
#> • /users/alice → user_id = "alice"
#> • /users/admin → user_id = "admin"
'''
#!------------------ Type Hints for Validation  ------------------!#
#> FastAPI can automatically validate and convert path parameters using Python type hints:

## String Parameters (Default)
@app.get("/users/{username}")
def get_user(username: str):
    return {"username": username}

## Integer Parameters
@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}
#> What happens:
#> /items/123 ✅ Works → item_id = 123 (integer)
#> /items/abc ❌ Error → Returns 422 validation error

## Float Parameters
@app.get("/prices/{price}")
def get_price_info(price: float):
    return {"price": price, "currency": "USD"}

#!------------------ Step-by-Step Examples ------------------!#
## Example 1: User Profile Endpoint
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    """Get user information by ID."""
    return {
        "user_id": user_id,
        "message": f"Hello user {user_id}!"
    }

#> Test it:
#> • Visit /users/john → {"user_id": "john", "message": "Hello user john!"}

## Example 2: Product with Integer ID
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get product details by ID."""
    return {
        "product_id": product_id,
        "name": f"Product #{product_id}",
        "available": True
    }
#> Test it:
#> • Visit /products/42 → {"product_id": 42, "name": "Product #42", "available": true}
#> • Visit /products/abc → Validation error (not a number)

## Example 3: Multiple Path Parameters
@app.get("/users/{user_id}/posts/{post_id}")
async def get_user_post(user_id: str, post_id: int):
    """Get a specific post from a specific user."""
    return {
        "user_id": user_id,
        "post_id": post_id,
        "title": f"Post {post_id} by {user_id}"
    }
#> Test it:
#> • Visit /users/alice/posts/5 → Gets post 5 from user alice
#!------------------ Best Practices ------------------!#
## 1. Use Descriptive Names
#> ✅ Good - clear and descriptive
@app.get("/users/{user_id}")
def get_user(user_id: str):
    pass

#> ❌ Avoid - unclear abbreviations 
@app.get("/users/{uid}")
def get_user(uid: str):
    pass

## 2. Add Type Hints
#> ✅ Good - automatic validation
@app.get("/items/{item_id}")
def get_item(item_id: int):
    pass

#> ❌ Missing - no validation
@app.get("/items/{item_id}")
def get_item(item_id):
    pass

## 3. Use Docstrings
#> ✅ Good - clear documentation
@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Get product details by ID."""
    return {"product_id": product_id}

#!------------------ Common Beginner Mistakes ------------------!#
## Mistake 1: Mismatched Parameter Names
#> ❌ Wrong - names don't match
@app.get("/users/{user_id}")
def get_user(id):  # Should be 'user_id'
    return {"id": id}

## Mistake 2: Forgetting Type Hints
#> ❌ Wrong - no validation
@app.get("/items/{item_id}")
def get_item(item_id):  # Should be 'item_id: int'
    return {"item_id": item_id}

## Mistake 3: Wrong Bracket Style
#> ❌ Wrong - using square brackets
#> @app.get("/users/[user_id]") # Should be {user_id}

#> ❌ Wrong - using parentheses 
#> @app.get("/users/(user_id)") # Should be {user_id}
