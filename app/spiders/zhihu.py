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
                "cookie": "",
                "referer": "https://www.zhihu.com/",
            }
        )

    async def parse(self, html: str) -> List[Dict[str, Any]]:
        logger.info(f"Parsing Zhihu hot topics {self.url}")
        topics = []
        soup = BeautifulSoup(html, "html.parser")

        # 找到热榜内容列表 - 更新选择器
        items = soup.select(".HotItem")

        for item in items:
            try:
                # 提取排名
                rank_element = item.select_one(".HotItem-rank")
                rank = int(self.clean_text(rank_element.text)) if rank_element else 0

                # 提取标题和链接
                link_element = item.select_one(".HotItem-content a")
                title = link_element.get("title", "") if link_element else ""
                url = link_element.get("href", "") if link_element else ""

                # 提取热度
                metrics_element = item.select_one(".HotItem-metrics")
                hot_value = ""
                if metrics_element:
                    # 移除火焰图标的文本,只保留数字部分
                    hot_text = self.clean_text(metrics_element.text)
                    # 处理 '774 万热度\u200b分享' 格式的文本
                    hot_value = (
                        hot_text.split("热度")[0].strip() if "热度" in hot_text else ""
                    )

                # 提取描述
                excerpt_element = item.select_one(".HotItem-excerpt")
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
                logger.error(f"Error parsing Zhihu hot topic: {str(e)}")
                continue

        return topics
