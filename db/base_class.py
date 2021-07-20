from sqlalchemy import Column, INTEGER
from sqlalchemy.ext.declarative import as_declarative


@as_declarative()
class Base:
    __name__: str

    id = Column(INTEGER, primary_key=True, autoincrement=True, index=True)
