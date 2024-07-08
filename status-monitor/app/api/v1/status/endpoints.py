from fastapi import APIRouter, Response, status

from .models import StatusResponse

router = APIRouter()


@router.get("/check-connection", response_model=StatusResponse)
async def check_connection(response: Response):
    response.status_code = status.HTTP_200_OK
    return StatusResponse(status="success", message="connection-ok")
