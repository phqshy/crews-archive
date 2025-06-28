import math
from datetime import datetime

from fastapi import APIRouter

from database import rmb_database

router = APIRouter(
    prefix="/rmb",
    tags=["rmb"]
)


@router.get("/posts")
def search_posts(
        page: int = 0,
        author: str = "",
        before: int = 0,
        after: int = 0,
        keywords: str = "",
        sort: str = "id",
        order: str = "desc"
):
    cur = rmb_database.cursor()
    offset = page * 20

    conditions = []
    if not author == "":
        conditions.append(("nation = %s", author))
    if not before == 0:
        conditions.append(("posted <= %s", datetime.fromtimestamp(before)))
    if not after == 0:
        conditions.append(("posted >= %s", datetime.fromtimestamp(after)))
    if not keywords == "":
        conditions.append(("ts @@ phraseto_tsquery('english', %s)", keywords))

    if len(conditions) == 0:
        conditions.append(("id > %s", 0))

    statements = " AND ".join(map(lambda x: x[0], conditions))
    values = list(map(lambda x: x[1], conditions))
    order = f"ORDER BY {sort} {order}"

    query = f"SELECT * FROM rmb WHERE {statements} {order} LIMIT 20 OFFSET {offset}"

    cur.execute(query, values)
    messages = parse_messages(cur)
    cur.close()

    return messages


def parse_messages(cur):
    all_posts = []

    for i in cur:
        posted = math.floor(i[1].timestamp())
        edited = math.floor(i[2].timestamp()) if i[2] is not None else 0

        obj = {
            "id": i[0],
            "posted": posted,
            "edited": edited,
            "nation": i[3],
            "likes": i[4],
            "likers": i[5],
            "message": i[6],
            "status": i[7],
            "suppressor": i[8],
        }

        all_posts.append(obj)

    return all_posts
