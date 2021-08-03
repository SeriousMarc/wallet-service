"""
Run Application Logic
"""
import uvicorn

from fastapi import FastAPI, Request, HTTPException
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from wallet_service.routes import router
from wallet_service.utils import db_hearbeat, init_models, drop_models


app = FastAPI()
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    await init_models()
    await db_hearbeat()


# @app.on_event("shutdown")
# async def shutdown_event():
#     await drop_models()


# @app.middleware('http')
# async def validation_middleware(request: Request, call_next):
#     try:
#         return await call_next(request)
#     except ValidationError as e:
#         return HTTPException(
#             status_code=422,
#             detail=str(e),
#             headers={"X-Error": "ValidationError"}
#         )
#     except SQLAlchemyError as e:
#         return HTTPException(
#             status_code=500,
#             detail=str(e),
#             headers={"X-Error": "DB Validation Error"}
#         )

if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='127.0.0.1')
