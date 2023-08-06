import typing as t

from pydantic import BaseModel

from bavard.common.pydantics import Tag, StrPredWithConf


class NLUPrediction(BaseModel):
    intent: StrPredWithConf
    tags: t.List[Tag]


class NLUPredictions(BaseModel):
    predictions: t.List[NLUPrediction]
