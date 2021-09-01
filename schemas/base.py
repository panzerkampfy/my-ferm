from functools import partial

from utils import snake2camel
from pydantic.main import BaseConfig, BaseModel


class APIModel(BaseModel):
    class Config(BaseConfig):
        orm_mode = True
        allow_population_by_field_name = True
        alias_generator = partial(snake2camel, start_lower=True)


class GenericHTTPError(APIModel):
    """
    A generic model for HTTP errors. Consists of error status code and detailed message.
    """

    status_code: int
    detail: str
