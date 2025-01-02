import logging
import sys
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# 创建日志目录
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

# 日志文件路径
LOG_FILE = LOG_DIR / f"hot_topics_{datetime.now().strftime('%Y-%m-%d')}.log"

# 日志格式
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def setup_logger(name: str = None) -> logging.Logger:
    """
    设置日志记录器
    :param name: 日志记录器名称
    :return: 日志记录器实例
    """
    # 获取日志记录器
    logger = logging.getLogger(name or __name__)
    logger.setLevel(logging.INFO)

    # 如果已经有处理器，直接返回
    if logger.handlers:
        return logger

    # 创建格式化器
    formatter = logging.Formatter(LOG_FORMAT, DATE_FORMAT)

    # 控制台处理器
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    # 文件处理器（每天轮换）
    file_handler = TimedRotatingFileHandler(
        LOG_FILE,
        when="midnight",
        interval=1,
        backupCount=30,  # 保留30天的日志
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # 添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# 创建默认日志记录器
logger = setup_logger("hot_topics")
