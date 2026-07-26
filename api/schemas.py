from pydantic import BaseModel, ConfigDict


class SymbolOut(BaseModel):
    code: str
    name: str
    sector: str

    model_config = ConfigDict(from_attributes=True)

