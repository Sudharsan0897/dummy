from sqlalchemy import Column, Integer, String
from database import Base


class Branch(Base):
    __tablename__ = "branch"

    id = Column(Integer, primary_key=True, index=True)
    branch_name = Column(String(100), nullable=False, unique=True)
    branch_code = Column(Integer, nullable=False, unique=True)
    address = Column(String(255), nullable=False)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    pincode = Column(Integer, nullable=False)
    contact_person = Column(String(100), nullable=False)
    phone = Column(Integer, nullable=False)
    email = Column(String(100), nullable=False)
