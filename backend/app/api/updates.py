from fastapi import APIRouter
from app.data.database import get_db

router = APIRouter()


@router.get("/elder/{elder_id}")
async def get_updates(elder_id: int, limit: int = 20):
    db = await get_db()
    cursor = await db.execute(
        """SELECT d.id, d.elder_id, e.name as elder_name, d.content, d.mood,
                  d.image_url, d.activity, d.meal_summary, d.created_at
           FROM daily_updates d
           JOIN elders e ON d.elder_id = e.id
           WHERE d.elder_id = ?
           ORDER BY d.created_at DESC LIMIT ?""",
        (elder_id, limit)
    )
    rows = await cursor.fetchall()
    await db.close()
    return [dict(r) for r in rows]


@router.get("/institution/{institution_id}")
async def get_institution_updates(institution_id: int = 1, limit: int = 30):
    db = await get_db()
    cursor = await db.execute(
        """SELECT d.id, d.elder_id, e.name as elder_name, e.avatar, d.content, d.mood,
                  d.image_url, d.activity, d.meal_summary, d.created_at
           FROM daily_updates d
           JOIN elders e ON d.elder_id = e.id
           WHERE e.institution_id = ?
           ORDER BY d.created_at DESC LIMIT ?""",
        (institution_id, limit)
    )
    rows = await cursor.fetchall()
    await db.close()
    return [dict(r) for r in rows]


@router.post("")
async def create_update(data: dict):
    db = await get_db()
    cursor = await db.execute(
        """INSERT INTO daily_updates (elder_id, content, mood, image_url, activity, meal_summary)
           VALUES (?, ?, ?, ?, ?, ?)""",
        (data["elder_id"], data["content"], data.get("mood", "calm"),
         data.get("image_url"), data.get("activity", ""), data.get("meal_summary", ""))
    )
    update_id = cursor.lastrowid
    await db.commit()
    await db.close()
    return {"id": update_id, "status": "created"}
