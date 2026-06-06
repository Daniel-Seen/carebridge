from fastapi import APIRouter, Depends
from app.data.database import get_db

router = APIRouter()


@router.get("")
async def list_elders(institution_id: int = 1):
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, name, room, avatar, birth_date, notes, status FROM elders WHERE institution_id = ?",
        (institution_id,)
    )
    rows = await cursor.fetchall()
    await db.close()
    return [dict(r) for r in rows]


@router.get("/{elder_id}")
async def get_elder(elder_id: int):
    db = await get_db()
    cursor = await db.execute(
        "SELECT id, name, room, avatar, birth_date, notes, status FROM elders WHERE id = ?",
        (elder_id,)
    )
    row = await cursor.fetchone()
    if not row:
        await db.close()
        return {"error": "Not found"}
    # Get family members
    f_cursor = await db.execute(
        "SELECT id, name, relation, phone FROM family_members WHERE elder_id = ?",
        (elder_id,)
    )
    family = [dict(f) for f in await f_cursor.fetchall()]
    await db.close()
    result = dict(row)
    result["family"] = family
    return result


@router.post("")
async def create_elder(data: dict):
    db = await get_db()
    cursor = await db.execute(
        "INSERT INTO elders (institution_id, name, room, birth_date, notes) VALUES (?, ?, ?, ?, ?)",
        (data.get("institution_id", 1), data["name"], data.get("room", ""),
         data.get("birth_date"), data.get("notes", ""))
    )
    elder_id = cursor.lastrowid
    await db.commit()
    await db.close()
    return {"id": elder_id, "name": data["name"]}
