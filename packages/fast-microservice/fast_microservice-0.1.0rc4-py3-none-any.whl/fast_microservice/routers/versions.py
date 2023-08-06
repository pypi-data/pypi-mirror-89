from fastapi import APIRouter
from pydantic import BaseModel

from fast_microservice.settings.globals import APP_VERSION

router = APIRouter()


class VersionResult(BaseModel):
    """ Version response model. """

    version: str


@router.get("/version", response_model=VersionResult, name="version")
def get_version() -> VersionResult:
    """ Version of the application."""
    return VersionResult(version=APP_VERSION)
