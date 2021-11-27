# Python
from typing import Optional

#pydantic
from pydantic import BaseModel

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()

class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"Hello": "World"}

# Request and Response Body

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# validaciones: query parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title= "Person name",
        description= "This is a person"
    ),
    age: Optional[int] = Query(
        ...,
        title="Person_age",
        description="This is a person age"
    )
):
    return {name: age}

#Validaciones por path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(...,
                          gt=0,
                          title= "Person name",
                          description= "This is a person"
                          ) #Los 3 puntos significan que es obligatorio
):
    return {person_id: "Exist"}