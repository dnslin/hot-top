from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.api_v1.api import api_router
from fastapi.middleware.cors import CORSMiddleware
from app.core.scheduler import Scheduler
from app.models.topic import Base
from app.db.session import engine

# 创建调度器实例
scheduler = Scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时执行
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # 启动调度器
    scheduler.start(interval_seconds=settings.CRAWLER_INTERVAL)

    yield

    # 关闭时执行
    scheduler.stop()


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan,
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 包含API路由
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
