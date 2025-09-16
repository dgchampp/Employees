from typing import Optional
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pymongo.errors import DuplicateKeyError
from ..database import db
from ..models.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse, PaginatedEmployeeResponse
from ..auth.dependencies import get_current_user
from .utils import employee_helper, validate_pagination

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/search", response_model=PaginatedEmployeeResponse)
async def search_by_skill(skill: str, page: int = 1, size: int = 10):
    try:
        skip = validate_pagination(page, size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Case-insensitive exact match using regex
    query = {"skills": {"$regex": f"^{skill}$", "$options": "i"}}
    cursor = db.employees.find(query).sort("joining_date", -1).skip(skip).limit(size)
    items = [employee_helper(doc) async for doc in cursor]
    total = await db.employees.count_documents(query)
    return {"total": total, "page": page, "size": size, "items": items}

@router.get("/avg-salary")
async def avg_salary_by_dept():
    pipeline = [{"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}}]
    cursor = db.employees.aggregate(pipeline)
    out = []
    async for doc in cursor:
        out.append({"department": doc["_id"], "avg_salary": round(doc["avg_salary"])})
    return out


@router.post("/", status_code=201, response_model=EmployeeResponse)
async def create_employee(emp: EmployeeCreate, current_user=Depends(get_current_user)):
    doc = emp.dict()

    doc["joining_date"] = datetime.combine(doc["joining_date"], datetime.min.time())
    try:
        res = await db.employees.insert_one(doc)
    except DuplicateKeyError:
        raise HTTPException(status_code=409, detail="employee_id already exists")
    new_doc = await db.employees.find_one({"_id": res.inserted_id})
    return employee_helper(new_doc)


@router.get("/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: str):
    doc = await db.employees.find_one({"employee_id": employee_id})
    if not doc:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee_helper(doc)


@router.put("/{employee_id}", response_model=EmployeeResponse)
async def update_employee(
    employee_id: str, 
    emp: EmployeeUpdate, 
    current_user=Depends(get_current_user)
):
    update_doc = {k: v for k, v in emp.dict().items() if v is not None}
    if "joining_date" in update_doc:
        update_doc["joining_date"] = datetime.combine(update_doc["joining_date"], datetime.min.time())
    if not update_doc:
        raise HTTPException(status_code=400, detail="No fields provided for update")
    
    res = await db.employees.update_one({"employee_id": employee_id}, {"$set": update_doc})
    if res.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    updated = await db.employees.find_one({"employee_id": employee_id})
    return employee_helper(updated)


@router.delete("/{employee_id}")
async def delete_employee(employee_id: str, current_user=Depends(get_current_user)):
    res = await db.employees.delete_one({"employee_id": employee_id})
    if res.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "deleted"}


@router.get("/", response_model=PaginatedEmployeeResponse)
async def list_employees(
    department: Optional[str] = None,
    page: int = 1,
    size: int = 10,
):
    try:
        skip = validate_pagination(page, size)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    query = {}
    if department:
        query["department"] = department
    
    cursor = db.employees.find(query).sort("joining_date", -1).skip(skip).limit(size)
    items = [employee_helper(doc) async for doc in cursor]
    total = await db.employees.count_documents(query)
    return {"total": total, "page": page, "size": size, "items": items}


