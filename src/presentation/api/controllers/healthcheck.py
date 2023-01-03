from fastapi import APIRouter, status
from fastapi.responses import ORJSONResponse

healthcheck_router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
)


@healthcheck_router.get("/", response_class=ORJSONResponse, status_code=status.HTTP_200_OK)
async def create_user():
    return {"status": "ok"}
