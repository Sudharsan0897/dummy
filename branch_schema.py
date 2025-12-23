# Add to your existing schemas.py
from typing import List

from pydantic import BaseModel, ConfigDict

class BranchCreate(BaseModel):
    branch_name: str
    branch_code: int
    address: str
    city: str
    state: str
    pincode: int
    contact_person: str
    phone: int
    email: str

class BranchResponse(BaseModel):
    id: int
    branch_name: str
    branch_code: int
    address: str
    city: str
    state: str
    pincode: int
    contact_person: str
    phone: int
    email: str

    class Config:
        from_attributes = True


class BranchListResponse(BaseModel):
    branches: List[BranchResponse]
    total: int
