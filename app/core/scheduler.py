import asyncio
from app.spiders.manager import SpiderManager
from datetime import datetime
import schedule
import time
from threading import Thread
from app.core.logger import setup_logger

logger = setup_logger("scheduler")


class Scheduler:
    def __init__(self):
        self.spider_manager = SpiderManager()
        self.is_running = False
        self._loop = None

    async def crawl_task(self):
        """爬虫任务"""
        try:
            logger.info(f"Starting crawl task at {datetime.now()}")
            # 直接运行爬虫，数据保存已经在 run_all_spiders 中处理
            topics = await self.spider_manager.run_all_spiders()
            logger.info(
                f"Crawl task completed at {datetime.now()}, got {len(topics)} topics"
            )
        except Exception as e:
            logger.error(f"Error in crawl task: {str(e)}")

    def _run_crawl_task(self):
        """在新的事件循环中运行爬虫任务"""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.crawl_task())
        loop.close()

    def start(self, interval_seconds: int = 3600):
        """启动调度器"""
        if self.is_running:
            return

        self.is_running = True
        logger.info(f"Starting scheduler with interval: {interval_seconds} seconds")

        # 立即运行一次
        Thread(target=self._run_crawl_task).start()

        # 设置定时任务
        schedule.every(interval_seconds).seconds.do(
            lambda: Thread(target=self._run_crawl_task).start()
        )

        # 在后台线程中运行调度器
        def run_scheduler():
            while self.is_running:
                schedule.run_pending()
                time.sleep(1)

        Thread(target=run_scheduler, daemon=True).start()

    def stop(self):
        """停止调度器"""
        self.is_running = False
        logger.info("Scheduler stopped")
