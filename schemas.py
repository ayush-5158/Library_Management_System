from pydantic import BaseModel
from typing import Optional

class Books(BaseModel):
    title : str
    author : str
    is_available : str
    assigned_to : str

class BookUpdate(BaseModel):
    title : Optional[str] = None
    author : Optional[str] = None
    is_available: Optional[str] = None
    assigned_to : Optional[str] = None