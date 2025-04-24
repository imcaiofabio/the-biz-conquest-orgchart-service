from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base

class OrgChart(Base):
    __tablename__ = "org_charts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    employees = relationship("Employee", back_populates="org")

class Employee(Base):
    __tablename__ = "employees"
    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey("org_charts.id"), nullable=False)
    name = Column(String, nullable=False)
    title = Column(String, nullable=False)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    org = relationship("OrgChart", back_populates="employees")
    manager = relationship("Employee", remote_side=[id], backref="direct_reports")
