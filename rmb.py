import math
import os
from datetime import datetime

import psycopg2
from flask import Blueprint, request

rmb = Blueprint("rmb", __name__, url_prefix="/rmb")


postgres_url = os.environ['POSTGRES_URL']
postgres_username = os.environ['POSTGRES_USERNAME']
postgres_password = os.environ['POSTGRES_PASSWORD']
postgres_database = os.environ['POSTGRES_DATABASE']


database_connection = psycopg2.connect(
    f"host={postgres_url} dbname={postgres_database} user={postgres_username} password={postgres_password}")


###
# Able to search for:
# - Author
# - Posted time
# - Sort type? (newest/oldest/number of likes)
# - Keywords
###
@rmb.route("/posts")
def search_posts():
    offset = int(request.args.get("page", 0)) * 20
    cur = database_connection.cursor()

    author = request.args.get("nation", "").replace(" ", "_")
    before = int(request.args.get("before", 0))
    after = int(request.args.get("after", 0))
    keywords = request.args.get("keywords", "")
    sort = request.args.get("sort", "id")
    order = request.args.get("order", "desc")

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
