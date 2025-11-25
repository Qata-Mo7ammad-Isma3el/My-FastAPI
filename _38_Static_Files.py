# Static Files
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#? What are Static Files?
#> Static files are files that don't change dynamically - they're served exactly as they exist on disk. 
#> Common examples include:
#> • HTML files
#> • CSS stylesheets
#> • JavaScript files
#> • Images (PNG, JPG, SVG)
#> • Fonts
#> • PDF documents

## Using StaticFiles in FastAPI
#> FastAPI provides StaticFiles to automatically serve files from a directory:

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Mount static files at /static path
app.mount("/static", StaticFiles(directory="static"), name="static")

### Understanding "Mounting"
#> Mounting means adding a complete independent application at a specific path. Key points:
#> • The mounted application handles all sub-paths under its mount point
#> • It's completely independent from your main FastAPI app
#> • OpenAPI docs won't include the mounted application
#> • Different from APIRouter which integrates with your app

### Mount Parameters
app.mount("/static", StaticFiles(directory="static"), name="static")
#> • First parameter ("/static"): The URL path where files will be served
#> • directory: The local directory containing your static files
#> • name: Internal name used by FastAPI for the mount

## example Directory Structure
'''
#> myapp/
#> ├── main.py
#> └── static/
#>     ├── index.html
#>     ├── styles.css
#>     ├── script.js
#>     └── images/
#>         └── logo.png
'''
#> With the mount above, files would be accessible at:

#> http://localhost:8000/static/index.html
#> http://localhost:8000/static/styles.css
#> http://localhost:8000/static/images/logo.png

#!------------------ Key Concepts ------------------!#
#> • StaticFiles: A Starlette class that FastAPI re-exports for convenience
#> • Mounting: Adding an independent application at a specific path
#> • Directory Serving: Automatically maps URL paths to file system paths
#> • Production Use: Essential for serving frontend assets in full-stack applications

#!------------------ Best Practices ------------------!#
#> • Organize by Type: Group files in subdirectories (css/, js/, images/)
#> • Use CDNs: For production, consider CDN for better performance
#> • Security: Never expose sensitive files in static directories
#> • Cache Headers: StaticFiles automatically sets appropriate cache headers
#> • Mount Order: Mount static files after defining API routes to avoid conflicts

#!------------------ Real-World Use Cases ------------------!#
#> • Single Page Applications: Serve your React/Vue/Angular app
#> • Documentation: Host API documentation or user guides
#> • Media Files: Serve user-uploaded images or documents
#> • Admin Panels: Serve admin dashboard HTML/CSS/JS
#!------------------ Browser Environment Note ------------------!#
#> In this interactive tutorial running in your browser (Pyodide), we can't actually access a file system to serve static 
#> files. However, understanding this concept is crucial for building real FastAPI applications in production environments.

## In production, you would:
#> 1. Create a static/ directory in your project
#> 2. Add your HTML, CSS, JS, and other files
#> 3. Mount StaticFiles as shown above
#> 4. Access files via /static/filename
