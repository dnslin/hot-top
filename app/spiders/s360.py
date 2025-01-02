from app.spiders.base import BaseSpider
from typing import List, Dict, Any
import json
from app.core.logger import setup_logger

logger = setup_logger("360_spider")


class Spider360(BaseSpider):
    def __init__(self):
        super().__init__()
        self.source = "360"
        self.url = "https://ranks.hao.360.com/mbsug-api/hotnewsquery?type=news&realhot_limit=50&src=hao_ranklist_so"

    async def parse(self, html: str) -> List[Dict[str, Any]]:
        logger.info(f"Parsing 360 hot topics {self.url}")
        topics = []

        try:
            # 解析JSON响应
            data = json.loads(html)

            # 直接遍历列表数据
            for item in data:
                try:
                    topics.append(
                        {
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "source": self.source,
                            "rank": int(item.get("rank", 0)),
                            "hot_value": item.get("score", ""),
                            "description": item.get("brieftxt", ""),
                            "image_url": item.get("newscard_imgurl", ""),
                        }
                    )
                except Exception as e:
                    logger.error(f"Error parsing 360 topic item: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing 360 response: {str(e)}")

        return topics
