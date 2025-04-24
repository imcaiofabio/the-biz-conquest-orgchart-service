from pydantic import BaseModel
from typing import Optional, List

class OrgChartCreate(BaseModel):
    name: str

class OrgChartOut(BaseModel):
    id: int
    name: str
    class Config:
        orm_mode = True

class EmployeeBase(BaseModel):
    name: str
    title: str
    manager_id: Optional[int]

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeOut(EmployeeBase):
    id: int
    org_id: int
    class Config:
        orm_mode = True
