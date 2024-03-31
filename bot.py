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

# Переменная для отслеживания состояния секундомера
is_timer_running = False

# Список для хранения идентификаторов сообщений секундомера
timer_messages = []

# Словарь для связи названий упражнений с путями к изображениям
exercise_images = {
    "Грудь и трицепс": ["pictures/chest_triceps/1.jpg", "pictures/chest_triceps/2.jpg", "pictures/chest_triceps/3.jpg",
                        "pictures/chest_triceps/4.jpg", "pictures/chest_triceps/5.jpg", "pictures/chest_triceps/6.jpg"],
    # Добавьте здесь остальные упражнения
}

# Счетчик для отслеживания текущего индекса упражнения
current_exercise_index = 0


async def send_timer_messages(chat_id, seconds):
    global timer_messages
    while True:
        await asyncio.sleep(20)
        if not is_timer_running:  # Проверяем, нужно ли продолжать отправлять сообщения
            return
        message = await bot.send_message(chat_id, f"Прошло {seconds} секунд")
        timer_messages.append(message.message_id)  # Сохраняем идентификатор сообщения
        seconds += 20


@dp.message(F.text == "Грудь и трицепс")
async def chest_and_triceps(message: types.Message):
    global current_exercise_index
    photo_paths = exercise_images.get("Грудь и трицепс", [])
    if current_exercise_index < len(photo_paths):
        photo_path = photo_paths[current_exercise_index]
        await bot.send_photo(message.chat.id, photo=types.FSInputFile(photo_path))

        # Отправляем кнопки управления секундомером
        kb = [
            [types.KeyboardButton(text="Секундомер")],
            [types.KeyboardButton(text="Остановить секундомер")],
            [types.KeyboardButton(text="Следующее упражнение")],
            [types.KeyboardButton(text="Закончить тренировку")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        await message.answer("Упражнения закончились")
        current_exercise_index = 0
        await cmd_start(message)


@dp.message(F.text == "Следующее упражнение")
async def next_exercise(message: types.Message):
    global current_exercise_index
    current_exercise_index += 1
    await chest_and_triceps(message)  # Вызываем ту же функцию, чтобы показать следующее изображение упражнения

@dp.message(F.text == "Секундомер")
async def start_timer(message: types.Message):
    global is_timer_running, timer_messages
    is_timer_running = True
    response_message = await message.answer("Секундомер запущен. Через 20 секунд вы будете получать сообщения.")
    timer_messages.append(response_message.message_id)

    # Удаляем сообщение "Секундомер"
    await bot.delete_message(message.chat.id, message.message_id)

    await send_timer_messages(message.chat.id, 20)


@dp.message(F.text == "Остановить секундомер")
async def stop_timer(message: types.Message):
    global is_timer_running, timer_messages
    is_timer_running = False  # Останавливаем секундомер

    # Удаляем все сообщения секундомера
    for msg_id in timer_messages:
        await bot.delete_message(message.chat.id, msg_id,message.message_id)
    timer_messages = []  # Очищаем список идентификаторов
    await bot.delete_message(message.chat.id, message.message_id)

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Грудь и трицепс")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите группу мышц или управляйте секундомером:", reply_markup=keyboard)

@dp.message(F.text == 'Закончить тренировку')
async def workout_end(message: types.Message):
    await cmd_start(message)

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

