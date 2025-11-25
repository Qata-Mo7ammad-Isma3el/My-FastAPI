# SQL Databases with SQLModel
#> explanations
#! headers, Notes
## sub-headers
#? Questions 
#code: code blocks
#// discarded lines

#!------------------ Theory ------------------!#
#> SQLModel is a library created by the same author as FastAPI, designed specifically to work seamlessly with FastAPI
#> applications that need SQL databases. It combines the power of SQLAlchemy (for database operations) with Pydantic 
#> (for data validation).

## 1. Multiple Models Pattern for Security
#> The official FastAPI approach uses multiple models to enhance security and API design:
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select
from contextlib import asynccontextmanager



#> 1.1 Base Model with Shared Fields:
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)

#> 1.2 Table Model for Database:
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str

#> 1.3 Public Model for API Responses:
class HeroPublic(HeroBase):
    id: int  # Always present in responses

#> 1.4 Create Model for Input Validation:
class HeroCreate(HeroBase):
    secret_name: str  # Required for creation

#> 1.5 Update Model for Partial Updates:
class HeroUpdate(SQLModel):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None

### Key Field Configurations:
#> • primary_key=True: Marks the field as the table's primary key
#> • index=True: Creates a database index for faster queries
#> • default=None: Allows the database to auto-generate values (especially for IDs)


## 2. Database Engine Setup:

sqlite_file_name = "./DB/my_database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

## 3. Database Session Management:

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

## 4. Database Table Creation:

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    print("Database initialized!")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)

#! discarded lines (THE OLD WAY)
#// @app.on_event("startup")
#// def on_startup():
#//     create_db_and_tables()

## CRUD Operations with Multiple Models
### Create Operation with Security:
@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep):
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero  #> Returns HeroPublic (no secret_name)

### Read Operations with Public Models:

#> Read multiple with pagination - returns public data only
@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes( session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100 ):
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes  #> Automatically filtered to HeroPublic

#> Read single by ID - no secret data exposed
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

### Update Operation with Partial Updates:

@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep):
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    #> Only update fields that were actually sent
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)  #> SQLModel's update method
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db

#> Delete Operation:

@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}
#!------------------ Key Concepts ------------------!#
#> • Multiple Models Pattern: Use different models for different purposes (security, validation)
#> • Table Models: Classes with table=True represent database tables (Hero)
#> • Data Models: Classes without table=True are for API contracts (HeroPublic, HeroCreate)
#> • Model Inheritance: Use base classes to share common fields (HeroBase)
#> • Response Models: Use response_model to control what data is returned to clients
#> • Partial Updates: Use exclude_unset=True to update only provided fields
#> • Database Engine: Manages database connections and should be created once
#> • Sessions: Handle individual transactions and should be injected per request
#> • Dependency Injection: Use Depends() to inject database sessions into endpoints
#> • Query Builder: Use select() for complex database queries
#> • Pagination: Implement with offset and limit parameters

#!------------------ Best Practices ------------------!#
#> • Multiple Models for Security: Never expose sensitive data like secret_name in public APIs
#> • Use Response Models: Always specify response_model to control API responses
#> • Model Inheritance: Use base models to avoid duplicating field definitions
#> • Partial Updates: Use exclude_unset=True for PATCH operations to update only provided fields
#> • Primary Key Required: Every table model must have a primary key field
#> • Session Per Request: Use dependency injection for database sessions to ensure thread safety
#> • Proper Error Handling: Always check if records exist before operations
#> • Database Startup: Create tables during application startup with @app.on_event("startup")
#> • Connection Arguments: Use check_same_thread=False for SQLite with FastAPI
#> • Query Limits: Always limit query results to prevent performance issues
#> • Transaction Management: Use session.commit() to save changes and session.refresh() to get updated data



