from dataclasses import dataclass

from fastapi import APIRouter, status

healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@dataclass(frozen=True)
class OkStatus:
    status: str = "ok"


OK_STATUS = OkStatus()


@healthcheck_router.get("/", status_code=status.HTTP_200_OK)
async def create_user() -> OkStatus:
    return OK_STATUS
