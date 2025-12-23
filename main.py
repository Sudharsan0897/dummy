from argon2 import verify_password
from datetime import datetime, timedelta
from typing import List
from database import get_db
from fastapi import FastAPI, Depends, status
from fastapi import HTTPException
from auth import verify_token
from database import engine, Base
from model import UserDB
from schema import UserCreate, UserLogin, UserResponse, ForgotPasswordRequest, ResetPasswordRequest
from utils import create_access_token, verify_password, hash_password
from sqlalchemy.orm import Session

from branch_schema import BranchCreate, BranchResponse
import branch_crud
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Create tables on startup
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Login/Signup API - Branch API")
@app.get("/")

def root():
    return {"message": "Auth API Ready ✅", "database": "setup_db"}

@app.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    return {"status": "db ok"}


# --------------------------------------------------------------------------------------------Sign up ----------------------------------------------------------------
@app.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if username exists
    existing_user = db.query(UserDB).filter(UserDB.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    # Check if email exists
    existing_email = db.query(UserDB).filter(UserDB.email == user.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already exists")

    # Hash password
    hashed_pw = hash_password(user.password)

    # Create user db model
    new_user = UserDB(
        username=user.username,
        email=user.email,
        branch = user.branch,
        team = user.team,
        hashed_password=hashed_pw,
        role = user.role
    )
    # -------------------------------------------------------------------- Save to DB --------------------------------------------------------------------------
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {'message': 'User created successfully'}


# ----------------------------------------------------------------------Login setup-----------------------------------------------------------------------------
@app.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(
        data={"sub": db_user.username}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


# ---------------------------------------------------------------------LIST USERS---------------------------------------

@app.get("/users/", response_model=List[UserResponse])
def list_users(
        token: str = Depends(verify_token),
        db: Session = Depends(get_db)
):
    users = db.query(UserDB).all()
    return users

# ------------------------------------------------------------------------- GET USER BY ID -------------------------------
@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# ------------------------------------------------------------------------ UPDATE USER ---------------------------------------------
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.username = user_update.username
    db_user.email = user_update.email
    db_user.branch = user_update.branch
    db_user.team = user_update.team
    db_user.role = user_update.role
    db_user.hashed_password = hash_password(user_update.password)
    db.commit()
    db.refresh(db_user)
    return db_user


#  -------------------------------------------------------------------DELETE USER--------------------------------------------------
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}


# --------------------------------------------------------- FORGOT PASSWORD ------------------------------------------------------
@app.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(UserDB.email == request.email).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Email not found")

    reset_token = f"reset_{db_user.id}_{int(datetime.now().timestamp())}"
    db_user.reset_token = reset_token
    db_user.reset_token_expires = datetime.now() + timedelta(hours=1)
    db.commit()

    return {
        "message": "Reset token generated",
        "reset_token": reset_token,
        "expires_in": "1 hour"
    }


# -----------------------------------------------------------------RESET PASSWORD----------------------------------------------------
@app.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    db_user = db.query(UserDB).filter(
        UserDB.reset_token == request.token,
        UserDB.reset_token_expires > datetime.now()
    ).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    db_user.hashed_password = hash_password(request.new_password)
    db_user.reset_token = None
    db_user.reset_token_expires = None
    db.commit()

    return {"message": "Password reset successful"}


# #---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Root
@app.get("/")
def root():
    return {"message": "Branch API Ready ✅"}

@app.post("/branches", response_model=BranchResponse)
def create_branch(branch: BranchCreate, db: Session = Depends(get_db)):
    return branch_crud.create_branch(db, branch)

# Get all branch
@app.get("/branches", response_model=List[BranchResponse])
def list_branches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return branch_crud.get_branches(db, skip, limit)

# Get branch by id
@app.get("/branches/{branch_id}", response_model=BranchResponse)
def get_branch(branch_id: int, db: Session = Depends(get_db)):
    branch = branch_crud.get_branch(db, branch_id)
    if not branch:
        raise HTTPException(status_code=404, detail="Branch not found")
    return branch

# Update branch
@app.put("/branches/{branch_id}", response_model=BranchResponse)
def update_branch(branch_id: int, branch: BranchCreate, db: Session = Depends(get_db)):
    updated = branch_crud.update_branch(db, branch_id, branch)
    if not updated:
        raise HTTPException(status_code=404, detail="Branch not found")
    return updated

# Delete branch
@app.delete("/branches/{branch_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_branch(branch_id: int, db: Session = Depends(get_db)):
    deleted = branch_crud.delete_branch(db, branch_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Branch not found")
    return None
# # ------------------------------------------------------------------------------------------------------------------