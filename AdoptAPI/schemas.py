from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime

class Pet(BaseModel):
    id: int
    name: str = Field(..., min_length = 1, max_length = 50)
    age: int = Field(..., ge=0)
    type: str = Field(..., min_length = 1, max_length = 50)
    adopted: bool = Field(default=False)

class Person(BaseModel):
    id: int
    name: str = Field(..., min_length = 1, max_length = 100)
    email: str = Field(..., pattern=r'^\S+@\S+\.\S+$')
    phone: str = Field(..., min_length = 9)

# --- nueva clase para solicitudes de adopción ---
class RequestStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class AdoptionRequest(BaseModel):
    id: int
    person_id: int
    pet_id: int
    status: RequestStatus = Field(default=RequestStatus.PENDING)
    date: datetime = Field(default_factory=datetime.now)