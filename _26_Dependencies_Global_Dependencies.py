# Dependencies - Global Dependencies
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines
#!------------------ Theory ------------------!#
#> For some types of applications you might want to add dependencies to the whole application.
#> Similar to the way you can add dependencies to the path operation decorators, you can add them to the FastAPI application.
#> In that case, they will be applied to all the path operations in the application:

#code: app = FastAPI(dependencies=[Depends(verify_token), Depends(verify_key)])
#> And all the ideas in the section about adding dependencies to the path operation decorators still apply, but in this case,

#> to all of the path operations in the app.
#> Dependencies for Groups of Path Operations
#> Later, when reading about how to structure bigger applications (Bigger Applications - Multiple Files), possibly with 
#> multiple files, you will learn how to declare a single dependencies parameter for a group of path operations.
#!------------------ Key Concepts ------------------!#
#> • Global Dependencies: Dependencies applied to the entire FastAPI application
#> • Application-wide: Affects all path operations automatically
#> • No Duplication: Eliminates the need to add the same dependency to every endpoint

#!------------------ Best Practices ------------------!#
#> • Use global dependencies for cross-cutting concerns like authentication
#> • Keep global dependencies lightweight to avoid performance overhead
#> • Consider using sub-dependencies for complex global logic
#> • Document global dependencies clearly for team members


