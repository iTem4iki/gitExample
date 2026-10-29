from __future__ import annotations
from database.database import get_connection
from models.user_role import UserRole


def _map(row) -> UserRole:
    return UserRole(*row)


def create(name: str, description: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO UserRole(name, description) VALUES (?, ?)",
                (name, description))
    conn.commit()
    conn.close()


def get_by_id(role_id: int) -> UserRole | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT UserRoleID, name, description FROM UserRole WHERE UserRoleID = ?",
                (role_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[UserRole]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT UserRoleID, name, description FROM UserRole")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(role_id: int, name: str, description: str | None):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE UserRole SET name = ?, description = ? WHERE UserRoleID = ?",
                (name, description, role_id))
    conn.commit()
    conn.close()


def delete(role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM UserRole WHERE UserRoleID = ?", (role_id,))
    conn.commit()
    conn.close()
