import asyncio
import random

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    KeyboardButton,
    ReplyKeyboardMarkup,
)

TOKEN = "8951057518:AAE_1pJyh6Dut0o_iESUawpdueyVQG4hm-g"
bot = Bot(token=TOKEN) 

dp = Dispatcher()

games = {}
stats = {}
def get_stats(user_id):
    global stats

    if user_id not in stats:
        stats[user_id] = {
            "games": 0,
            "wins": 0,
            "attempts": 0
        }
    return stats[user_id]

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎮 Играть")],
        [KeyboardButton(text="📊 Статистика")],
        [KeyboardButton(text="⛔ Остановить игру")],
    ],
    resize_keyboard=True
)

def create_game(user_id):
    get_stats(user_id)["games"] += 1

    games[user_id] = {
        "number": random.randint(1, 100),
        "attempts": 0
    }

def stop_game(user_id):
    if user_id in games:
        del games[user_id]

@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "👋 Добро пожаловать!\n\n"
        "Я умею играть с тобой в игру 'Угадай число'.\n\n"
        "👇 Выбери действие:",
        reply_markup=main_keyboard
    )

async def start_new_game(message: Message):
    user_id = message.from_user.id

    if user_id in games:
        await message.answer("⚠️ У тебя уже идёт игра!")
        return

    create_game(user_id)

    await message.answer(
        "🎲 Я загадал число от 1 до 100!\n\n"
        "Попробуй угадать 😎"
    )

@dp.message(lambda message: message.text == "🎮 Играть")
async def start_game(message: Message):
    await start_new_game(message)

@dp.message(lambda message: message.text == "⛔ Остановить игру")
async def stop_game_handler(message: Message):
    user_id = message.from_user.id

    if user_id not in games:
        await message.answer("⚠️ У тебя нет активной игры.")
        return

    stop_game(user_id)

    await message.answer("🛑 Игра остановлена. Можешь начать заново 🎮") 

@dp.message(lambda message: message.text == "📊 Статистика")
async def stats_handler(message: Message):
    user_id = message.from_user.id
    user_stats = get_stats(user_id)

    await message.answer(
        "📊 Твоя статистика:\n\n"
        f"🎮 Игр сыграно: {user_stats['games']}\n"
        f"🏆 Побед: {user_stats['wins']}\n"
        f"🎯 Попыток всего: {user_stats['attempts']}"
    )


@dp.message()
async def guess(message: Message):
    user_id = message.from_user.id

    if user_id not in games:
        await message.answer("⚠️ У тебя нет активной игры. Нажми '🎮 Играть' чтобы начать.")
        return

    game_data = games[user_id]
    game_data["attempts"] += 1
    get_stats(user_id)["attempts"] += 1

    try:
        guess_number = int(message.text)
    except ValueError:
        await message.answer("Введи число от 1 до 100")
        return

    if guess_number < 1 or guess_number > 100:
        await message.answer("Только числа от 1 до 100")
        return

    if guess_number == game_data["number"]:
        await message.answer(
            f"🎉 Поздравляю! Ты угадал число {game_data['number']} за {game_data['attempts']}  попыток!\n\n"
        "👉 Нажми 📊 Статистика, чтобы посмотреть прогресс"
        )
        get_stats(user_id)["wins"] += 1

        del games[user_id]
    elif guess_number < game_data["number"]:
        await message.answer("Моё число больше ⬆️")
    else:
        await message.answer("Моё число меньше ⬇️")


async def main():
    print("BOT STARTED")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())