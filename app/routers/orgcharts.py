from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas
from app.crud import orgcharts
from app.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.OrgChartOut)
def create_orgchart(org: schemas.OrgChartCreate, db: Session = Depends(get_db)):
    return orgcharts.create_orgchart(db, org)

@router.get("/", response_model=list[schemas.OrgChartOut])
def list_orgcharts(db: Session = Depends(get_db)):
    return orgcharts.get_orgcharts(db)
