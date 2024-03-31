import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

# Объект бота
bot = Bot(token="7068234959:AAHvJKfcrpZkfnLmsT2d-BXgwriNuLdyiSo")

# Диспетчер
dp = Dispatcher()


@dp.message(F.text == 'Грудь и бицепс')
async def func1(message: types.Message):
    await message.answer("контент")

@dp.message(F.text == 'Спина и трицепс')
async def func2(message: types.Message):
    await message.answer("контент")

@dp.message(F.text == 'Ноги и плечи')
async def func3(message: types.Message):
    await message.answer("контент")


@dp.message(F.text == 'clear')
async def func(message: types.Message):
    await message.answer("Вы очистили клавиатуру", reply_markup=types.ReplyKeyboardRemove())


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Грудь и бицепс")],
        [types.KeyboardButton(text="Спина и трицепс")],
        [types.KeyboardButton(text="Ноги и плечи")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выбирите группу мышц!", reply_markup=keyboard)


# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
