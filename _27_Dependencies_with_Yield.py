# Dependencies with Yield
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#?------------------ What is Yield? ------------------?#
#> Definition and Usage
#> The yield keyword is used to return a list of values from a function.
#> • Unlike the return keyword which stops further execution of the function, the yield keyword continues 
#>   to the end of the function.
#> When you call a function with yield keyword(s), the return value will be a list of values, one for each yield.

#!------------------ Theory ------------------!#
#> FastAPI supports dependencies that do extra steps after finishing. To do this, use yield instead of return, 
#> and write the extra steps (code) after.

## A Database Dependency with yield
#> You can use this to create a database session and close it after finishing. Only the code prior to and
#> including the yield statement is executed before creating a response:
class DBSession:
    def __init__(self):
        self.connected = True
        self.transaction_count = 0
        print("Database connection established")
    
    def close(self):
        self.connected = False
        print("Database connection closed")

async def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
#> The yielded value is what is injected into path operations and other dependencies. 
#> The code following the yield statement is executed after creating the response but before sending it.

## Execution Flow
#> When you use yield in a dependency:
#> 1. Setup Code: Code before yield runs before the endpoint executes
#> 2. Value Injection: The yielded value is injected into your endpoint
#> 3. Endpoint Execution: Your path operation function runs
#> 4. Response Creation: FastAPI creates the response
#> 5. Cleanup Code: Code after yield runs before sending the response

## Dependencies with yield and try
#> If you use a try block in a dependency with yield, you'll receive any exception that was thrown when using the dependency.
#> You can use except to handle specific exceptions and finally to ensure cleanup always happens:

async def get_db():
    db = DBSession()
    try:
        yield db
    except Exception:
        # Handle any exception that occurred during endpoint execution
        db.rollback()
        raise
    finally:
        # This always runs, even if there was an exception
        db.close()


#!------------------ Key Concepts ------------------!#
#> • Resource Management: Automatically clean up resources like database connections
#> • Exception Handling: Use try/except blocks to handle errors during cleanup
#> • Execution Order: FastAPI ensures cleanup code runs in the correct order for nested dependencies
#> • Context Managers: Yield dependencies work similarly to Python's context managers

#!------------------ Best Practices ------------------!#
#> • Always use yield only once per dependency function
#> • Use try/finally blocks to ensure cleanup code always runs
#> • Handle specific exceptions in except blocks when needed
#> • Re-raise exceptions to maintain proper error handling
#> • Keep setup and cleanup code minimal and focused

#!------------------ Real-World Applications ------------------!#
#> • Database Sessions: Create and close database connections
#> • File Handling: Open and close files safely
#> • Cache Management: Initialize and cleanup cache connections
#> • External API Clients: Setup and teardown HTTP clients
#> • Logging Context: Setup request-specific logging


