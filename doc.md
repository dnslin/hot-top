# Hot Topics API

一个聚合各大网站热门话题的 RESTful API 服务。

## 项目简介

本项目是一个基于 FastAPI 的异步网络爬虫和 API 服务，用于实时获取和提供各大网站的热门话题数据。

### 主要特性

- 异步爬虫：使用 aiohttp 进行高效的并发爬取
- 实时更新：定时任务自动更新热门话题
- RESTful API：标准的 REST 接口设计
- 数据持久化：使用 SQLite 数据库存储
- 日志管理：完整的日志记录和轮转机制
- CORS 支持：支持跨域请求
- 自动文档：集成 Swagger/ReDoc API 文档

## 项目结构

```bash
/hot-top
├── app/
│   ├── api/            # API接口
│   │   └── api_v1/     # API v1 版本
│   │       ├── endpoints/  # API端点
│   │       └── api.py     # API路由聚合
│   ├── core/           # 核心配置
│   │   ├── config.py   # 配置管理
│   │   ├── logger.py   # 日志工具
│   │   └── scheduler.py # 调度器
│   ├── db/             # 数据库
│   │   └── session.py  # 数据库会话
│   ├── models/         # 数据模型
│   │   └── topic.py    # 话题模型
│   └── spiders/        # 爬虫模块
│       ├── base.py     # 爬虫基类
│       ├── manager.py  # 爬虫管理器
│       └── zhihu.py    # 知乎爬虫
├── logs/               # 日志文件目录
├── tests/              # 测试目录
├── .env               # 环境变量
├── .gitignore         # Git忽略配置
├── main.py            # 主程序
└── requirements.txt   # 依赖管理
```

## 技术栈

- Python 3.8+
- FastAPI：Web框架
- SQLAlchemy：ORM框架
- aiohttp：异步HTTP客户端
- BeautifulSoup4：HTML解析
- SQLite：数据库
- Pydantic：数据验证
- uvicorn：ASGI服务器

## 安装和运行

1. 克隆项目
```bash
git clone [repository_url]
cd hot-top
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\activate   # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置环境变量
复制 `.env.example` 到 `.env` 并修改配置：
```env
DATABASE_URL=sqlite+aiosqlite:///./hot_topics.db
API_V1_STR=/api/v1
PROJECT_NAME=Hot Topics API
CRAWLER_INTERVAL=3600
CACHE_EXPIRE=86400
```

5. 运行服务
```bash
python main.py
```

## API 文档

服务启动后，可以通过以下地址访问API文档：

- Swagger UI：http://127.0.0.1:8080/docs
- ReDoc：http://127.0.0.1:8080/redoc

### 主要接口

1. 获取所有热门话题
```
GET /api/v1/topics/
```

2. 获取指定来源的热门话题
```
GET /api/v1/topics/{source}
```

## 日志系统

- 日志位置：`logs/hot_topics_YYYY-MM-DD.log`
- 日志级别：INFO
- 轮转策略：每天轮转，保留30天
- 格式：`时间戳 - 模块名 - 日志级别 - 消息内容`

## 爬虫扩展

要添加新的网站爬虫，需要：

1. 在 `app/spiders/` 下创建新的爬虫类
2. 继承 `BaseSpider` 类
3. 实现 `parse()` 方法
4. 在 `SpiderManager` 中注册新爬虫

示例：
```python
class NewSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.source = "source_name"
        self.url = "target_url"

    async def parse(self, html: str) -> List[Dict[str, Any]]:
        # 实现解析逻辑
        pass
```

## 注意事项

1. 爬虫规范
   - 遵守目标网站的robots.txt
   - 合理设置爬取间隔
   - 必要时添加请求头和认证信息

2. 数据安全
   - 环境变量文件(.env)不要提交到版本控制
   - 定期备份数据库
   - 及时更新依赖包版本

3. 性能优化
   - 合理设置爬虫间隔
   - 适当配置数据库缓存
   - 监控日志大小

## 许可证

MIT License