from typing import Generic, TypeVar

from pydantic import BaseModel

# TGeneric type variable to accept any structural Pydantic payload model dynamically
T = TypeVar("T")


class StandardResponse(BaseModel, Generic[T]):
    """Global envelope structure for all successful API responses."""
    success: bool = True
    payload: T


class ErrorResponse(BaseModel):
    """Global envelope structure for all error responses."""
    success: bool = False
    detail: str