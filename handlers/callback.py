from mics import bot, dp
from models import Database
import text
import markup 
import asyncio
from states import Order
db = Database()
@dp.callback_query_handler(lambda call: call.data[:9] == 'category_')
async def get_items_by_category(query):
    category_name = query.data.split("_")[1]
    pos = int(query.data.split("_")[2])
    await bot.delete_message(
        chat_id = query.message.chat.id,
        message_id = query.message.message_id
        )
    item = await db.get_item_by_category(category_name, pos)
    await bot.send_photo(
       chat_id = query.message.chat.id,
       photo = item['photo_id'],
       caption = text.item_wrapper.format(
                category = item['category'],
                item_name = item['item_name'],
                item_cost = item['cost'],
                description = item['description']
           ),
       parse_mode = 'Markdown',
       reply_markup = await markup.get_item_navigation_menu(category_name,item['item_name'],pos)
       
       )

@dp.callback_query_handler(lambda call:call.data[:12] == 'add_to_cart_')
async def add_to_cart(query):
    item_name = query.data[12:]
    is_item_in_bascket = await db.get_bascket_item_by_name_for_user(query.message.chat.id, item_name)
    if is_item_in_bascket :
        pass
    else:
        cost = (await db.get_cost_by_item_name(item_name))
        photo = (await db.get_photo_by_item_name(item_name))
        await db.add_item_to_backet(query.message.chat.id, item_name, cost, photo)

    
    await bot.answer_callback_query(callback_query_id = query.id , show_alert = True , text = '✅ Ваш товар уже в корзине')        


@dp.callback_query_handler(lambda call: call.data[:20] == 'delete_from_bascket_')
async def update_item_cart(query):
    await bot.delete_message(
            chat_id = query.message.chat.id,
            message_id = query.message.message_id,
            )    
    delete_item_name = query.data[20:]
    await db.delete_item_from_bascket(query.message.chat.id, delete_item_name)
    item_bascket = await db.get_item_in_backet_by_user_id(query.message.chat.id)
    if not item_bascket:

       await query.message.answer(
            text = 'В вашей корзине пусто'
        )
       return
    await bot.send_photo(
         chat_id = query.message.chat.id,
         photo = item_bascket['photo_id'],
         caption = text.item_bascket_wrapper.format(
             item_name = item_bascket['item_name'],
             cost = item_bascket['cost'],
             qty = item_bascket['qty'],
             sum = item_bascket['cost'] * item_bascket['qty']
             
         ),
         parse_mode = 'HTML',
         reply_markup = await markup.basket_navigation_menu(item_bascket['item_name'],1,query.message.chat.id)
        )    
        
@dp.callback_query_handler(lambda call: call.data[:19] == 'take_away_qty_item_')
async def update_item_cart(query):
    item_name = query.data[19:].split('_')[0]
    pos = int(query.data[19:].split('_')[1])
    item_bascket = await db.get_bascket_item_by_name_for_user(query.message.chat.id, item_name)
    if item_bascket['qty'] <= 1:
        return  
    await db.update_bascket_item_qty(query.message.chat.id, item_name ,-1)
   
    
    await bot.edit_message_caption(
         chat_id = query.message.chat.id,
         message_id = query.message.message_id,
         caption = text.item_bascket_wrapper.format(
             item_name = item_bascket['item_name'],
             cost = item_bascket['cost'],
             qty = item_bascket['qty']-1,
             sum = item_bascket['cost'] * item_bascket['qty']          
        ),
         parse_mode = 'HTML',
         reply_markup = await markup.basket_navigation_menu(item_bascket['item_name'],pos,query.message.chat.id)
         )

@dp.callback_query_handler(lambda call: call.data[:13] == 'add_qty_item_')
async def update_item_cart(query):
    print(query.data[13:])
    item_name = query.data[13:].split('_')[0]
    pos = int(query.data[13:].split('_')[1])
    item_bascket = await db.get_bascket_item_by_name_for_user(query.message.chat.id, item_name)
    await db.update_bascket_item_qty(query.message.chat.id, item_name ,1)
    await asyncio.sleep(0.5)
    
    await bot.edit_message_caption(
         chat_id = query.message.chat.id,
         message_id = query.message.message_id,
         caption = text.item_bascket_wrapper.format(
             item_name = item_bascket['item_name'],
             cost = item_bascket['cost'],
             qty = item_bascket['qty']+1,
             sum = item_bascket['cost'] * item_bascket['qty']          
        ),
         parse_mode = 'HTML',
         reply_markup = await markup.basket_navigation_menu(item_bascket['item_name'],pos,query.message.chat.id)
         )
         
@dp.callback_query_handler(lambda call: call.data[:17] == 'bascket_item_pos_')
async def update_item_cart(query):
    pos = int(query.data[17:])
    await bot.delete_message(
        chat_id = query.message.chat.id,
        message_id = query.message.message_id,
        )
    
    item_bascket = await db.get_item_in_backet_by_user_id(query.message.chat.id,pos)
    await bot.send_photo(
         chat_id = query.message.chat.id,
         photo = item_bascket['photo_id'],
         caption = text.item_bascket_wrapper.format(
             item_name = item_bascket['item_name'],
             cost = item_bascket['cost'],
             qty = item_bascket['qty'],
             sum = item_bascket['cost'] * item_bascket['qty']
             
         ),
         parse_mode = 'HTML',
         reply_markup = await markup.basket_navigation_menu(item_bascket['item_name'],pos,query.message.chat.id)
        )
        
@dp.callback_query_handler(text = 'order')
async def order_statrt(query):
    await bot.delete_message(
          chat_id = query.message.chat.id,
          message_id = query.message.message_id
        )
    await query.message.answer(
          text = text.get_name,
          reply_markup = markup.calncel
       )
    await Order.name.set()
       
       
@dp.callback_query_handler(text = 'catalog')
async def catalog(query):
    await bot.delete_message(
          chat_id = query.message.chat.id,
          message_id = query.message.message_id
        )    
    await query.message.answer(
             text = text.all_categories_message,
             reply_markup = markup.all_categories_menu
        )
