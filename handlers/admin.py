from mics import bot, dp
import models
import config
import markup
from models import Database

db = Database()
import text
from states import GetMessage,GetInfoUser
@dp.message_handler(text = "🔐Административная панель", chat_id = config.ADMIN)
async def message(message):
    await message.answer(
       text = 'Ваша админка',
       reply_markup = markup.admin_menu
       )


@dp.message_handler(text = "📩Рассылка", chat_id = config.ADMIN)
async def message(message):
    await message.answer(
            text = text.send_message_request,
            reply_markup = markup.cancel,
            parse_mode = 'Markdown'
        )       
        
    await GetMessage.photo_or_text.set()
    

@dp.message_handler(text = "📊Статистика", chat_id = config.ADMIN)
async def message(message):
    all_uset = len((await db.get_all_user_id()))
    await message.answer(
            text = text.get_all_user_message.format(all_uset),
            parse_mode = 'Markdown'
        )
@dp.message_handler(text = "ℹ️Пробить по базе", chat_id = config.ADMIN)
async def message(message):
    
    await message.answer(
            text = 'ℹ️Введите id пользователя',
            reply_markup = markup.cancel
        )
    await GetInfoUser.user_id.set()
@dp.message_handler(text = "◀️Назад", chat_id = config.ADMIN)
async def message(message):
    
    await message.answer(
            text = 'ℹ️Главное меню',
            reply_markup = markup.admin_menu_main
        )
    
        
        