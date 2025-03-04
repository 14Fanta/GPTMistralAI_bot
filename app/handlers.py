import os
# IMPORT AIOGRAM
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
#SQLITE3
import sqlite3
#OTHERS
from dotenv import load_dotenv
from config import TOKEN_TG
from states import *
#Mistral
from mistralai import Mistral


load_dotenv()

api_key = os.environ['Mistral_Key_api']

model = "mistral-large-latest"

client = Mistral(api_key=api_key)

bot = Bot(token=TOKEN_TG)
dp = Dispatcher()
db = sqlite3.connect("users.sqlite3")
cursor = db.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY, 
        tg_id INTEGER, 
        FULL_NAME TEXT
    )
""")

user_router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    user = cursor.execute("SELECT tg_id FROM users WHERE tg_id = ?", (message.from_user.id,)).fetchone()
    if not user:
        cursor.execute("INSERT INTO users(tg_id, FULL_NAME) VALUES(?, ?)", (message.from_user.id, message.from_user.full_name))
        db.commit()
    await message.answer("Добро пожаловать в бота для учёбы! Ты можешь задать мне любой вопрос на тему учёбы, а я постараюсь на него ответить!\n А также ты можешь попросить меня сделать для тебя какое-то задание.\n Напиши свой запрос: ")
    await state.set_state(waiting.waiting_a_message)

@user_router.message(waiting.waiting_a_message)
async def generator_content(msg: Message, state: FSMContext):
    # Проверяем, является ли сообщение командой
    if msg.text.startswith('/'):
        await msg.answer("Повторите команду.")
        await state.clear()
        return
    
    chat_response = client.chat.complete(
        model=model,
        messages=[
            {
                "role": "user",
                # "content": f"{msg.text}\n На основе этого выполни запрос про образование, если, что то непонятно, попроси человека уточнить. Также, если будет вопрос не по образовательной теме, ты просишь человека, задать вопрос на тему образования!  ",
                "content": f"Ты бот, который помогает изучать различные темы: языки, математика, история и т.д. Пользователи могут выбирать тему и уровень сложности, а бот будет предлагать задания, проверять ответы и давать рекомендации.\n{msg.text}",
            },
        ]
    )
    await msg.answer(chat_response.choices[0].message.content)
    
@user_router.message(Command('help'))
async def cmd_help(message:Message):
    await message.answer(f"Ты написал команду: {message.text}")