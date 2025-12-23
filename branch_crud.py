from sqlalchemy.orm import Session
from branch_model import Branch
from branch_schema import BranchCreate

def create_branch(db: Session, branch: BranchCreate):
    db_branch = Branch(**branch.dict())
    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch
def get_branch(db: Session, branch_id: int):
    return db.query(Branch).filter(Branch.id == branch_id).first()

def get_branches(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Branch).offset(skip).limit(limit).all()

def update_branch(db: Session, branch_id: int, branch_data: BranchCreate):
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        return None
    for key, value in branch_data.dict().items():
        setattr(db_branch, key, value)
    db.commit()
    db.refresh(db_branch)
    return db_branch

def delete_branch(db: Session, branch_id: int):
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        return None
    db.delete(db_branch)
    db.commit()
    return db_branch
