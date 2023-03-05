from typing import Optional
from pydantic import BaseModel, Field
from yahooquery import Ticker
from typing import Dict
from uuid import uuid4, UUID


class Bond(BaseModel):
    principal: float
    interest: float
    id_: UUID = Field(default_factory=uuid4)
