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
exercise_ct_images = {
    "Грудь и трицепс": ["pictures/chest_triceps/1.gif", "pictures/chest_triceps/2.gif", "pictures/chest_triceps/3.gif",
                        "pictures/chest_triceps/4.gif", "pictures/chest_triceps/5.gif", "pictures/chest_triceps/6.gif"],
    # Добавьте здесь остальные упражнения
}
exercise_bb_images = {
    "Спина и бицепс": ["pictures/back_biceps/1.jpg", "pictures/back_biceps/2.jpg", "pictures/back_biceps/3.jpg",
                       "pictures/back_biceps/4.jpg", "pictures/back_biceps/5.jpg"],
}

# Счетчик для отслеживания текущего индекса упражнения
current_exercise_ct_index = 0
current_exercise_bb_index = 0


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
    await message.answer('Отдых между подходами 2-3 минуты')
    global current_exercise_ct_index
    photo_paths = exercise_ct_images.get("Грудь и трицепс", [])
    if current_exercise_ct_index < len(photo_paths):
        photo_path = photo_paths[current_exercise_ct_index]
        await bot.send_animation(message.chat.id, animation=types.FSInputFile(photo_path))

        # Отправляем кнопки управления секундомером
        kb = [
            [types.KeyboardButton(text="Запустить секундомер")],
            [types.KeyboardButton(text="Остановить секундомер")],
            [types.KeyboardButton(text="Следующее упражнение")],
            [types.KeyboardButton(text="Закончить тренировку")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        await message.answer("Упражнения закончились")
        current_exercise_ct_index = 0
        await cmd_start(message)


@dp.message(F.text == "Спина и бицепс")
async def back_and_biceps(message: types.Message):
    await message.answer('Отдых между подходами 2-3 минуты')
    global current_exercise_bb_index
    photo_paths = exercise_bb_images.get("Спина и бицепс", [])
    if current_exercise_bb_index < len(photo_paths):
        photo_path = photo_paths[current_exercise_bb_index]
        await bot.send_photo(message.chat.id, photo=types.FSInputFile(photo_path))

        # Отправляем кнопки управления секундомером
        kb = [
            [types.KeyboardButton(text="Запустить секундомер")],
            [types.KeyboardButton(text="Остановить секундомер")],
            [types.KeyboardButton(text="Следующее упражнение*")],
            [types.KeyboardButton(text="Закончить тренировку")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("Выберите действие:", reply_markup=keyboard)
    else:
        await message.answer("Упражнения закончились")
        current_exercise_bb_index = 0
        await cmd_start(message)


@dp.message(F.text == "Следующее упражнение")
async def next_ct_exercise(message: types.Message):
    global current_exercise_ct_index
    current_exercise_ct_index += 1
    await chest_and_triceps(message)  # Вызываем ту же функцию, чтобы показать следующее изображение упражнения

    global is_timer_running, timer_messages
    is_timer_running = False  # Останавливаем секундомер
    timer_messages = []


@dp.message(F.text == "Следующее упражнение*")
async def next_bb_exercise(message: types.Message):
    global current_exercise_bb_index
    current_exercise_bb_index += 1
    await back_and_biceps(message)  # Вызываем ту же функцию, чтобы показать следующее изображение упражнения

    global is_timer_running, timer_messages
    is_timer_running = False  # Останавливаем секундомер
    timer_messages = []


@dp.message(F.text == "Запустить секундомер")
async def start_timer(message: types.Message):
    global is_timer_running, timer_messages
    is_timer_running = True
    response_message = await message.answer("Секундомер запущен. Каждые 20 секунд вы будете получать сообщения.")
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
        await bot.delete_message(message.chat.id, msg_id, message.message_id)
    await bot.delete_message(message.chat.id, message.message_id)
    timer_messages = []


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Грудь и трицепс")],
        [types.KeyboardButton(text="Спина и бицепс")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите группу мышц:", reply_markup=keyboard)


@dp.message(F.text == 'Закончить тренировку')
async def workout_end(message: types.Message):
    await cmd_start(message)


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
