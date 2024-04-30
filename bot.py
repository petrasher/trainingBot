import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

logging.basicConfig(level=logging.INFO)

bot = Bot(token="6887683385:AAEh_RhX5QBR-zaD9N0vVJNFTbxsQfgqJ4w")

dp = Dispatcher()

is_timer_running = False

stop_event = asyncio.Event()

timer_messages = []

number_of_approaches = 1

seconds = 0

exercise_ct_images = {
    "Грудь и трицепс": ["pictures/chest_triceps/1.gif", "pictures/chest_triceps/2.gif", "pictures/chest_triceps/3.gif",
                        "pictures/chest_triceps/4.gif", "pictures/chest_triceps/5.gif", "pictures/chest_triceps/6.gif"]
}
exercise_bb_images = {
    "Спина и бицепс": ["pictures/back_biceps/1.jpg", "pictures/back_biceps/2.jpg", "pictures/back_biceps/3.jpg",
                       "pictures/back_biceps/4.jpg", "pictures/back_biceps/5.jpg"]
}
exercise_ls_images = {
    "Ноги и плечи": ["pictures/legs_shoulders/1.jpg", "pictures/legs_shoulders/2.jpg", "pictures/legs_shoulders/3.jpg",
                     "pictures/legs_shoulders/4.jpg", "pictures/legs_shoulders/5.jpg",
                     "pictures/legs_shoulders/6.jpg", "pictures/legs_shoulders/7.jpg",
                     "pictures/legs_shoulders/8.jpg", "pictures/legs_shoulders/9.jpg",
                     "pictures/legs_shoulders/10.jpg"]
}

current_exercise_ct_index = 0
current_exercise_bb_index = 0
current_exercise_ls_index = 0

async def send_timer_messages(chat_id, stop_event):
    global timer_messages, seconds
    try:
        while True:
            await asyncio.wait([asyncio.create_task(stop_event.wait())], timeout=20)
            if stop_event.is_set():
                break
            seconds += 20
            message = await bot.send_message(chat_id, f"Прошло {seconds} секунд")
            timer_messages.append(message.message_id)
    except Exception as e:
        print(f"An error occurred: {e}")
    print("stopped")
    return



@dp.message(F.text == "Грудь и трицепс")
async def chest_and_triceps(message: types.Message):
    await message.answer('Отдых между подходами 120-180 секунд, отдых между упражнениями 300 секунд')
    global current_exercise_ct_index, seconds
    seconds = 0
    photo_paths = exercise_ct_images.get("Грудь и трицепс", [])
    if current_exercise_ct_index < len(photo_paths):
        photo_path = photo_paths[current_exercise_ct_index]
        await bot.send_animation(message.chat.id, animation=types.FSInputFile(photo_path))

        kb = [
            [types.KeyboardButton(text="Начать/Завершить подход")],
            [types.KeyboardButton(text="Следующее упражнение")],
            [types.KeyboardButton(text="Закончить тренировку")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("ВЫБЕРИТЕ ДЕЙСТВИЕ: \n-----------------------------------------------------------------",
                             reply_markup=keyboard)
    else:
        await message.answer("Упражнения закончились")
        current_exercise_ct_index = 0
        await cmd_start(message)


@dp.message(F.text == "Спина и бицепс")
async def back_and_biceps(message: types.Message):
    await message.answer('Отдых между подходами 120-180 секунд, отдых между упражнениями 300 секунд')
    global current_exercise_bb_index, seconds
    seconds = 0
    photo_paths = exercise_bb_images.get("Спина и бицепс", [])
    if current_exercise_bb_index < len(photo_paths):
        photo_path = photo_paths[current_exercise_bb_index]
        await bot.send_photo(message.chat.id, photo=types.FSInputFile(photo_path))

        kb = [
            [types.KeyboardButton(text="Начать/Завершить подход")],
            [types.KeyboardButton(text="Следующее упражнение*")],
            [types.KeyboardButton(text="Закончить тренировку")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("ВЫБЕРИТЕ ДЕЙСТВИЕ: \n-----------------------------------------------------------------",
                             reply_markup=keyboard)
    else:
        await message.answer("Упражнения закончились")
        current_exercise_bb_index = 0
        await cmd_start(message)

@dp.message(F.text == "Ноги и плечи")
async def legs_and_shoulders(message: types.Message):
    await message.answer('Отдых между подходами 120-180 секунд, отдых между упражнениями 300 секунд.'' '
                         'Упражнения на ноги выполняются по одному подходу с перерывом в 20 секунд.')
    global current_exercise_ls_index, seconds, number_of_approaches
    seconds = 0
    photo_paths = exercise_ls_images.get("Ноги и плечи", [])
    if current_exercise_ls_index < len(photo_paths):
        photo_path = photo_paths[current_exercise_ls_index]
        await bot.send_photo(message.chat.id, photo=types.FSInputFile(photo_path))

        kb = [
            [types.KeyboardButton(text="Начать/Завершить подход")],
            [types.KeyboardButton(text="Следующее упражнение**")],
            [types.KeyboardButton(text="Закончить тренировку")]
        ]
        keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
        await message.answer("ВЫБЕРИТЕ ДЕЙСТВИЕ: \n-----------------------------------------------------------------",
                             reply_markup=keyboard)
    else:
        await message.answer("Упражнения закончились")
        current_exercise_ls_index = 0
        await cmd_start(message)



@dp.message(F.text == "Следующее упражнение")
async def next_ct_exercise(message: types.Message):
    global current_exercise_ct_index, seconds, stop_event, number_of_approaches
    current_exercise_ct_index += 1
    await chest_and_triceps(message)
    number_of_approaches = 1

    global is_timer_running, timer_messages
    if is_timer_running:
        is_timer_running = False
        stop_event.set()
        timer_messages = []
        seconds = 0


@dp.message(F.text == "Следующее упражнение*")
async def next_bb_exercise(message: types.Message):
    global current_exercise_bb_index, seconds, stop_event, number_of_approaches
    current_exercise_bb_index += 1
    await back_and_biceps(message)
    number_of_approaches = 1

    global is_timer_running, timer_messages
    if is_timer_running:
        is_timer_running = False
        stop_event.set()
        timer_messages = []
        seconds = 0
        number_of_approaches = 1


@dp.message(F.text == "Следующее упражнение**")
async def next_ls_exercise(message: types.Message):
    global current_exercise_ls_index, seconds, stop_event, number_of_approaches
    current_exercise_ls_index += 1
    await legs_and_shoulders(message)
    number_of_approaches = 1

    global is_timer_running, timer_messages
    if is_timer_running:
        is_timer_running = False
        stop_event.set()
        timer_messages = []
        seconds = 0



@dp.message(F.text == "Начать/Завершить подход")
async def toggle_timer(message: types.Message):
    global is_timer_running, number_of_approaches, start_message
    if not is_timer_running:
        is_timer_running = True
        start_message = await message.answer("Секундомер запущен. Каждые 20 секунд вы будете получать сообщения.")
        start_message = start_message.message_id
        await bot.delete_message(message.chat.id, message.message_id)
        stop_event.clear()  # Сбрасываем событие перед запуском
        await send_timer_messages(message.chat.id, stop_event)
    else:
        is_timer_running = False
        stop_event.set()  # Устанавливаем событие, чтобы остановить send_timer_messages
        await message.answer(f"Количество выполненных подходов: {number_of_approaches}")
        number_of_approaches += 1

        # Удаляем все сообщения о таймере и о начале подхода
        for msg_id in timer_messages:
            await bot.delete_message(message.chat.id, msg_id)
        timer_messages.clear()

        # Удаляем сообщение о начале подхода
        await bot.delete_message(message.chat.id, message.message_id)

        await bot.delete_message(message.chat.id, start_message)




@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = [
        [types.KeyboardButton(text="Грудь и трицепс")],
        [types.KeyboardButton(text="Спина и бицепс")],
        [types.KeyboardButton(text="Ноги и плечи")]
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await message.answer("Выберите группу мышц:", reply_markup=keyboard)


@dp.message(F.text == 'Закончить тренировку')
async def workout_end(message: types.Message):
    global is_timer_running, timer_messages, seconds, stop_event, number_of_approaches
    await cmd_start(message)
    number_of_approaches = 1

    if is_timer_running:
        is_timer_running = False
        stop_event.set()
        timer_messages = []
        seconds = 0

async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())