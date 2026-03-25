from fastapi import FastAPI
from api.routes import router
from database.init_db import init_db
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from background_simulator import run_simulator
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the simulator when the app spins up
    task = asyncio.create_task(run_simulator())
    yield
    # Shutdown simulator
    task.cancel()

app = FastAPI(title="Women Safety IoT Backend", lifespan=lifespan)

init_db()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "Backend running"}
