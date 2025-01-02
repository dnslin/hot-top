import asyncio
from typing import List, Dict, Any
from app.spiders.zhihu import ZhihuSpider
from app.models.topic import Topic
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.logger import setup_logger

logger = setup_logger("spider_manager")


class SpiderManager:
    def __init__(self):
        self.spiders = [
            ZhihuSpider(),
            # 在这里添加其他爬虫
        ]

    async def run_spider(self, spider) -> List[Dict[str, Any]]:
        """运行单个爬虫"""
        try:
            return await spider.get_hot_topics()
        except Exception as e:
            logger.error(f"Error running spider {spider.source}: {str(e)}")
            return []

    async def run_all_spiders(self) -> List[Dict[str, Any]]:
        """运行所有爬虫"""
        tasks = [self.run_spider(spider) for spider in self.spiders]
        results = await asyncio.gather(*tasks)
        return [item for sublist in results for item in sublist]

    async def save_topics(self, topics: List[Dict[str, Any]], db: AsyncSession):
        """保存话题到数据库"""
        try:
            # 删除旧数据
            await db.execute("DELETE FROM topics")

            # 插入新数据
            db_topics = [
                Topic(
                    title=topic["title"],
                    url=topic["url"],
                    source=topic["source"],
                    rank=topic["rank"],
                    hot_value=topic["hot_value"],
                    description=topic["description"],
                )
                for topic in topics
            ]

            db.add_all(db_topics)
            await db.commit()

            logger.info(f"Successfully saved {len(topics)} topics to database")
        except Exception as e:
            await db.rollback()
            logger.error(f"Error saving topics to database: {str(e)}")
            raise
