import asyncio
from typing import List, Dict, Any
from app.spiders.zhihu import ZhihuSpider
from app.spiders.s360 import Spider360
from app.core.logger import setup_logger
from app.db.crud import save_topics
from app.db.session import async_session_maker
from app.spiders.sogou import SogouSpider

logger = setup_logger("spider_manager")


class SpiderManager:
    def __init__(self):
        self.spiders = [
            ZhihuSpider(),
            Spider360(),
            SogouSpider(),
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
        """运行所有爬虫并保存数据"""
        try:
            # 运行所有爬虫获取数据
            tasks = [self.run_spider(spider) for spider in self.spiders]
            results = await asyncio.gather(*tasks)
            all_topics = [item for sublist in results for item in sublist]

            # 如果有数据则保存
            if all_topics:
                async with async_session_maker() as session:
                    await save_topics(session, all_topics)

            return all_topics

        except Exception as e:
            logger.error(f"Error in run_all_spiders: {str(e)}")
            return []
