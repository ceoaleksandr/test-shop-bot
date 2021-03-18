from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from mics import dp , bot
from models import Database
from aiogram import types
import text
import markup
import datetime
import random
import config

db = Database()
class GetInfoUser(StatesGroup):
    user_id = State()
    
class UserProfile(StatesGroup):
    sex = State()
    age = State()
    color = State()
    
class GetMessage(StatesGroup):
    photo_or_text = State()
    get_action = State() 
    button = State()
    add_buttons = State()    
    
class Order(StatesGroup):
    name = State()
    location = State()
    confim = State()

class SendToGroup(StatesGroup):
    message = State()

@dp.callback_query_handler(lambda call : call.data[:4] == "sex_", state = UserProfile.sex )
async def upload_sex(query, state):
    sex_user = query.data[4:]
    await db.update_user_sex(query.message.chat.id , sex_user)
    await bot.edit_message_text(
          chat_id = query.message.chat.id,
          message_id= query.message.message_id,
          text = text.choose_age_message,
          reply_markup = markup.choose_age_menu
        )
    await UserProfile.age.set()
    
@dp.callback_query_handler(lambda call : call.data[:4] == "age_", state = UserProfile.age )
async def upload_color(query, state):
    age_user = query.data[4:]
    await db.update_user_age(query.message.chat.id, age_user)
    await bot.edit_message_text(
          chat_id = query.message.chat.id,
          message_id=query.message.message_id,
          text = text.choose_color_message,
          reply_markup =await markup.choose_color_menu()
        )
    await UserProfile.color.set()
    
@dp.callback_query_handler(lambda call : call.data[:6] == "color_", state = UserProfile.color )
async def upload_color(query, state):
    select_color = query.data[6:]
    colors = await db.get_user_favorite_colors(query.message.chat.id)
    colors.append(select_color)
    await db.update_user_favorite_colors(query.message.chat.id, colors)
    await bot.edit_message_text(
          chat_id = query.message.chat.id,
          message_id=query.message.message_id,
          text = text.choose_color_message,
          reply_markup = await markup.choose_color_menu(colors)
        )
    
    
@dp.callback_query_handler(text = 'set_colors',state = UserProfile.color)  
async def set_colors(query  , state):
    await bot.delete_message(
        chat_id = query.message.chat.id,
        message_id = query.message.message_id,    
        )
    await query.message.answer(
        text = text.start_message,
        reply_markup = markup.main_menu,
        parse_mode = 'Markdown'
       )
    await state.finish()
    
    



@dp.message_handler(text = '🚫 Отмена', state = Order.name)
async def cancel_name_user(message, state):
   
    await message.answer(
          text = text.cancel_oreder_message,
          reply_markup = markup.main_menu
        )
    await state.finish()
    
@dp.message_handler(content_types = types.ContentType.TEXT, state = Order.name)
async def cancel_name_user(message, state):
    await state.update_data(name = message.text)
    await message.answer(
          text = text.get_location,
          reply_markup = markup.get_lacation_menu
        )
    await Order.location.set()
    
    
@dp.message_handler(text = '🚫 Отмена', state = Order.location)
async def cancel_name_user(message, state):
   
    await message.answer(
          text = text.cancel_oreder_message,
          reply_markup = markup.main_menu
        )
    await state.finish()
    
@dp.message_handler(content_types = types.ContentType.LOCATION, state = Order.location)
async def cancel_name_user(message, state):
    location = message.location
    bascket_items = await db.get_all_item_in_backet_by_user_id(message.chat.id) 
    await state.update_data(location_latitude = location.latitude,location_longitude = location.longitude)
    await message.answer(
          text = await text.get_order_wrapper(bascket_items, message.chat.id),
          reply_markup = markup.confim_order
        )
    await Order.confim.set()    
    
@dp.message_handler(text = '✅ Подтверждаю' ,state = Order.confim)
async def cancel_name_user(message, state):
  
    bascket_items = await db.get_all_item_in_backet_by_user_id(message.chat.id) 
    bascket_info = await text.get_order_wrapper(bascket_items, message.chat.id)
    await bot.send_message(
        chat_id= -1001424223693,
        text = text.user_info.format(message.from_user.firstname, message.from_user.id, message.from_user.username)+'\n'+bascket_info
        )
   
    
    await message.answer(
          text = 'Ваш заказ прият',
          reply_markup = markup.main_menu
        )
    await state.finish()  
    
@dp.message_handler(text = 'Отмена', state = Order.confim)
async def cancel_name_user(message, state):
  
    
    await state.update_data(location_latitude = location.latitude,location_longitude = location.longitude)
    await message.answer(
          text = 'Главное меню',
          reply_markup = markup.main_menu
        )
    await state.finish()         
@dp.callback_query_handler(lambda : call.data[:18]  == 'order_with_scrores', state = Order.location)
async def get_order_whith_scrores(query):
    pass

            
@dp.message_handler(state = GetMessage.photo_or_text, text = '🚫 Отмена')
async def answer(message : types.Message, state):
    await state.finish()
    await message.answer(
            text = text.admin_menu_message,
            reply_markup = markup.admin_menu,
            parse_mode = 'Markdown'
        )   
async def sendler_messages(list, state, ):
    if state['photo']:
     
       for lz in list:
          try: 
             await bot.send_photo(chat_id = lz['user_id'], photo = state['file_id'], caption = state['caption'], parse_mode = 'Markdown')
           
          except :
             pass

    elif not state['photo']:
       for lz in list:
          try: 
             await bot.send_message(
                 chat_id = lz['user_id'], 
                 text = state['text'],
                 parse_mode = 'Markdown'
                 )
          except :
             pass            

async def sendler_messages_with_markup(list, state,mark ):
    if state['photo']:
     
       for lz in list:
          try: 
             await bot.send_photo(chat_id = lz['user_id'], photo = state['file_id'], caption = state['caption'], parse_mode = 'Markdown', reply_markup = mark)
           
          except :
             pass

    elif not state['photo']:
       for lz in list:
          try: 
             await bot.send_message(
                 chat_id = lz['user_id'], 
                 text = state['text'],
                 parse_mode = 'Markdown',
                 reply_markup = mark
                 )
          except :
             pass                     

        
@dp.message_handler(state = GetMessage.photo_or_text, content_types = types.ContentType.TEXT)
async def answer(message : types.Message, state):
    
    await message.answer(
          message.text
        )
    await message.answer(
           text = '✔️Сообщение успешно добавлено',
           reply_markup = markup.add_buttons
        )
    await state.update_data(text = message.text , photo = False)
    await GetMessage.button.set()
   

@dp.message_handler(state = GetMessage.photo_or_text, content_types = types.ContentType.PHOTO)
async def answer(message : types.Message, state):
        
        await message.answer(
           text = '✔️Сообщение успешно добавлено',
           reply_markup = markup.add_buttons
        )
        await state.update_data(
            text = message.text , 
            photo = True, 
            file_id = message.photo[-1].file_id, 
            caption = message.caption,
            parse_mode = 'Markdown'
            )
        await GetMessage.button.set()    

@dp.message_handler(state = GetMessage.button, text = '🚫 Отмена')
async def answer(message : types.Message, state):
    await state.finish()
    await message.answer(
            text = text.admin_menu_message,
            reply_markup = markup.admin_menu,
            parse_mode = 'Markdown'
        )   
        
@dp.message_handler(state = GetMessage.button, text = '📤 Отправить сообщение')
async def answer(message : types.Message, state):
    stats = await state.get_data()
    ls = await db.get_all_user_id()
    await state.finish()
    await sendler_messages(ls ,stats)
    await message.answer(
           text = 'ℹ️Рассылка началась!!!',
           reply_markup = markup.admin_menu
        )
        
@dp.message_handler(state = GetMessage.button, text = '☑️ Добвить инлайн кнопки')
async def answer(message : types.Message, state):        
    await GetMessage.add_buttons.set()
    await message.answer(
            text = text.button_request,
            reply_markup = markup.cancel,
            parse_mode = 'Markdown'
        )
        
@dp.message_handler(state = GetMessage.add_buttons, text = '🚫 Отмена')
async def answer(message : types.Message, state):
    await GetMessage.button.set()
    await message.answer(
            text = 'Выберите действие',
            reply_markup = markup.add_buttons,
            parse_mode = 'Markdown'
        )   
@dp.message_handler(state = GetMessage.add_buttons, content_types = types.ContentType.TEXT)
async def answer(message : types.Message, state):
    markups = []
    answer = message.text.split('\n')
    print(answer)
    for i in answer:
        for j in i.split('\n'):
            markups.append(j)
    states = await state.get_data()
    try:
       button = await markup.create_markup(answer)
    except :
        await message.answer(
                text = '❌Ошибка ,вы ввели не правильно', 
            )
        return
        
    
    if not states['photo']:
           await message.answer(
                text = states['text'],
                reply_markup = button
            )
    elif states['photo']:
             await bot.send_photo(
                 message.chat.id,
                 photo = states['file_id'],
                 caption = states['caption'],
                 parse_mode = 'Markdown',
                 reply_markup = button
             )
    await GetMessage.get_action.set()
    await state.update_data(markup = button)
    await message.answer(
            text = 'Подтвердите отпрвку сообщения',
            reply_markup = markup.get_actions
        )
      
@dp.message_handler(state = GetMessage.get_action, text = '🚫 Отмена')
async def answer(message : types.Message, state):
    await state.finish()
    await message.answer(
            text = text.admin_menu_message,
            reply_markup = markup.admin_menu,
            parse_mode = 'Markdown'
        )
        
@dp.message_handler(state = SendToGroup.message, text = '🚫 Отмена')
async def answer(message : types.Message, state):
    await state.finish()
    await message.answer(
            text = 'Главное меню',
            reply_markup = markup.main_menu,
            parse_mode = 'Markdown'
        )
@dp.message_handler(state = SendToGroup.message, content_types = types.ContentType.TEXT , chat_id = config.ADMIN)
async def answer(message : types.Message, state):
    await state.finish()
    await bot.send_message(
          chat_id = -1001424223693,
          text = text.new_m_user_info.format(message.from_user.first_name, message.from_user.id, message.from_user.username, ),
          parse_mode = 'Markdown'
        )
    await bot.send_message(
          chat_id = -1001424223693,
          text = message.text,
          parse_mode = 'Markdown'
        )        
    await message.answer(
            text = 'Сообщенте отправлено',
            reply_markup = markup.admin_menu_main,
            parse_mode = 'Markdown'
        )
    await state.finish()        
    
@dp.message_handler(state = SendToGroup.message, content_types = types.ContentType.TEXT)
async def answer(message : types.Message, state):
    await state.finish()
    await bot.send_message(
          chat_id = -1001424223693,
          text = text.new_m_user_info.format(message.from_user.first_name, message.from_user.id, message.from_user.username, ),
          parse_mode = 'Markdown'
        )
    await bot.send_message(
          chat_id = -1001424223693,
          text = message.text,
          parse_mode = 'Markdown'
        )        
    await message.answer(
            text = 'Сообщенте отправлено',
            reply_markup = markup.main_menu,
            parse_mode = 'Markdown'
        )
    await state.finish()

@dp.message_handler(state = GetMessage.get_action, text = '✅ Подтверждаю')
async def answer(message : types.Message, state):
    markups = await state.get_data()
    await state.finish()
    await message.answer(
            text = text.admin_menu_message,
            reply_markup = markup.admin_menu,
            parse_mode = 'Markdown'
        )   
    users_id = await db.get_all_user_id()
    await sendler_messages_with_markup(users_id, markups, markups['markup'])

@dp.message_handler(state = GetInfoUser.user_id, text = '🚫 Отмена')
async def answer(message : types.Message, state):
    await state.finish()
    await message.answer(
            text = 'Главное меню',
            reply_markup = markup.admin_menu,
            parse_mode = 'Markdown'
        )
        
@dp.message_handler(state = GetInfoUser.user_id, content_types = types.ContentType.TEXT)
async def answer(message : types.Message, state):
    try:
        user_info = await db.get_info(message.chat.id)
    except:
        await message.answer(
               'Пользователя нет в базе'
            )
        return
    if not user_info:
        await message.answer(
               'Пользователя нет в базе'
            )
        return
    await message.answer(
          text = text.pesronlal_info_for_user.format(
                user_info['user_id'],
                user_info['name'],
                user_info['user_id'],
                0,
                user_info['referals'],
                user_info['refid'],
                 
              ),
           parse_mode ='HTML'
          
        )
      
    