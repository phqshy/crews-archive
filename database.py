import os

import psycopg2

postgres_url = os.environ['POSTGRES_URL']
postgres_username = os.environ['POSTGRES_USERNAME']
postgres_password = os.environ['POSTGRES_PASSWORD']
postgres_database = os.environ['POSTGRES_DATABASE']


rmb_database = psycopg2.connect(
    f"host={postgres_url} dbname=archives user={postgres_username} password={postgres_password}")

discord_database = psycopg2.connect(
    f"host={postgres_url} dbname=discord user={postgres_username} password={postgres_password}")