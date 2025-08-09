from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import List
import yaml

app = FastAPI(
    title="Parazit.sk API",
    description="API for accessing data about Slovak corruption cases.",
    version="0.1.0"
)

DATA_PATH = Path(__file__).parent.parent.parent / "data/seed"

# --- Pydantic Models ---
class CaseSummary(BaseModel):
    id: str
    title: str
    summary: str
    severity: int

class CaseDetail(CaseSummary):
    status: str
    damageEur: int | None = None
    sourceUrls: List[str] = []

class Person(BaseModel):
    id: str
    name: str
    birthDate: str | None = None
    function: str | None = None

# --- API Endpoints ---

@app.get("/", tags=["Status"])
def read_root():
    return {"status": "ok", "message": "Welcome to Parazit.sk API"}

# --- Cases Endpoints ---
@app.get("/api/v1/cases", response_model=List[CaseSummary], tags=["Cases"])
def get_all_cases():
    cases = []
    for f in DATA_PATH.glob('*.yaml'):
        if not f.name.startswith('person_'):
            with f.open('r', encoding='utf-8') as stream:
                data = yaml.safe_load(stream)
                cases.append(CaseSummary(**data))
    return cases

@app.get("/api/v1/cases/{case_id}", response_model=CaseDetail, tags=["Cases"])
def get_case_by_id(case_id: str):
    file_path = DATA_PATH / f"{case_id}.yaml"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found.")
    with file_path.open('r', encoding='utf-8') as stream:
        data = yaml.safe_load(stream)
        return CaseDetail(**data)

# --- Persons Endpoints ---
@app.get("/api/v1/persons", response_model=List[Person], tags=["Persons"])
def get_all_persons():
    persons = []
    for f in DATA_PATH.glob('person_*.yaml'):
        with f.open('r', encoding='utf-8') as stream:
            data = yaml.safe_load(stream)
            persons.append(Person(**data))
    return persons

@app.get("/api/v1/persons/{person_id}", response_model=Person, tags=["Persons"])
def get_person_by_id(person_id: str):
    file_path = DATA_PATH / f"person_{person_id}.yaml"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found.")
    with file_path.open('r', encoding='utf-8') as stream:
        data = yaml.safe_load(stream)
        return Person(**data)
