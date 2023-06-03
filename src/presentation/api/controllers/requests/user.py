from pydantic import BaseModel


class SetUserUsernameData(BaseModel):
    username: str
