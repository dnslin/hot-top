from app.spiders.base import BaseSpider
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from app.core.logger import setup_logger

logger = setup_logger("zhihu_spider")


class ZhihuSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.source = "zhihu"
        self.url = "https://www.zhihu.com/hot"
        self.headers.update(
            {
                "cookie": "",  # 需要添加登录后的cookie
                "referer": "https://www.zhihu.com/",
            }
        )

    async def parse(self, html: str) -> List[Dict[str, Any]]:
        topics = []
        soup = BeautifulSoup(html, "html.parser")

        # 找到热榜内容列表
        items = soup.select(".HotList-item")

        for rank, item in enumerate(items, 1):
            try:
                # 提取标题和链接
                title_element = item.select_one(".HotList-itemTitle")
                title = self.clean_text(title_element.text) if title_element else ""
                url = title_element.get("href", "") if title_element else ""

                # 提取热度
                hot_value_element = item.select_one(".HotList-itemMetrics")
                hot_value = (
                    self.clean_text(hot_value_element.text)
                    if hot_value_element
                    else "0"
                )

                # 提取描述
                excerpt_element = item.select_one(".HotList-itemExcerpt")
                description = (
                    self.clean_text(excerpt_element.text) if excerpt_element else None
                )

                if title and url:
                    topics.append(
                        {
                            "title": title,
                            "url": url,
                            "source": self.source,
                            "rank": rank,
                            "hot_value": hot_value,
                            "description": description,
                        }
                    )
            except Exception as e:
                logger.error(f"Error parsing Zhihu hot topics: {str(e)}")
                continue

        return topics
