from fastapi import APIRouter

from fast_microservice.settings.globals import DEBUG

router = APIRouter()


@router.get("/error", name="error")
def get_error():
    """Raise ZeroDivisionError for debugging purposes."""
    if DEBUG:
        raise ZeroDivisionError("This is a debugging feature.")
