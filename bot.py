import asyncio
import logging

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import InputFile

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="7068234959:AAHvJKfcrpZkfnLmsT2d-BXgwriNuLdyiSo")

# Диспетчер
dp = Dispatcher()


@dp.message(F.text == 'Грудь и бицепс')
async def func1(message: types.Message):
    photo_path = ("005.jpg")
    await bot.send_photo(message.chat.id, photo=types.FSInputFile(photo_path))


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Грудь и бицепс")]

    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выбирите группу мышц!", reply_markup=keyboard)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
