# Python
from typing import Optional
from enum import Enum

#pydantic
from pydantic import BaseModel
from pydantic import Field

#FastApi
from fastapi import FastAPI
from fastapi import Body, Query, Path


app = FastAPI()

class HairColor(Enum):
    white = "White"
    brown = "Brown"
    black = "Black"



class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
    )
    last_name: str
    age: int = Field(
        gt=0,
        le=115
    )
    hair_color: Optional[HairColor] = Field(default="Black")
    is_married: Optional[bool] = None

    class Config:
        schema_extra = {
            "example":{
                "first_name": "Julián",
                "last_name": "Velandia"
            }
        }


class Location(BaseModel):
    city: str
    state: str

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
        description= "This is a person",
        example= "Julián"
    ),
    age: Optional[int] = Query(
        ...,
        title="Person_age",
        description="This is a person age",
        example = 22
    )
):
    return {name: age}

#Validaciones por path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
      gt=0,
      title= "Person name",
      description= "This is a person",
      example = "1"
      ) #Los 3 puntos significan que es obligatorio
):
    return {person_id: "Exist"}

#validacion request body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title= "Person ID",
        descirption = "Update the person",
        gt =0,
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results