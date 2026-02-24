import asyncio
import sqlite3
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from config import BOT_TOKEN, GROUPS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

db = sqlite3.connect("data.db")
cursor = db.cursor()

user_steps = {}

@dp.message(Command("start"))
async def start(message: Message):
    cursor.execute(
        "INSERT OR IGNORE INTO users(user_id) VALUES(?)",
        (message.from_user.id,)
    )
    db.commit()

    await message.answer(
        "🚛 FARIDUN LOGISTIC BOT\n\n/yuk - yuk joylash"
    )

@dp.message(Command("yuk"))
async def yuk(message: Message):
    user_steps[message.from_user.id] = {"step": "route"}
    await message.answer("Yo‘nalish kiriting")

@dp.message()
async def handler(message: Message):

    uid = message.from_user.id

    if uid not in user_steps:
        return

    step = user_steps[uid]["step"]

    if step == "route":
        user_steps[uid]["route"] = message.text
        user_steps[uid]["step"] = "cargo"
        await message.answer("Yuk nomi?")
        return

    if step == "cargo":
        user_steps[uid]["cargo"] = message.text
        user_steps[uid]["step"] = "weight"
        await message.answer("Og‘irligi?")
        return

    if step == "weight":
        user_steps[uid]["weight"] = message.text
        user_steps[uid]["step"] = "truck"
        await message.answer("Nechta mashina?")
        return

    if step == "truck":
        user_steps[uid]["truck"] = message.text
        user_steps[uid]["step"] = "phone"
        await message.answer("Telefon?")
        return

    if step == "phone":

        data = user_steps[uid]

        text = f"""
🚛 FARIDUN LOGISTIC

📍Yo‘nalish:
➡️ {data['route']}

📦 Yuk: {data['cargo']}
⚖️ Og‘irligi: {data['weight']}
🚚 Kerak: {data['truck']}

👤 Kontakt: @{message.from_user.username}
📞 Aloqa: {message.text}
"""

        cursor.execute(
            "INSERT INTO loads(user_id,text) VALUES(?,?)",
            (uid, text)
        )
        db.commit()

        await message.answer("✅ Yuk saqlandi!")

        user_steps.pop(uid)

async def auto_send():
    while True:
        cursor.execute("SELECT text FROM loads")
        loads = cursor.fetchall()

        for load in loads:
            for group in GROUPS:
                try:
                    await bot.send_message(group, load[0])
                except:
                    pass

        await asyncio.sleep(600)

async def main():
    asyncio.create_task(auto_send())
    await dp.start_polling(bot)

asyncio.run(main())
