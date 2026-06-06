"""Database initialization"""
import aiosqlite
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "carebridge.db"


async def get_db():
    db = await aiosqlite.connect(str(DB_PATH))
    db.row_factory = aiosqlite.Row
    return db


async def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    db = await get_db()
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS institutions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            code TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS elders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            institution_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            room TEXT,
            avatar TEXT DEFAULT '👴',
            birth_date TEXT,
            notes TEXT,
            status TEXT DEFAULT 'active',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (institution_id) REFERENCES institutions(id)
        );

        CREATE TABLE IF NOT EXISTS family_members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elder_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            relation TEXT NOT NULL,
            phone TEXT,
            wechat_id TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (elder_id) REFERENCES elders(id)
        );

        CREATE TABLE IF NOT EXISTS daily_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elder_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            mood TEXT CHECK(mood IN ('happy','calm','tired','unwell','other')),
            image_url TEXT,
            activity TEXT,
            meal_summary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (elder_id) REFERENCES elders(id)
        );

        CREATE TABLE IF NOT EXISTS health_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            elder_id INTEGER NOT NULL,
            blood_pressure TEXT,
            heart_rate INTEGER,
            blood_sugar REAL,
            temperature REAL,
            weight REAL,
            notes TEXT,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (elder_id) REFERENCES elders(id)
        );

        -- Seed demo data
        INSERT OR IGNORE INTO institutions (id, name, code) VALUES (1, '阳光养老院', 'SUN001');
        INSERT OR IGNORE INTO elders (id, institution_id, name, room, birth_date, notes)
        VALUES (1, 1, '张大爷', '301', '1942-03-15', '喜安静，爱下棋');
        INSERT OR IGNORE INTO elders (id, institution_id, name, room, birth_date, notes)
        VALUES (2, 1, '李奶奶', '205', '1948-08-22', '爱唱歌，需按时服药');
        INSERT OR IGNORE INTO family_members (id, elder_id, name, relation, phone)
        VALUES (1, 1, '张小明', '儿子', '13800138001');
        INSERT OR IGNORE INTO family_members (id, elder_id, name, relation, phone)
        VALUES (2, 2, '李小红', '女儿', '13900139001');
        INSERT OR IGNORE INTO daily_updates (elder_id, content, mood, activity, meal_summary)
        VALUES (1, '今天张大爷精神很好，早上下了一盘棋赢了！', 'happy', '下棋、散步', '早餐小米粥+鸡蛋，午餐红烧肉+青菜');
        INSERT OR IGNORE INTO daily_updates (elder_id, content, mood, activity, meal_summary)
        VALUES (2, '李奶奶参加了合唱活动，唱了《茉莉花》', 'happy', '合唱、手工', '早餐豆浆+馒头，午餐清蒸鱼+豆腐');
        INSERT OR IGNORE INTO health_records (elder_id, blood_pressure, heart_rate, blood_sugar, temperature)
        VALUES (1, '128/82', 72, 5.6, 36.5);
        INSERT OR IGNORE INTO health_records (elder_id, blood_pressure, heart_rate, blood_sugar, temperature)
        VALUES (2, '135/88', 78, 6.2, 36.3);
    """)
    await db.commit()
    await db.close()
