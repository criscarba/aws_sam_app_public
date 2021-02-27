from pydantic import BaseModel, ValidationError, validator, AnyUrl, Field

class payload_format(BaseModel):
    table: str
    id: int