import asyncio
from dotenv import load_dotenv
from aiogram import Dispatcher, Router , Bot
from aiogram.types import Message
from aiogram.filters import CommandStart , Command , CommandObject
from connection import create_table
from service import *
import os

load_dotenv()
token = os.getenv("token")

bot = Bot(token)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer(f"Hello {message.from_user.first_name} dear 😁")
    else:
        await save_user(message.from_user.id , message.from_user.username , message.from_user.full_name)
        await message.answer(f"Hello {message.from_user.first_name} dear 😁")


@dp.message(Command("add_task"))
async def add_task1(message: Message , command: CommandObject):
    task = command.args
    if task is None:
        await message.answer("Enter task in this format: task_name/task_description")
    else:
        task = task.split("/")
        await add_task(task[0] , task[1] , message.from_user.id)
        await message.answer(f"You entered {task[0]}")

@dp.message(Command("show_tasks"))
async def show_all_tasks(message:Message):
    show_all = await show_your_tasks(message.from_user.id)
    if show_all is None:
        await message.answer("You don't have tusks")
    else:
        text = "You tasks:\n\n"
        for i in show_all:
            text += f"""
Telegram id: {i['task_id']}
title: {i['task_name']}
description: {i['task_description']}
status {i['task_status']}
telegram id of user: {i['telegram_id']}
created at: {i['created_at']}\n
            """
            await message.answer(f"{text}")

@dp.message(Command("update_task"))
async def update_your_task(message:Message , command:CommandObject):
    info_from_user = command.args
    try:
        info_from_user = info_from_user.split("/")
        await update_task(info_from_user[0] , info_from_user[1] , info_from_user[2] , info_from_user[3] , message.from_user.id)
        await message.answer(f"{info_from_user[1]} is updated!")
    except Exception:
        await message.answer("You entered some data not properly please enter like this:\n/update_task task_id/task_name/task_description/task_status")

@dp.message(Command("help"))
async def help(message: Message):
    await message.answer("""
===Help Menu===
Comands:
/start - Start the bot
/help - Help menu
/add_task - Add a new task
/show_tasks - shows all your tasks
/update_task - update your tasks
""")

async def main():
    print("Bot started")
    await create_table()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())