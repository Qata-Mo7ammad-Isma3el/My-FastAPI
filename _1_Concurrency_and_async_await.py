# Concurrency and async / await
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Concurrency and async / await  ------------------!#
'''
#> await keyword in Python is used to pause the execution of a task until the result of 
#> another task or operation is ready. It's a key part of Python's asynchronous programming,
#> allowing for non-blocking, concurrent execution of I/O-bound tasks.
'''
import asyncio
# asynchronous function
async def fun():
    print("Hello")
    await asyncio.sleep(1)  # Simulate an asynchronous task
    print("World")
asyncio.run(fun()) # calling fun()
'''
Output
Hello
World
'''

'''
#> • Explanation:
#> • await asyncio.sleep(1) pauses the execution for 1 second without blocking other tasks,
#>   allowing the event loop to run other asynchronous operations.
#> • After the pause, print("World") executes, demonstrating the non-blocking behavior enabled by await.

#> • Syntax: await <expression>
#> • Parameters:
#> • expression: An awaitable object, such as a coroutine, an asynchronous function, or any object that supports 
#> • asynchronous operations (e.g., asyncio.sleep(), a Future object). Returns:
#>   • It returns the result of the awaited task or coroutine once it has finished executing.
'''

#!------------------ await Examples  ------------------!#
'''
#> Example 1: Mutiple coroutines with await
#> This example demonstrates how to run two tasks concurrently using Python's asyncio library.
'''
import asyncio

async def task_1():
    print("Task 1 started")
    await asyncio.sleep(2)  # Simulate a 2-second task
    print("Task 1 completed")

async def task_2():
    print("Task 2 started")
    await asyncio.sleep(1)  # Simulate a 1-second task
    print("Task 2 completed")

async def main():
    await asyncio.gather(task_1(), task_2())  # Run both tasks concurrently

asyncio.run(main())
'''
Output

Task 1 started
Task 2 started
Task 1 completed
Task 2 completed

#> Explanation: task_1() and task_2() start together with asyncio.gather(). Since task_2 waits 1 second and task_1 
#> waits 2 seconds, Task 2 finishes first, which is why it completes before Task 1 in the output.
'''


#!------------------ Concurrency and async / await in fastapi  ------------------!#
#> If you are using third party libraries that tell you to call them with await, like:
# esults = await some_library()
#> Then, declare your path operation functions with async def like:


# @app.get('/')
# async def read_results():
#     results = await some_library()
#     return results
#! Note: You can only use await inside of functions created with async def.