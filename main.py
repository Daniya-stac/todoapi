import uvicorn
from fastapi import FastAPI
from backend.routers import handles
from contextlib import asynccontextmanager
from starlette.middleware.cors import CORSMiddleware
from backend.database.conf import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(title="Todo API",
              lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(handles.router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
