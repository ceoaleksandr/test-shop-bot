from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from models import Database
db = Database()

main_menu = ReplyKeyboardMarkup(resize_keyboard = True)
main_menu.add(
           KeyboardButton("🛍 Каталог"),
           KeyboardButton("🛒 Корзина")
    )
main_menu.add(
          KeyboardButton('👥Партнёрская программа'),
          KeyboardButton("💼 Личный кабинет")
    )
main_menu.add(
          KeyboardButton('🏪 О магазине'),
          KeyboardButton("📨 Техподдержка")
    )
admin_main_menu = ReplyKeyboardMarkup(resize_keyboard = True)
admin_main_menu.add(
           KeyboardButton("🛍 Каталог"),
           KeyboardButton("🛒 Корзина")
    )
admin_main_menu.add(
          KeyboardButton('👥Партнёрская программа'),
          KeyboardButton("💼 Личный кабинет")
    )
admin_main_menu.add(
          KeyboardButton('🏪 О магазине'),
          KeyboardButton("📨 Техподдержка")
    )
admin_main_menu.add(
        KeyboardButton('🔐Административная панель')
    )
admin_menu = ReplyKeyboardMarkup(resize_keyboard = True)
admin_menu.add(
    KeyboardButton('📩Рассылка'),
    KeyboardButton('📊Статистика')
        
    )
    
admin_menu.add(
    KeyboardButton('ℹ️Пробить по базе'),
    KeyboardButton('👤Доб. Админа')
    )    
    
admin_menu.add(
    KeyboardButton('🛒 История покупок'),
    KeyboardButton('🖋Написать юзеру')
    )
admin_menu.add(
    "◀️Назад"
    )    
all_categories_menu = InlineKeyboardMarkup()
all_categories_menu.add(
        InlineKeyboardButton(
            text = '👕Футболки',
            callback_data = "category_t-shirts_1"
        ),
        InlineKeyboardButton(
            text = '🧢 Кепки',
            callback_data = "category_caps_1"
        ),       
    )
all_categories_menu.add(
        InlineKeyboardButton(
            text = '👖Джинсы',
            callback_data = "category_jeans_1"
        ),
        InlineKeyboardButton(
            text = '👟Кросовки',
            callback_data = "category_sneakers_1"
        ),       
    )
    
all_categories_menu.add(
        InlineKeyboardButton(
            text = '🧦Носки',
            callback_data = "category_socks_1"
        )
    )    
    
async def get_item_navigation_menu(category_name,item_name, pos):
    menu = InlineKeyboardMarkup()
    back_pos = pos - 1
    if pos == 1:
        back_pos = 5
    next_pos = pos+1    
    if pos == 5:
        next_pos = 1
    menu.add(
            InlineKeyboardButton(
                text = "◀️" ,
                callback_data = f"category_{category_name}_{back_pos}"
            ),
            InlineKeyboardButton(
                text = "▶️" ,
                callback_data = f"category_{category_name}_{next_pos}"
            )            
        )
    menu.add(
            InlineKeyboardButton(
               text = '🛒 Добавить в корзину',
               callback_data = f'add_to_cart_{item_name}'
        )
      )
    return menu

choose_sex_menu = InlineKeyboardMarkup()
choose_sex_menu.add(
        InlineKeyboardButton(
                text = 'Мужской',
                callback_data = 'sex_Мужской'
            ),
        InlineKeyboardButton(
                text = 'Женский',
                callback_data = 'sex_Женский'
            )            
    )
    
choose_age_menu = InlineKeyboardMarkup()
choose_age_menu.add(
        InlineKeyboardButton(
                text = 'до 20',
                callback_data = 'age_до 20'
            ),
        InlineKeyboardButton(
                text = '20-30',
                callback_data = 'age_30-20'
            ),
        InlineKeyboardButton(
                text = 'более 30',
                callback_data = 'age_более 30'
            )                        
    ) 
async def choose_color_menu(choosen_color = []):   
    menu = InlineKeyboardMarkup(row_width = 4)
    colors = [['⚫️', 'Черный'],['🔴', 'Красный'],['⚪️', 'Белый'],['🟢', 'Зеленый']]
    finaly_menu = []
    for color in colors:
        if color[1] in choosen_color:
           finaly_menu.append(
                InlineKeyboardButton(
                    text = '☑️',
                    callback_data = 'pass'
                    ) 
                )
        else:
             finaly_menu.append(
                 InlineKeyboardButton(
                     text = color[0],
                     callback_data = f'color_{color[1]}'
                        )
                 )
    menu.add(
         *finaly_menu
        )
    menu.add(
            InlineKeyboardButton(
                    text = '✅ Подтвердить',
                    callback_data = 'set_colors'
                )
        )
    return menu

async def basket_navigation_menu(item_name, pos, id):
    last_pos = await db.get_last_position_bascket(id)
    sum = await db.get_sum_cost_bascket(id)
    next_pos = pos+1
    back_pos = pos-1
    print(last_pos)
    if pos == last_pos:
       next_pos = 1
    elif pos <=1:
        
        back_pos = last_pos
    menu = InlineKeyboardMarkup()
    menu.add(
            InlineKeyboardButton(
                text = '🔺',
                callback_data = f'add_qty_item_{item_name}_{pos}'
                ),
            InlineKeyboardButton(
                text = '❌',
                callback_data = f'delete_from_bascket_{item_name}'
                ),
            InlineKeyboardButton(
                text = '🔻',
                callback_data = f'take_away_qty_item_{item_name}_{pos}'
                ),            
                
        )
    menu.add(
            InlineKeyboardButton(
                text = '◀️',
                callback_data = f'bascket_item_pos_{back_pos}'
                ),
            InlineKeyboardButton(
                text = '1/2',
                callback_data = 'test'
                ),
            InlineKeyboardButton(
                text = '▶️',
                callback_data = f'bascket_item_pos_{next_pos}'
                ),            
        )    
    menu.add(
            InlineKeyboardButton(
                text =f'✅ Оформить заказ нa {sum}?',
                callback_data = 'order'
                )
              )
    menu.add(
            InlineKeyboardButton(
                text ='🛍 Проложить покупки',
                callback_data = 'catalog'
                )
           )
    return menu


calncel = ReplyKeyboardMarkup(resize_keyboard = True)
calncel.add(
        KeyboardButton('🚫 Отмена')
  
    )
    
get_lacation_menu = ReplyKeyboardMarkup(resize_keyboard = True)
get_lacation_menu.add(
        KeyboardButton('📍 Отправить геолокация',request_location = True)
  
    )
get_lacation_menu.add(
        KeyboardButton('🚫 Отмена')
  
    )
    
add_buttons = ReplyKeyboardMarkup(resize_keyboard = True)
add_buttons.add(
        KeyboardButton('📤 Отправить сообщение'),
)
add_buttons.add(
         KeyboardButton('☑️ Добвить инлайн кнопки'),
    )

add_buttons.add(
        KeyboardButton('🚫 Отмена')
    )
    
    
async def create_markup(markpus):
    menu = InlineKeyboardMarkup()
    for markpup in markpus:
        
        ii = [markpup.split(' | ')]
        num = 0
        for i in ii:
            if len(i) > 1:
                markup1 = i[0].split(' - ')
                markup2 = i[1].split(' - ')
                menu.add(
                       InlineKeyboardButton(
                           text = markup1[0],
                           url  = markup1[1]
                           ),
                       InlineKeyboardButton(
                           text = markup2[0],
                           url = markup2[1]
                           )
                )
            else:
                markup1 = i[0].split(' - ')
             
                menu.add(
                       InlineKeyboardButton(
                           text = markup1[0],
                           url  = markup1[1]
                           ),
                        )
                
                
                
    return menu
inline_back_button = InlineKeyboardMarkup()
inline_back_button.add(
        InlineKeyboardButton(
            text = '🔙 Назад',
            callback_data = 'back'
            )
    
    )
    

get_actions = ReplyKeyboardMarkup(resize_keyboard = True)


get_actions.add(
        KeyboardButton('✅ Подтверждаю')
    )

get_actions.add(
        KeyboardButton('🚫 Отмена')
    ) 
    
cancel = ReplyKeyboardMarkup(resize_keyboard = True)
cancel.add(
        KeyboardButton('🚫 Отмена')
    )    
    
    
confim_order = ReplyKeyboardMarkup(resize_keyboard = True)
confim_order.add('✅ Подтверждаю')

