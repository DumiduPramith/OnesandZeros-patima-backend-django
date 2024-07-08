import os

from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.openapi.utils import get_openapi
from api.v1.status.endpoints import router as status_router


class CommonResponse(BaseModel):
    status: str
    message: str


app = FastAPI(
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc",
)


@app.get("/", response_model=CommonResponse)
async def root():
    return CommonResponse(status="success", message="Hello")

@app.get("/api/v1/openapi.json", include_in_schema=False)
async def get_open_api_v1():
    return Response(content=get_openapi(app, "/api/v1"))

app.include_router(status_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    from pathlib import Path
    from dotenv import load_dotenv

    env_path = Path('') / '.env'
    load_dotenv(dotenv_path=env_path)
    env = os.getenv("ENV")
    if env == "dev":
        uvicorn.run(app, host="0.0.0.0", port=8001, reload=True)
    else:
        uvicorn.run(app, host="0.0.0.0", port=8001)
