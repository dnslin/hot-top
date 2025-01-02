from sqlalchemy import text
from datetime import datetime


async def save_topics(db, topics: list):
    try:
        # 为每个话题添加抓取时间
        current_time = datetime.now()
        for topic in topics:
            # 检查是否存在相同的话题(基于标题和来源)
            existing_topic = await db.execute(
                text("SELECT id FROM topics WHERE title = :title AND source = :source"),
                {"title": topic["title"], "source": topic["source"]},
            )
            result = existing_topic.first()

            if result:
                # 如果存在,更新数据
                await db.execute(
                    text("""
                        UPDATE topics 
                        SET url = :url, 
                            rank = :rank, 
                            hot_value = :hot_value, 
                            description = :description,
                            image_url = :image_url,
                            updated_at = :updated_at
                        WHERE id = :id
                    """),
                    {
                        "id": result[0],
                        "url": topic["url"],
                        "rank": topic["rank"],
                        "hot_value": topic["hot_value"],
                        "description": topic["description"],
                        "image_url": topic.get("image_url"),  # 使用get方法安全获取
                        "updated_at": current_time,
                    },
                )
            else:
                # 如果不存在,插入新数据
                await db.execute(
                    text("""
                        INSERT INTO topics (
                            title, url, source, rank, hot_value, 
                            description, image_url, created_at, updated_at
                        )
                        VALUES (
                            :title, :url, :source, :rank, :hot_value, 
                            :description, :image_url, :created_at, :updated_at
                        )
                    """),
                    {**topic, "created_at": current_time, "updated_at": current_time},
                )

        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
