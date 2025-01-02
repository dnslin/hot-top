from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from typing import AsyncGenerator

# 创建异步引擎
engine = create_async_engine(settings.DATABASE_URL, echo=True)

# 创建异步会话工厂
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# 创建异步会话实例
async_session = async_session_maker


# 异步会话上下文管理器
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
