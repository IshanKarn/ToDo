# from app.database import get_sqlite_connection

# def create_task(data):
#     conn = get_sqlite_connection()
#     cursor = conn.cursor()
#     cursor.execute(
#         "INSERT INTO tasks (title, description, due_date) VALUES (?, ?, ?)",
#         (data["title"], data.get("description"), data.get("due_date"))
#     )
#     conn.commit()
#     task_id = cursor.lastrowid
#     conn.close()
#     return task_id

# def get_tasks():
#     conn = get_sqlite_connection()
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM tasks")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows


from app.database import get_connection

def create_task(data, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO tasks (title, description, due_date, user_id)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (data["title"], data["description"], data["due_date"], user_id))

    task_id = cur.fetchone()[0]
    conn.commit()
    conn.close()
    return {"id": task_id, "message": "Task created"}

def get_tasks(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, title, description, due_date, status FROM tasks WHERE user_id=%s",
        (user_id,)
    )

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "due_date": str(r[3]),
            "status": r[4]
        } for r in rows
    ]

def update_task(task_id, user_id, data):
    conn = get_connection()
    cur = conn.cursor()

    fields = []
    values = []

    for key, value in data.items():
        if value is not None:
            fields.append(f"{key}=%s")
            values.append(value)

    if not fields:
        conn.close()
        return {"message": "No fields to update"}

    values.extend([task_id, user_id])

    query = f"""
        UPDATE tasks
        SET {', '.join(fields)}
        WHERE id=%s AND user_id=%s
    """

    cur.execute(query, tuple(values))
    conn.commit()

    updated = cur.rowcount
    conn.close()

    if updated == 0:
        return None

    return {"message": "Task updated"}


def delete_task(task_id, user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM tasks WHERE id=%s AND user_id=%s",
        (task_id, user_id)
    )

    conn.commit()
    deleted = cur.rowcount
    conn.close()

    if deleted == 0:
        return None

    return {"message": "Task deleted"}
