from pydantic import BaseModel


class Tag(BaseModel):
    """Represents a named entity's type and value.
    """
    tagType: str
    value: str


class StrPredWithConf(BaseModel):
    value: str
    confidence: float
