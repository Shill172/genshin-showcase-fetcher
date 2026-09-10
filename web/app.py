from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from src.showcase import build_showcase_data
from typing import Optional
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.exceptions import ShowcaseNotFoundError, EnkaRequestError

app = FastAPI()

app.mount("/static", StaticFiles(directory="web/static"), name="static")

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

    @field_validator("uid")
    @classmethod
    def validate_uid(cls, value):
        if not value.isdigit():
            raise ValueError("UID must contain only digits")
        if not (9 <= len(value) <= 10):
            raise ValueError("UID must be 9 or 10 digits long")
        return value


class ShowcaseResponse(BaseModel):
    message: str
    characters: list[CharacterData]


@app.get("/")
def read_index():
    return FileResponse("web/templates/index.html")

"""
@app.get("/showcase/{uid}", response_model=ShowcaseResponse, response_model_exclude_none=True)
def get_showcase(uid: str):
    return {
        "message": "Attempting showcase retrieval",
        "characters": build_showcase_data(uid)
    }
"""

@app.post("/showcase", response_model=ShowcaseResponse, response_model_exclude_none=True)
def get_custom_showcase(request: ShowcaseRequest):
    try:
        characters = build_showcase_data(request.uid, request.fields)
    except ShowcaseNotFoundError:
        raise HTTPException(status_code=404, detail=f"No showcase found for UID {request.uid}")
    except EnkaRequestError:
        raise HTTPException(status_code=502, detail="Enka's API is currently unavailable")

    return {
        "message": "Attempting showcase retrieval",
        "characters": characters
    }