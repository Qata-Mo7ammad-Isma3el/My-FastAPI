# Metadata and Docs URLs
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> When building APIs, professional documentation is essential. FastAPI automatically generates interactive documentation,
#> but you can customize the metadata to make your API documentation more informative and professional.

## API Metadata
#> You can configure several metadata fields when creating your FastAPI application. 
#> These fields appear in the automatic API documentation:
from fastapi import FastAPI

description = \
""" 
    Task Management API helps you organize your work efficiently.
    🚀 ## Features 
        * **Create and manage tasks** 
        * **Organize with categories** 
        * **Track completion status** 
"""

app = FastAPI(
    title="Task Management API",
    description=description,
    summary="A simple and efficient task manager",
    version="1.0.0",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "API Support Team",
        "url": "http://example.com/contact/",
        "email": "support@example.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)
### Available Metadata Fields
#> • title: The name of your API (appears prominently in documentation)
#> • summary: A short one-liner about your API
#> • description: Detailed description supporting Markdown formatting
#> • version: Your API version (e.g., "1.0.0", "2.3.1")
#> • terms_of_service: URL to your terms of service
#> • contact: Dictionary with name, url, and email
#> • license_info: Dictionary with name and url (or identifier)

## Markdown Support
#> The description field supports full Markdown syntax:

description = \
""" 
    ## Items You can **create**, **read**, **update**, and **delete** items.
    # ## Users Manage user accounts: 
        * Create new users 
        * Update profiles 
        * Delete accounts 
"""

## Tags Metadata
#> Organize your endpoints with tags and add descriptions for each tag:

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://example.com/items/",
        },
    },
]

app = FastAPI(openapi_tags=tags_metadata)

@app.get("/users/", tags=["users"])
async def get_users():
    return [{"username": "johndoe"}]

@app.get("/items/", tags=["items"])
async def get_items():
    return [{"name": "Item"}]

## Customizing Documentation URLs
#> FastAPI serves documentation at default URLs, but you can customize them:
app = FastAPI(
    docs_url="/documentation",  # Default: /docs
    redoc_url="/redoc",         # Default: /redoc
    openapi_url="/api/v1/openapi.json"  # Default: /openapi.json
)

#> You can also disable documentation completely:
app = FastAPI(
    docs_url=None,      # Disable Swagger UI
    redoc_url=None,     # Disable ReDoc
    openapi_url=None    # Disable OpenAPI schema
)
#!------------------ Key Concepts ------------------!#
#> • OpenAPI Schema: JSON file describing your entire API structure
#> • Swagger UI: Interactive documentation at /docs by default
#> • ReDoc: Alternative documentation UI at /redoc by default
#> • Tags: Organize endpoints into logical groups in documentation
#> • Metadata: Information about your API shown in documentation

#!------------------ Best Practices ------------------!#
#> • Write clear descriptions: Use Markdown to format documentation
#> • Version your API: Use semantic versioning (major.minor.patch)
#> • Provide contact information: Help users reach you for support
#> • Add license information: Clarify usage terms for your API
#> • Organize with tags: Group related endpoints together
#> • Keep it updated: Update metadata when your API changes
#> • Use meaningful titles: Make your API easily identifiable

