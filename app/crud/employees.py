from sqlalchemy.orm import Session
from app import models, schemas
from fastapi import HTTPException

def create_employee(db: Session, org_id: int, employee: schemas.EmployeeCreate):
    db_emp = models.Employee(**employee.dict(), org_id=org_id)
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp

def get_employees(db: Session, org_id: int, employee_id: int = None):
    if not employee_id:
        return db.query(models.Employee).filter(models.Employee.org_id == org_id).all()
    return db.query(models.Employee).filter(models.Employee.org_id == org_id, models.Employee.id == employee_id).first()

def update_employee(db: Session, org_id: int, employee_id: int, employee: schemas.EmployeeCreate):
    db_emp = get_employees(db, org_id, employee_id)
    if db_emp:
        db_emp.name = employee.name
        db_emp.title = employee.title
        db_emp.manager_id = employee.manager_id
        db.commit()
        db.refresh(db_emp)
    return db_emp

def delete_employee_with_reassignment(db: Session, org_id: int, employee_id: int):
    emp = get_employees(db, org_id, employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")

    if emp.manager_id is None:
        raise HTTPException(status_code=400, detail="Cannot delete CEO")

    for report in emp.direct_reports:
        report.manager_id = emp.manager_id

    db.delete(emp)
    db.commit()
    return {"detail": "Employee deleted and reports reassigned"}

def promote_employee_to_ceo(db: Session, org_id: int, employee_id: int):
    current_ceo = db.query(models.Employee).filter(
        models.Employee.org_id == org_id,
        models.Employee.manager_id == None
    ).first()
    if not current_ceo:
        raise HTTPException(status_code=404, detail="Current CEO not found")

    if current_ceo.id == employee_id:
        raise HTTPException(status_code=400, detail="This employee is already the CEO")

    new_ceo = get_employees(db, org_id, employee_id)
    if not new_ceo:
        raise HTTPException(status_code=404, detail="Employee not found")

    new_ceo.manager_id = None
    current_ceo.manager_id = new_ceo.id

    db.commit()
    db.refresh(new_ceo)
    return new_ceo