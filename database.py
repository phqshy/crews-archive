import os

import psycopg2

postgres_url = os.environ['POSTGRES_URL']
postgres_username = os.environ['POSTGRES_USERNAME']
postgres_password_file = os.environ['POSTGRES_PASSWORD']
with open(postgres_password_file) as f:
    postgres_password = f.readline()
rmb_database_name = os.environ['RMB_DATABASE']
discord_database_name = os.environ['DISCORD_DATABASE']

rmb_database = psycopg2.connect(
    f"host={postgres_url} dbname={rmb_database_name} user={postgres_username} password={postgres_password}")

discord_database = psycopg2.connect(
    f"host={postgres_url} dbname={discord_database_name} user={postgres_username} password={postgres_password}")
