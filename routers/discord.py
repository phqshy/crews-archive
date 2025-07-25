from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from database import discord_database

router = APIRouter(
    prefix="/discord",
    tags=["discord"]
)


def parse_channel(channel_tuple):
    return {
        'id': str(channel_tuple[4]),
        'category_id': str(channel_tuple[1]),
        'category': channel_tuple[2],
        'name': channel_tuple[0],
        'topic': channel_tuple[5],
        'type': channel_tuple[3],
    }


# DEVELOPMENT
"""def parse_channel(channel_tuple):
    return {
        'id': str(channel_tuple[0]),
        'category_id': str(channel_tuple[1]),
        'category': channel_tuple[2],
        'name': channel_tuple[3],
        'topic': channel_tuple[4],
        'type': channel_tuple[5],
    }"""


def parse_user(user_tuple):
    return {
        'id': str(user_tuple[4]),
        'name': user_tuple[5],
        'discriminator': user_tuple[2],
        'nickname': user_tuple[0],
        'is_bot': user_tuple[1],
        'avatar_url': user_tuple[3],
    }


# DEVELOPMENT
"""def parse_user(user_tuple):
    return {
        'id': str(user_tuple[0]),
        'name': user_tuple[1],
        'discriminator': user_tuple[2],
        'nickname': user_tuple[3],
        'is_bot': user_tuple[4],
        'avatar_url': user_tuple[5],
    }"""


def parse_emoji(emoji_tuple):
    return {
        'id': emoji_tuple[1],
        'name': emoji_tuple[2],
        'code': emoji_tuple[3],
        'image_url': emoji_tuple[0],
    }


# DEVELOPMENT
"""def parse_message(message_tuple):
    return {
        'id': str(message_tuple[0]),
        'channel_id': str(message_tuple[1]),
        'author_id': str(message_tuple[2]),
        'type': message_tuple[3],
        'timestamp': message_tuple[4],
        'timestamp_edited': message_tuple[5],
        'is_pinned': message_tuple[6],
        'content': message_tuple[7],
        'reference_message': str(message_tuple[8]),
        'embeds': message_tuple[9][0] if message_tuple[9] is not None else [],
        # 'ts': message_tuple[10],
        'mentioned_users': message_tuple[11] if message_tuple[11][0] is not None else [],
        'reactions': message_tuple[12] if message_tuple[12][0]['reaction_id'] is not None else []
    }"""


def parse_message(message_tuple):
    if message_tuple[11] is None or message_tuple[11][0] is None:
        mentioned_users = []
    else:
        mentioned_users = message_tuple[11]

    if message_tuple[12] is None or message_tuple[12][0]['reaction_id'] is None:
        reactions = []
    else:
        reactions = message_tuple[12]

    return {
        'id': str(message_tuple[4]),
        'channel_id': str(message_tuple[6]),
        'author_id': str(message_tuple[7]),
        'type': message_tuple[0],
        'timestamp': message_tuple[5],
        'timestamp_edited': message_tuple[2],
        'is_pinned': message_tuple[3],
        'content': message_tuple[10],
        'reference_message': str(message_tuple[9]),
        'embeds': message_tuple[8][0] if message_tuple[8] is not None else [],
        # 'ts': message_tuple[1],
        'mentioned_users': mentioned_users,
        'reactions': reactions
    }


class ErrorMessage(BaseModel):
    message: str


class Channel(BaseModel):
    id: str
    category_id: str | None = None
    category: str | None = None
    name: str
    topic: str | None = None
    type: str


class User(BaseModel):
    id: str
    name: str
    discriminator: str
    nickname: str
    is_bot: bool
    avatar_url: str


class Emoji(BaseModel):
    id: int
    name: str
    code: str
    image_url: str


class EmbedAuthor(BaseModel):
    name: str
    url: str | None = None
    iconUrl: str | None = None


class EmbedMedia(BaseModel):
    url: str
    width: int
    height: int


class EmbedField(BaseModel):
    name: str
    value: str
    isInline: bool


class Embed(BaseModel):
    title: str
    url: str
    timestamp: datetime | None = None
    description: str
    color: str | None = None
    author: EmbedAuthor | None = None
    thumbnail: EmbedMedia | None = None
    video: EmbedMedia | None = None
    images: List[EmbedMedia] = []
    fields: List[EmbedField] = []


class Reaction(BaseModel):
    reaction_id: int
    emoji_id: int
    count: int
    users: List[int]


class Message(BaseModel):
    id: str
    channel_id: str
    author_id: str
    type: str
    timestamp: datetime
    timestamp_edited: datetime | None = None
    is_pinned: bool
    content: str
    reference_message: str | None = None
    embeds: List[Embed]
    mentioned_users: List[int]
    reactions: List[Reaction]


@router.get("/channels", response_model=List[Channel])
def get_all_channels():
    cur = discord_database.cursor()
    cur.execute("SELECT * FROM channels")
    return list(map(lambda x: parse_channel(x), cur.fetchall()))


@router.get("/channel", response_model=Channel, responses={404: {"model": ErrorMessage}})
def get_channel_by_id(channel_id: int):
    cur = discord_database.cursor()
    cur.execute("SELECT * FROM channels WHERE id = %s", (channel_id,))
    result = cur.fetchall()
    if result is None or len(result) == 0:
        return JSONResponse(status_code=404, content={"message": "Channel not found"})
    else:
        return parse_channel(result[0])


@router.get("/users", response_model=List[User])
def get_all_users():
    cur = discord_database.cursor()
    cur.execute("SELECT * FROM users")
    return list(map(lambda x: parse_user(x), cur.fetchall()))


@router.get("/user", response_model=User, responses={404: {"model": ErrorMessage}})
def get_user_by_id(user_id: int):
    cur = discord_database.cursor()
    cur.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    result = cur.fetchall()
    if result is None:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    else:
        return parse_user(result[0])


@router.get("/emojis", response_model=List[Emoji])
def get_all_emojis():
    cur = discord_database.cursor()
    cur.execute("SELECT * FROM emoji")
    return list(map(lambda x: parse_emoji(x), cur.fetchall()))


@router.get("/emoji", response_model=Emoji, responses={404: {"model": ErrorMessage}})
def get_emoji_by_id(emoji_id):
    cur = discord_database.cursor()
    cur.execute("SELECT * FROM emoji WHERE id = %s", (emoji_id,))
    result = cur.fetchall()
    if result is None:
        return JSONResponse(status_code=404, content={"message": "Emoji not found"})
    else:
        return parse_emoji(result[0])


whitelistedChannels = (668731047361511435,
                       668731263888130058,
                       668731285316960276,
                       668731685139120129,
                       668731740981821440,
                       668731818802937856,
                       668755221778006016,
                       845917318738477086,
                       922811489469988904,
                       933553404112957500,
                       948321518834831390)


@router.get("/messages", response_model=List[Message])
def get_messages(
        limit: int = 20,
        last_id: int = 0,
        channel_id: int = 0,
        author_id: int = 0,
        mentioned_id: int = 0,
        before: int = 0,
        after: int = 0,
        content: str = ""
):
    cur = discord_database.cursor()
    base_query = """
    select
        messages.*,
        json_agg(mentions.user_id) as mentioned_users,
        json_agg(
            json_build_object(
                'reaction_id', reactions.id,
                'emoji_id', reactions.emoji_id,
                'count', reactions.count,
                'users', (
                    select json_agg(reactions_users.user_id)
                    from reactions_users
                    where reactions_users.reaction_id = reactions.id
                )
            )
        ) as reactions
    from messages
    left join reactions on messages.id = reactions.message_id
    left join mentions on messages.id = mentions.message_id
    """

    conditions = []
    if channel_id != 0:
        conditions.append(("channel_id = %s", channel_id))

    if last_id != 0:
        conditions.append(("messages.id < %s", last_id))

    if author_id != 0:
        conditions.append(("messages.author_id = %s", author_id))

    if mentioned_id != 0:
        conditions.append(("mentions.user_id = %s", mentioned_id))

    if before != 0:
        conditions.append(("messages.timestamp <= %s", datetime.fromtimestamp(before)))

    if after != 0:
        conditions.append(("messages.timestamp >= %s", datetime.fromtimestamp(after)))

    if content != "":
        conditions.append(("ts @@ phraseto_tsquery('english', %s)", content))

    conditions.append(("channel_id in %s", whitelistedChannels))

    statements = " and ".join(map(lambda x: x[0], conditions))
    values = list(map(lambda x: x[1], conditions))

    if len(statements) != 0:
        base_query += f"where {statements} "

    base_query += f"""
    group by messages.id
    order by messages.id desc 
    limit {limit}"""
    cur.execute(base_query, values)
    return list(map(lambda x: parse_message(x), cur.fetchall()))
