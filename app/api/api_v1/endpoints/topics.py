from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.models.topic import Topic
from typing import List
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


class TopicResponse(BaseModel):
    id: int
    title: str
    url: str
    source: str
    rank: int
    hot_value: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


@router.get("/", response_model=List[TopicResponse])
async def get_topics(
    skip: int = 0,
    limit: int = 100,
    source: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    """获取热门话题列表"""
    query = select(Topic).order_by(Topic.rank)

    if source:
        query = query.filter(Topic.source == source)

    result = await db.execute(query.offset(skip).limit(limit))
    topics = result.scalars().all()
    return topics


@router.get("/{source}", response_model=List[TopicResponse])
async def get_topics_by_source(source: str, db: AsyncSession = Depends(get_db)):
    """获取指定来源的热门话题"""
    query = select(Topic).filter(Topic.source == source).order_by(Topic.rank)
    result = await db.execute(query)
    topics = result.scalars().all()

    if not topics:
        raise HTTPException(
            status_code=404, detail=f"No topics found for source: {source}"
        )

    return topics
