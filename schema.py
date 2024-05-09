# from abc import ABC
from typing import Optional

import pydantic


# class AbstractAdvertisement(pydantic.BaseModel, ABC):
#     title_adv: str
#     owner: str
#
#     @pydantic.field_validator("password")
#     @classmethod
#     def secure_password(cls, v: str) -> str:
#         if len(v) < 8:
#             raise ValueError(f"Minimal length of password is 8")
#         return v


class CreateAdvertisement(pydantic.BaseModel):
    title_adv: str
    description: str
    owner: str


class UpdateAdvertisement(pydantic.BaseModel):
    title_adv: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None