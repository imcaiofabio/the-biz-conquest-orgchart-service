from fastapi import FastAPI
from app.routers import orgcharts, employees

app = FastAPI()

app.include_router(orgcharts.router, prefix="/orgcharts", tags=["Org Charts"])
app.include_router(employees.router, prefix="/orgcharts", tags=["Employees"])
