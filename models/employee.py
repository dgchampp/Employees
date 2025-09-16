from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: float
    joining_date: date
    skills: List[str] = []


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    salary: Optional[float] = None
    joining_date: Optional[date] = None
    skills: Optional[List[str]] = None


class EmployeeResponse(BaseModel):
    id: str
    employee_id: str
    name: str
    department: str
    salary: float
    joining_date: str
    skills: List[str] = []


class PaginatedEmployeeResponse(BaseModel):
    total: int
    page: int
    size: int
    items: List[EmployeeResponse]
