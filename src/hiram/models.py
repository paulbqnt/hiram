from typing import Optional, Dict, Union
from pydantic import BaseModel, Field, ConfigDict


class Greeks(BaseModel):
    delta: Optional[float] = None
    gamma: Optional[float] = None
    vega: Optional[float] = None
    theta: Optional[float] = None
    rho: Optional[float] = None

    model_config = ConfigDict(
        extra='ignore',
        strict=False
    )

class PricingResult(BaseModel):
    value: float
    greeks: Greeks = Field(default_factory=Greeks)

    def to_json(self) -> Dict[str, Union[float, Dict[str, Optional[float]]]]:
        return {
            "value": self.value,
            "greeks": self.greeks.model_dump()
        }
