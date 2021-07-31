"""
Run Application Logic
"""
import uvicorn

from fastapi import FastAPI

from wallet_service.routes import router
from wallet_service.config import init_models
from wallet_service.utils import db_hearbeat

app = FastAPI()
app.include_router(router)

@app.on_event("startup")
async def startup_event():
    await init_models()
    await db_hearbeat()

if __name__ == '__main__':

    uvicorn.run(app, port=8000, host='127.0.0.1')
