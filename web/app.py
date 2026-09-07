from fastapi import FastAPI
from pydantic import BaseModel
from src.showcase import build_showcase_text, build_showcase_data, DEFAULT_FIELDS
from typing import Optional

app = FastAPI()

class CharacterData(BaseModel):
    name: str
    level: Optional[int] = None
    constellation: Optional[int] = None
    weapon: Optional[str] = None
    artifact_set: Optional[str] = None
    friendship: Optional[int] = None
    talents: Optional[str] = None
    hp: Optional[int] = None
    atk: Optional[int] = None
    defense: Optional[int] = None
    crit: Optional[str] = None
    er: Optional[str] = None
    em: Optional[int] = None
    dmg_bonus: Optional[str] = None

class ShowcaseRequest(BaseModel):
    uid: str
    fields: list[str]

class ShowcaseResponse(BaseModel):
    message: str
    characters: list[CharacterData]



@app.get("/")
def hello_world():
    return {"message": "Hello, World!"}

@app.get("/showcase/{uid}", response_model=ShowcaseResponse, response_model_exclude_none=True)
def get_showcase(uid: str):
    return {
        "message": "Attempting showcase retrieval",
        "characters": build_showcase_data(uid)
    }


@app.post("/showcase", response_model=ShowcaseResponse, response_model_exclude_none=True)
def get_custom_showcase(request: ShowcaseRequest):
    return {
        "message": "Attempting showcase retrieval",
        "characters": build_showcase_data(
            request.uid,
            request.fields
        )
    }