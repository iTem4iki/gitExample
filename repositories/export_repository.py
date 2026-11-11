from __future__ import annotations
from database.database import get_connection

# Запрос для экспорта: заявки вместе с клиентом и оператором.
# Колонки вида client__login попадут во вложенный объект client.
# Чтобы выгрузить другую таблицу, достаточно заменить этот запрос.
EXPORT_SQL = """
    SELECT r.RequestID AS id,
           r.status,
           CASE WHEN r.status = 1 THEN 'Закрыта'
                WHEN r.operatorID IS NULL THEN 'Новая'
                ELSE 'В работе' END AS status_text,
           r.comment,
           r.rate,
           c.UserID AS client__id,
           c.login  AS client__login,
           o.UserID AS operator__id,
           o.login  AS operator__login
    FROM Request r
    JOIN User c ON c.UserID = r.clientID
    LEFT JOIN User o ON o.UserID = r.operatorID
    ORDER BY r.RequestID
"""


def _nest(row: dict) -> dict:
    # client__login -> {"client": {"login": ...}}
    result = {}
    for key, value in row.items():
        if "__" in key:
            group, name = key.split("__", 1)
            result.setdefault(group, {})[name] = value
        else:
            result[key] = value

    # если все поля вложенного объекта пустые (нет оператора), ставим None
    for key, value in result.items():
        if isinstance(value, dict) and all(v is None for v in value.values()):
            result[key] = None
    return result


def get_export_rows(sql: str = EXPORT_SQL) -> list[dict]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(sql)
    names = [d[0] for d in cur.description]
    rows = cur.fetchall()
    conn.close()
    return [_nest(dict(zip(names, r))) for r in rows]
