# Background Tasks
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> Background tasks are operations that run after returning a response to the client. This is useful for operations that 
#> don't need to block the response, such as:
#> • Email notifications: Sending emails can take several seconds, so you can return the response immediately and send the 
#>   email in the background
#> • Data processing: Processing uploaded files or computing statistics that the user doesn't need to wait for
#> • Logging: Writing detailed logs or analytics data
#> • External API calls: Making non-critical requests to third-party services

## Using BackgroundTasks
#> FastAPI provides BackgroundTasks to easily add background operations. Simply:
#> 1. Import BackgroundTasks from fastapi
#> 2. Add a parameter with type BackgroundTasks to your path operation
#> 3. Use background_tasks.add_task() to add functions to run in the background

from fastapi import BackgroundTasks, FastAPI

app = FastAPI()

def write_log(message: str):
    with open("log.txt", mode="a") as log:
        log.write(message)

@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_log, f"Notification sent to {email}\n")
    return {"message": "Notification sent in the background"}

#? How It Works
#> 1. FastAPI creates a BackgroundTasks object automatically
#> 2. You add tasks using .add_task(function, arg1, arg2, kwarg1="value")
#> 3. The response is sent to the client immediately
#> 4. After the response is sent, all background tasks execute in order

## Task Functions
### Background task functions can be:
#> • Regular functions (def)
#> • Async functions (async def)
#> • Functions with any number of arguments
#> • Functions with keyword arguments

def send_email(email: str, subject: str, body: str):
    # Simulate sending email
    print(f"Sending to {email}: {subject}")

@app.post("/register")
async def register_user(username: str, email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, email, subject="Welcome!", body=f"Hello {username}!")
    return {"message": "User registered"}

## Multiple Background Tasks
#> You can add multiple background tasks to the same request. They will execute in the order they were added:

@app.post("/process-order/{order_id}")
async def process_order(order_id: int, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, "customer@example.com", "Order Confirmed", "Thanks!")
    background_tasks.add_task(update_inventory, order_id)
    background_tasks.add_task(notify_shipping, order_id)
    return {"message": "Order processed"}

#!------------------ Key Concepts ------------------!#
#> • BackgroundTasks: A FastAPI object that manages background operations
#> • add_task(): Method to add a function to be executed after the response
#> • Non-blocking: The client receives the response immediately without waiting for background tasks
#> • Sequential Execution: Background tasks run in the order they were added
#> • Dependency Injection: BackgroundTasks works seamlessly with FastAPI's dependency system

#!------------------ Best Practices ------------------!#
#> • Use for non-critical operations: Background tasks run after the response, so they shouldn't affect the main functionality
#> • Keep tasks lightweight: For heavy computations, consider dedicated task queues like Celery
#> • Handle errors gracefully: Background tasks that fail won't affect the response, but implement proper error handling
#> • Don't rely on shared state: Background tasks run after the response context, so be careful with database connections
#> • Combine with dependencies: Use background tasks in dependencies for shared background operations