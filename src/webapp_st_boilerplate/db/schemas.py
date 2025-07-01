from datetime import datetime

from pydantic import BaseModel, field_validator


class EntityBase(BaseModel):
    entityName: str


class EntityCreate(EntityBase):
    pass


class EntityPandas(EntityBase):
    id: int

    @field_validator("id", mode="before")
    def cast_int(cls, v):
        return int(v)


class UserBase(BaseModel):
    name: str
    email: str
    password: str
    role: str
    disabled: bool
    lastLogin: datetime | None = None
    createdDate: datetime | None = None
    updatedDate: datetime | None = None


class UserCreate(UserBase):
    pass


class UserPandas(UserBase):
    id: int
    entityId: int
    lastLogin: str
    createdDate: str
    updatedDate: str

    @field_validator("id", "entityId", mode="before")
    def cast_int(cls, v):
        return int(v)

    @field_validator("lastLogin", "createdDate", "updatedDate", mode="before")
    def cast_date(cls, v):
        if v is not None:
            return datetime.strftime(v, "%Y-%m-%d %H:%M:%S")
        else:
            return None
