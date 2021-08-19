from fastapi import HTTPException
from starlette import status


class ValidationError(ValueError):
    def __init__(self, detail: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class NotFoundError(Exception):
    def __init__(self, detail: str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=detail
        )


class ForbiddenError(Exception):
    def __init__(self, detail: str):
        self.detail = detail
