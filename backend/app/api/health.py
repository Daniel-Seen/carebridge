from fastapi import APIRouter
from app.data.database import get_db

router = APIRouter()


@router.get("/elder/{elder_id}")
async def get_health_records(elder_id: int, limit: int = 30):
    db = await get_db()
    cursor = await db.execute(
        """SELECT id, elder_id, blood_pressure, heart_rate, blood_sugar,
                  temperature, weight, notes, recorded_at
           FROM health_records
           WHERE elder_id = ?
           ORDER BY recorded_at DESC LIMIT ?""",
        (elder_id, limit)
    )
    rows = await cursor.fetchall()
    await db.close()
    return [dict(r) for r in rows]


@router.post("")
async def create_health_record(data: dict):
    db = await get_db()
    cursor = await db.execute(
        """INSERT INTO health_records (elder_id, blood_pressure, heart_rate,
           blood_sugar, temperature, weight, notes)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (data["elder_id"], data.get("blood_pressure"), data.get("heart_rate"),
         data.get("blood_sugar"), data.get("temperature"), data.get("weight"), data.get("notes", ""))
    )
    record_id = cursor.lastrowid
    await db.commit()
    await db.close()
    return {"id": record_id, "status": "recorded"}
