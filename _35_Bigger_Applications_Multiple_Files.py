# Bigger Applications - Multiple Files
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> • When building real-world applications, putting everything in a single file becomes unwieldy. FastAPI provides excellent
#>   tools to organize your code into multiple files while maintaining all the flexibility and features you need.

## Project Structure
### The recommended structure for larger FastAPI applications follows Python package conventions:
'''
#> app/
#> ├── __init__.py         # Makes 'app' a Python package
#> ├── main.py             # Main application entry point
#> ├── dependencies.py     # Shared dependencies
#> ├── routers/            # Route modules
#> │   ├── __init__.py     # Makes 'routers' a subpackage
#> │   ├── users.py        # User-related routes
#> │   └── items.py        # Item-related routes
#> └── internal/           # Internal modules
#>     ├── __init__.py     # Makes 'internal' a subpackage
#>     └── admin.py        # Admin-only routes
'''
## Key Concepts 

### 1. APIRouter
#> APIRouter is like a "mini FastAPI" that you can use to organize related routes:

from fastapi import APIRouter , Depends , FastAPI

router = APIRouter()

@router.get("/users/")
async def get_users():
    return {"users": []}

### 2. Router Configuration
#> You can configure routers with common settings:

router = APIRouter(
    prefix="/items",           # All routes get this prefix
    tags=["items"],           # OpenAPI tags for documentation
    dependencies=[Depends(auth)], # Applied to all routes
    responses={404: {"description": "Not found"}},
)


### 3. Including Routers
#> In your main application, include routers:

from fastapi import FastAPI
from .routers import users, items

app = FastAPI()

app.include_router(users.router)
app.include_router(items.router)


### 4. Relative Imports
#> Use relative imports to access modules within your package:

#> From app/routers/items.py
from ..dependencies import get_token_header  # Go up one level
from . import users  # Same level

### 5. Dependencies Across Modules
#> Dependencies can be shared across the entire application or specific routers:

#> Global dependencies (applied to all routes)
app = FastAPI(dependencies=[Depends(global_dep)])

#> Router-specific dependencies
router = APIRouter(dependencies=[Depends(router_dep)])

#> Route-specific dependencies
@router.get("/", dependencies=[Depends(route_dep)])
async def get_items():
    pass

#!------------------ Key Concepts ------------------!#
#> • APIRouter: Organizes related routes into modules
#> • Package Structure: Use __init__.py files to create Python packages
#> • Relative Imports: Navigate between modules using . and .. syntax
#> • Router Inclusion: Use app.include_router() to add routers to your main app
#> • Dependency Sharing: Apply dependencies at app, router, or route level

#!------------------ Best Practices ------------------!#
#> • Group Related Routes: Put related functionality in the same router
#> • Use Prefixes: Apply common URL prefixes at the router level
#> • Share Dependencies: Define common dependencies once and reuse them
#> • Organize by Feature: Structure your code by business logic, not technical layers
#> • Keep Main App Simple: The main app should primarily orchestrate routers
