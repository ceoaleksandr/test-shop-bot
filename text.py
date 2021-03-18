from models import Database

db = Database() 




start_message = "Приветственное сообщение"

all_categories_message = "Выберите нужную категорию"

item_wrapper = """*▪️Категория* : {category}
*▪️Наименование* : {item_name}
*▪Цена *: {item_cost}₱
*▪️Описание* : {description}"""

item_bascket_wrapper = """🛒 Корзина

▪️<b>Наименование</b> : {item_name}
▪️<b>Цена </b> : {cost}
▪️<b>Количество</b> : {qty}
▪️<b>Сумма</b> : {cost} × {qty} = {sum}"""

referlas_system_message = """<b>👥Партнёрская программа :</b>

Получайте 10 % от покупок вашего реферала:

<b>Ваша ссылка </b>🔗
<code>https://t.me/{bot_username}?start={user_id}</code>"""

about_shop_message = 'нужен  текст'

choose_sex_message = "ℹ️Выберите ваш пол"
choose_age_message = 'ℹ️Выберите ваш возраст'

choose_color_message = "ℹ️Выберите ваши любимые цвета"

get_name = '▪️Введите ваше имя :'
get_location ='Введите или отправьте ваш адресс'
cancel_oreder_message = "❗️Вы отменили заказ"

order_text_item = """: 

▪️Название :{item_name}
▪️Цена :{cost} ₽
▪️Количество : {qty}
▪️Сумма : {sum} ₽
➖➖➖➖➖➖➖➖➖➖➖➖➖
"""
text_item_end = """
▪️ Подарочные баллы : {scrores} 
▪️ Купон : {coupon}
➖➖➖➖➖➖➖➖➖➖➖➖➖
▪️Итого : {all_sum} ₽"""

async def get_order_wrapper(items_bascket, id, coupon = None , scrores = None ):
    
    sum  = await db.get_sum_cost_bascket(id)
    if scrores:
        sum = sum - scrores
        scrores = f'{scrores} ₽'
    elif not scrores: 
        scrores = 'Не указан'
        
    text = 'Ваш заказ'
    if coupon:
        sum = sum - (sum*(coupon/100))
        coupon = f'{coupon} %'
    elif not coupon:
        coupon = 'Не указан'
        
    for item_bascket in items_bascket:
        text += order_text_item.format(
                item_name = item_bascket['item_name'],
                cost = item_bascket['cost'],
                qty = item_bascket['qty'],
                sum = item_bascket['cost'] * item_bascket['qty']
            )
    text+= text_item_end.format(
        scrores = scrores,
        coupon = coupon,
        all_sum = sum
        )
    return text
       
        
        
    
send_message_request = '✍ Отправьте сообщение для 📤 *Рассылки*'

button_request = '''*Чтобы добавить несколько кнопок в один ряд, пишите ссылки рядом с предыдущими.
Формат:*

[Первый текст + первая ссылка][Второй текст + вторая ссылка]

*Чтобы добавить несколько кнопок в строчку, пишите новые ссылки с новой строки.
Формат:*

[Первый текст + первая ссылка]
[Второй текст + вторая ссылка]'''

personal_cabinet = 'Ваши баллы {}'
button_request_err = 'ℹ️ *Ошибка в списке ссылок! Исправьте и попробуйте заново* ❗️'

get_all_user_message = 'ℹ️Всего пользователь {}'

admin_menu_message = 'Главное меню'


user_info="""ℹ️Новый заказ:

▫️Имя : {}
▫️id : {}
▫️username : @{}

▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️"""
 
new_m_user_info="""ℹ️Новое сообщение:

▫️Имя : {}
▫️id : `{}`
▫️username : @{}

▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️▪️"""
help_for_user = 'ℹ️Отправьте ваше сообщение. В ближайшее время администрация свяжется с вами'


pesronlal_info_for_user = """◼️ <a href='tg://user?id={}'>{}</a>
◼️ ID : {}
◼️Покупки : {}
◼️Всего рефералов : {}
◼️Приглашен : {}"""