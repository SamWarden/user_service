from pydantic import BaseModel


class SetUserUsernameData(BaseModel):
    username: str


class SetUserFullNameData(BaseModel):
    first_name: str
    last_name: str
    middle_name: str | None
