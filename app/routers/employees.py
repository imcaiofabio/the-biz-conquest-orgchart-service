from fastapi import APIRouter, Depends, Path, HTTPException
from sqlalchemy.orm import Session
from app import schemas
from app.crud import employees
from app.db import SessionLocal
from app import models

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{org_id}/employees", response_model=schemas.EmployeeOut)
def create_employee(org_id: int, emp: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    return employees.create_employee(db, org_id, emp)

@router.get("/{org_id}/employees", response_model=list[schemas.EmployeeOut])
def list_employees(org_id: int, db: Session = Depends(get_db)):
    return employees.get_employees(db, org_id)

@router.get("/{org_id}/employees/{employee_id}", response_model=schemas.EmployeeOut)
def get_employee_from_org(org_id: int, employee_id: int, db: Session = Depends(get_db)):
    emp = employees.get_employees(db, org_id, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@router.put("/{org_id}/employees/{employee_id}", response_model=schemas.EmployeeOut)
def update_employee(org_id: int, employee_id: int, emp_update: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    emp = employees.update_employee(db, org_id, employee_id, emp_update)
    if not emp:
        raise HTTPException(status_code=404, detail="Org or Employee not found")
    return emp

@router.delete("/{org_id}/employees/{employee_id}")
def delete_employee(org_id: int, employee_id: int, db: Session = Depends(get_db)):
    return employees.delete_employee_with_reassignment(db, org_id, employee_id)

@router.get("/{org_id}/employees/{employee_id}/direct_reports", response_model=list[schemas.EmployeeOut])
def get_direct_reports(org_id: int, employee_id: int, db: Session = Depends(get_db)):
    emp = employees.get_employees(db, org_id, employee_id)

    if not emp:
        raise HTTPException(status_code=404, detail="Org or Employee not found")

    return emp.direct_reports

@router.put("/{org_id}/employees/{employee_id}/promote", response_model=schemas.EmployeeOut)
def promote_to_ceo(org_id: int, employee_id: int, db: Session = Depends(get_db)):
    return employees.promote_employee_to_ceo(db, org_id, employee_id)