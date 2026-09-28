import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()
ps = os.getenv("ps")

async def connection():
    try:
        con = await asyncpg.connect(
            database = "Bot_db",
            host = "localhost",
            user = "postgres",
            port = 5432,
            password = ps
        )
        print("Connection OK")
        return con
    except Exception as error:
        print(f"Connection Error: {error}")

async def create_table():
    con = await connection()
    try:
        await con.execute("""
            create table if not exists users1(
                user_id serial primary key,
                user_name varchar(100),
                full_name varchar(100),
                telegram_id varchar,
                created_at timestamp default now(),
                is_active boolean default true
            );

            create table if not exists tasks(
                task_id serial primary key,
                task_name varchar(100),
                task_description varchar(100),
                task_status boolean default false,
                telegram_id varchar,
                created_at timestamp default now(),
                is_active boolean default true
            );
""")
        print("Table created")
    except Exception as error:
        print(f"Creating table error: {error}")
    finally:
        await con.close()