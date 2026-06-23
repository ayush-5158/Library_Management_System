from database import Base
from sqlalchemy import Column,Integer,String

class Books(Base):
    __tablename__="books"

    id = Column(Integer,index=True,primary_key=True)
    title = Column(String(255),unique=True)
    author = Column(String(255))
    is_available = Column(String(255))
    assigned_to = Column(String(255))

