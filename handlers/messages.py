from mics import bot, dp
from aiogram import types
from models import Database
import config
import text 
import markup
from states import SendToGroup
db = Database()
@dp.message_handler(text = '🛍 Каталог')
async def get_all_categories(message):
    await message.answer(
             text = text.all_categories_message,
             reply_markup = markup.all_categories_menu
        )
        
@dp.message_handler(content_types = types.ContentType.PHOTO)
async def create_item(message):
    photo_id = message.photo[-1].file_id
    item_info = message.caption.split('\n')
    print(item_info)
    await db.create_item(photo_id = photo_id, *item_info)
    
@dp.message_handler(text = "👥Партнёрская программа")
async def get_referal_system(message):
    await message.answer(
            text = text.referlas_system_message.format(
                     bot_username = config.TG_BOT_USERNAME,
                     user_id = message.from_user.id
                ),
            parse_mode = 'HTML'
        )
    


@dp.message_handler(text = "🏪 О магазине")
async def get_referal_system(message):
    await message.answer(
            text = text.about_shop_message
        )
        
@dp.message_handler(text = "🛒 Корзина")
async def get_first_item_in_bascket(message):
    item_bascket = await db.get_item_in_backet_by_user_id(message.chat.id)
    if not item_bascket:
       await message.answer(
            text = 'В вашей корзине пусто'
        )
       return
    await bot.send_photo(
         chat_id = message.chat.id,
         photo = item_bascket['photo_id'],
         caption = text.item_bascket_wrapper.format(
             item_name = item_bascket['item_name'],
             cost = item_bascket['cost'],
             qty = item_bascket['qty'],
             sum = item_bascket['cost'] * item_bascket['qty']
             
         ),
         parse_mode = 'HTML',
         reply_markup = await markup.basket_navigation_menu(item_bascket['item_name'],1,message.chat.id)
        )
        
@dp.message_handler(text = "📨 Техподдержка")   
async def get_referal_system(message):
    await message.answer(
            text = text.help_for_user,
            reply_markup = markup.cancel
        )
    await SendToGroup.message.set()
        