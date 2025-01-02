from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class Topic(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), index=True)
    url = Column(String(1000))
    source = Column(String(50), index=True)  # 来源网站
    rank = Column(Integer)  # 排名
    hot_value = Column(String(100))  # 热度值
    description = Column(Text, nullable=True)  # 描述
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
