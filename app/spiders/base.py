from abc import ABC, abstractmethod
from typing import List, Dict, Any
import aiohttp
from app.core.logger import setup_logger
from app.db.crud import save_topics
from app.db.session import async_session

logger = setup_logger("spider")


class BaseSpider(ABC):
    def __init__(self):
        self.source: str = ""
        self.url: str = ""
        self.headers: Dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    @abstractmethod
    async def parse(self, html: str) -> List[Dict[str, Any]]:
        """解析HTML内容"""
        pass

    async def fetch(self) -> str:
        """获取页面内容"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.url, headers=self.headers) as response:
                    return await response.text()
        except Exception as e:
            logger.error(f"Error fetching {self.url}: {str(e)}")
            return ""

    async def get_hot_topics(self) -> List[Dict[str, Any]]:
        """获取热门话题"""
        html = await self.fetch()
        if not html:
            return []
        return await self.parse(html)

    def clean_text(self, text: str) -> str:
        """清理文本"""
        if not text:
            return ""
        return text.strip()

    async def crawl(self):
        try:
            html = await self.fetch()
            if html:
                topics = await self.parse(html)
                if topics:
                    async with async_session() as session:
                        await save_topics(session, topics)
                    return topics
        except Exception as e:
            logger.error(f"Error in crawl task: {str(e)}")
            raise e
