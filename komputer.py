import logging
from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv
from function import KA
import os
load_dotenv('.env')

API_TOKEN: str = os.getenv('TOKEN')
admin_id: int = int(os.getenv('ADMIN_ID'))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    if message.from_user.username:
        info = f"username: @{message.from_user.username} \n ID: {user_id}"
        await bot.send_message(admin_id, info)
    else:
        info = f"full name: {message.from_user.full_name} \n ID: {user_id}"
        await bot.send_message(admin_id, info)
    text = f"Assalomu alaykum <b>{message.from_user.full_name}</b>.\n"
    text += f"Kompyuter arxitekturasi fanidan ma'lumotlarni olishingiz uchun sizga linklar yuboraman.\n"
    text += f"Linklar nomiga qarab sizga kerakli ma'lumot nomini ko'rgan linkning ustiga bosing "
    text += f" va sizga <b>Google Cloud</b>ga yuklangan maruza matnlari beriladi.\n"
    text += f"Shu linklar bo'yicha kerakli ma'lumotlarni ko'rishingiz mumkin."
    await message.reply(text)
    for ka in KA:
        await bot.send_message(user_id, text=f"<a href='{ka['link']}'>{ka['name']}</a>")


@dp.message_handler(commands=['admin', 'developer'])
async def admins(message: types.Message):
    user_id = message.from_user.id
    if message.from_user.username:
        info = f"<b>username:</b> @{message.from_user.username} \n <b>ID:</b> {user_id}" \
               f"\n <b>User:</b> Siz bilan Bog'lanmoqchi."
        await bot.send_message(admin_id, info)
        await message.reply("Siz bilan admin tez oraqa bog'lanadi.")
    else:
        info = f"<b>full name:</b> {message.from_user.full_name} \n <b>ID:</b> {user_id}" \
               f"\n <b>User: Siz bilan bog'lanmoqchi.</b>\n Undan nomerini so'radim."
        await bot.send_message(admin_id, info)
        await message.reply("Siz bilan admin tez oraqa bog'lanadi. Iloji bo'lsa telefon nomerizni yozivoring. ")


@dp.message_handler()
async def echo(message: types.Message):
    user_id = message.from_user.id
    await bot.send_message(admin_id, f"<b>ID:</b> {user_id} \n <b>Messages:<b/> {message.text}")
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
