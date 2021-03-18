from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram import types
from mics import dp , bot
from models import Database
from states import (UserProfile)
import config
import text
import markup
db = Database()
@dp.message_handler(CommandStart(), chat_id =  config.ADMIN)
async def welcome(message):
    await message.answer(
             text = text.start_message,
             reply_markup = markup.admin_main_menu,
             parse_mode = 'Markdown'
        )    
        
@dp.message_handler(CommandStart())
async def welcome(message):
    
    await db.create_table_backet()
    await db.create_item_table()
    await db.create_users_table()
    is_authentication = await db.authentication(message.chat.id, message.from_user.first_name)
    if not is_authentication:
        await UserProfile.sex.set()
        await message.answer(
              text = text.choose_sex_message,
              reply_markup = markup.choose_sex_menu
            )
        return
    await message.answer(
             text = text.start_message,
             reply_markup = markup.main_menu,
             parse_mode = 'Markdown'
        )
        
