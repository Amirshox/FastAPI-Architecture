from pydantic import BaseModel, validator


class UserBaseSchema(BaseModel):
    username: str
    first_name: str
    last_name: str


class UserCreateSchema(UserBaseSchema):
    password: str


class UserUpdateSchema(UserBaseSchema):
    pass


class UserListSchema(UserBaseSchema):
    id: int


class UserDetailSchema(UserBaseSchema):
    id: int


class UserUpdatePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    re_new_password: str

    # validate passwords match
    @validator("re_new_password")
    def passwords_match(cls, v, values):
        if "new_password" in values and v != values["new_password"]:
            raise ValueError("passwords do not match")
        return v
