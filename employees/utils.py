from typing import Dict, Any
from datetime import datetime


def employee_helper(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document to Employee response format"""
    jd = doc.get("joining_date")
    if isinstance(jd, datetime):
        jd = jd.date().isoformat()

    return {
        "id": str(doc["_id"]),
        "employee_id": doc["employee_id"],
        "name": doc["name"],
        "department": doc["department"],
        "salary": doc["salary"],
        "joining_date": jd,
        "skills": doc.get("skills", []),
    }


def validate_pagination(page: int, size: int):
    if page < 1 or size < 1:
        raise ValueError("page and size must be positive integers")
    return max(0, (page - 1) * size)
