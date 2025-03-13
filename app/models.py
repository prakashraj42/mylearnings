from pydantic import BaseModel

class UserOut(BaseModel):
    username: str
    email: str
    password: str
    is_driver: bool

    class Config:
        from_attributes = True