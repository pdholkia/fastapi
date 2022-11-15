from pydantic import BaseModel

class students(BaseModel):
    fname: str
    lname: str
    phone: str
    course: str
    gender: str
    country: str
    state: str
    city: str
    address: str
    vehicle: str
    image: str
