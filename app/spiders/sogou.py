from app.spiders.base import BaseSpider
from typing import List, Dict, Any
import json
from app.core.logger import setup_logger

logger = setup_logger("sogou_spider")


class SogouSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.source = "sogou"
        self.url = "https://hotlist.imtt.qq.com/Fetch"

    async def parse(self, html: str) -> List[Dict[str, Any]]:
        logger.info(f"Parsing Sogou hot topics {self.url}")
        topics = []

        try:
            # 解析JSON响应
            data = json.loads(html)

            # 获取 main 数组数据
            main_data = data.get("main", [])

            for item in main_data:
                try:
                    topics.append(
                        {
                            "title": item.get("title", ""),
                            "url": item.get("url", ""),
                            "source": self.source,
                            "rank": len(topics) + 1,  # 使用索引作为排名
                            "hot_value": item.get("score", "0"),
                            "description": item.get(
                                "event_type", ""
                            ),  # 使用事件类型作为描述
                            "image_url": "",  # 搜狗接口没有提供图片URL
                        }
                    )
                except Exception as e:
                    logger.error(f"Error parsing Sogou topic item: {str(e)}")
                    continue

        except Exception as e:
            logger.error(f"Error parsing Sogou response: {str(e)}")

        return topics
