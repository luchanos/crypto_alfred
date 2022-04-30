import pydantic
from pydantic import typing


class ExhangeData(pydantic.BaseModel):
    asset_id: str
    name: str
    price_usd: typing.Optional[float]
