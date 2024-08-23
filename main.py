from aiogram import *
from bd import db_start, create_profile, edit_profile
from sheets import zapis

days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
hours_of_day = [str(hour) for hour in range(9, 24)]

TOKEN = '7257951343:AAFeNnkcQq4qE5vqaus_feMVnIkRnoBGfBA'

storage = MemoryStorage()
bot = Bot(TOKEN)
dp = Dispatcher(bot, storage=storage)

confirmationanswer = ['Да', 'Нет']
days_of_week = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
hours_of_day = [str(hour) for hour in range(9, 24)]

class ProfileStatesGroup(StatesGroup):
    nameroom = State()
    weekday = State()
    hourr = State()

async def on_startup(__):
    await db_start()
    
def generate_keyboard(buttons):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for button in buttons:
        keyboard.add(KeyboardButton(text=button))
    return keyboard

@dp.message_handler(commands=['start'], state='*')
async def process_start_command(message: types.Message, state='*'):
    await ProfileStatesGroup.nameroom.set()
    await message.reply("Привет, это бот для записи на стирку, Напиши свою фамилию и комнату(например Иванов101")
    await create_profile(user_id=message.from_user.id)
    await ProfileStatesGroup.next()

@dp.message_handler(lambda message: message.text, state=ProfileStatesGroup.weekday)
async def process_nameroom_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['nameroom'] = message.text
    await message.reply("Теперь выбери день недели когда ты хотел бы записаться:", reply_markup=generate_keyboard(days_of_week))
    await ProfileStatesGroup.next()


@dp.message_handler(lambda message: message.text in days_of_week, state=ProfileStatesGroup.hourr)
async def process_day_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weekday'] = message.text
    await message.reply("Теперь выбери час дня:", reply_markup=generate_keyboard(hours_of_day))


@dp.message_handler(lambda message: message.text in hours_of_day, state=ProfileStatesGroup.hourr)
async def process_hour_command(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['hourr'] = message.text
    await edit_profile(state, user_id=message.from_user.id)
    await message.reply('Ты выбрал стирку в ' + f"{data['weekday']}" + ' в ' + f"{data['hourr']}" + ' часов' + ', все верно?', reply_markup=generate_keyboard(confirmationanswer))

    
@dp.message_handler(lambda message: message.text in confirmationanswer, state=ProfileStatesGroup.hourr)
async def confirm(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            zapis(f"{data['weekday']}", int(f"{data['hourr']}"), f"{data['nameroom']}")
        await message.reply("Отлично, записал!")
    else:
        await message.reply("Тогда начни с начала, /start")

@dp.message_handler(state='*')
async def handle_random_text(message: types.Message, state='*'):
    await message.reply("Извините, я не понимаю ваш запрос. Пожалуйста, выберите день недели и час дня, используя кнопки на клавиатуре и начните снова /start")

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
