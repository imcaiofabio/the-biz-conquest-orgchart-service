from sqlalchemy.orm import Session
from app import models, schemas

def create_orgchart(db: Session, orgchart: schemas.OrgChartCreate):
    db_org = models.OrgChart(name=orgchart.name)
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

def get_orgcharts(db: Session):
    return db.query(models.OrgChart).all()
