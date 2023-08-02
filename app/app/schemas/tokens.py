from typing import Optional

from pydantic import BaseModel


class token(BaseModel):
    access_token: str
    token_type: str


class tokenPayload(BaseModel):
    sub: Optional[int] = None
