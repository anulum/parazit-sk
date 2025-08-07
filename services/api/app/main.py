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

# --- Paths ---
DATA_PATH = Path(__file__).parent.parent / "data/seed"

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
async def read_root():
    return {"status": "ok", "message": "Welcome to Parazit.sk API"}

# --- Cases Endpoints ---
@app.get("/api/v1/cases", response_model=List[CaseSummary], tags=["Cases"])
async def get_all_cases():
    """Lists all available cases with summary data."""
    cases = []
    # Simplified to find any .yaml file in the seed directory for now
    for f in DATA_PATH.glob('*.yaml'):
        try:
            with f.open('r', encoding='utf-8') as stream:
                data = yaml.safe_load(stream)
                # Basic check if it's a case file
                if 'title' in data and 'severity' in data:
                    cases.append(CaseSummary(**data))
        except Exception:
            continue
    return cases

@app.get("/api/v1/cases/{case_id}", response_model=CaseDetail, tags=["Cases"])
async def get_case_by_id(case_id: str):
    """Fetches a single case by its ID from the YAML seed files."""
    file_path = DATA_PATH / f"{case_id}.yaml"
    if not file_path.is_file():
        raise HTTPException(status_code=404, detail=f"Case '{case_id}' not found.")
    
    with file_path.open('r', encoding='utf-8') as stream:
        data = yaml.safe_load(stream)
        return CaseDetail(**data)

# --- Persons Endpoints ---
@app.get("/api/v1/persons", response_model=List[Person], tags=["Persons"])
async def get_all_persons():
    """(Simulated) Returns a list of all persons."""
    # This is a mocked response. In the future, it will read from a database or YAML files.
    return [
        Person(id='gasparovic', name='Ivan Gašparovič', birthDate='1941-03-27', function='President SR'),
        Person(id='hascak', name='Jaroslav Haščák', birthDate='1969-08-30', function='Co-owner Penta Investments')
    ]

@app.get("/api/v1/persons/{person_id}", response_model=Person, tags=["Persons"])
async def get_person_by_id(person_id: str):
    """(Simulated) Returns a single person by ID."""
    # Mocked response
    if person_id == 'gasparovic':
        return Person(id='gasparovic', name='Ivan Gašparovič', birthDate='1941-03-27', function='President SR')
    if person_id == 'hascak':
        return Person(id='hascak', name='Jaroslav Haščák', birthDate='1969-08-30', function='Co-owner Penta Investments')
    raise HTTPException(status_code=404, detail=f"Person '{person_id}' not found.")