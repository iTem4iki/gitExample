from __future__ import annotations
from database.database import get_connection
from models.user import User

# role_name берём из таблицы UserRole
SELECT_SQL = """
    SELECT u.UserID, u.login, u.passwordHash, u.UserRoleID, r.name
    FROM User u
    JOIN UserRole r ON r.UserRoleID = u.UserRoleID
"""


def _map(row) -> User:
    return User(*row)


def create(login: str, password_hash: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO User(login, passwordHash, UserRoleID) VALUES (?, ?, ?)",
                (login, password_hash, role_id))
    conn.commit()
    conn.close()


def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_SQL + " WHERE u.UserID = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_SQL + " WHERE u.login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(SELECT_SQL + " ORDER BY u.UserID")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(user_id: int, login: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE User SET login = ?, UserRoleID = ? WHERE UserID = ?",
                (login, role_id, user_id))
    conn.commit()
    conn.close()


def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM User WHERE UserID = ?", (user_id,))
    conn.commit()
    conn.close()
