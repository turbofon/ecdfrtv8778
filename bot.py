API_TOKEN = '7903466278:AAEztSGUXfkc2lwK6OPD_Eeve0tB4NDAqgU'

from aiogram import Bot, types, Dispatcher
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.methods import edit_message_text
from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery, Message
from aiogram.enums import ParseMode 
import asyncio

from modules.ip import ip_detect
from modules.phone import russia_num, phnum_parse
from modules.base1 import base1_by_email, base1_by_fio, base1_by_phone
from modules.base2 import base2
from modules.getcontact import get_contact
from modules.base_big import full_search
from modules.osint import social_search, get_telegram_by_username
from aiogram.client.default import DefaultBotProperties
from subs import *

from art import tprint

# Диспетчер
dp = Dispatcher()

blacklist = ['79912083252']
admin_ids = ['5158396682', '6008247740', '5594962119']

# Инициализация бота и диспетчера
bot = Bot(API_TOKEN, default=DefaultBotProperties(
        parse_mode=ParseMode.HTML
        # тут ещё много других интересных настроек
    ))
storage = MemoryStorage()

# Определение состояний
class Form(StatesGroup):
    waiting_for_phone = State()
    waiting_for_ip = State()
    waiting_for_username = State()
    waiting_for_telegram = State()
    waiting_for_email = State()
    waiting_for_fio = State()

# Функция для создания инлайн-клавиатуры
def get_inline_keyboard(user_id):
    builder = InlineKeyboardBuilder()
    button = types.InlineKeyboardButton(text="📞 Пробив по номеру", callback_data='search_by_number')
    button2 = types.InlineKeyboardButton(text="🛜 Пробив по IP", callback_data='search_by_ip')
    button3 = types.InlineKeyboardButton(text="💫 Поиск по нику", callback_data='search_by_username')
    button4 = types.InlineKeyboardButton(text="📕 Пробив по ФИО", callback_data='search_by_fio')
    admin_button = types.InlineKeyboardButton(text="⚙️ Админ панель", callback_data='admin')
    
    builder.row(button, button2)
    builder.row(button3, button4)

    if user_id in admin_ids:
        builder.row(admin_button)

    return builder.as_markup()

def get_admin_keyboard():
    builder = InlineKeyboardBuilder()
    button = types.InlineKeyboardButton(text="➕ Добавить премиум", callback_data='add')
    builder.row(button)

    return builder.as_markup()

# Обработчик на Python:
@dp.pre_checkout_query()
async def on_pre_checkout_query(
    pre_checkout_query: PreCheckoutQuery
):
    await pre_checkout_query.answer(
        ok=True
    )

async def get_pay_keyboard(message):
    builder = InlineKeyboardBuilder()
    button = types.InlineKeyboardButton(text="Заплатить через Stars", callback_data='pay')
    builder.add(button)

    await message.answer("Кажется вы потратили все свои пробные использования!\n\n⚠️ <b>ОСНОВНОЙ СПОСОБ ОПЛАТЫ</b>\nДля покупки писать: @FinishType\n\n⚠️ <b>СПОСОБ ОПЛАТЫ ЧЕРЕЗ Stars НИЖЕ</b>\nНажмите на кнопку ниже для оплаты через Stars", reply_markup=builder.as_markup())    
    
@dp.callback_query(F.data == 'pay')
async def stars_pay(callback_query: types.CallbackQuery):
    await callback_query.answer()  # Уведомляем Telegram, что запрос обработан
    message = callback_query.message

    prices = [LabeledPrice(label="XTR", amount=99)]
    await message.answer_invoice(
        title="Оформление подписки на вечно",
        description="Ваш счет за подписку! ⚠️ ВЫ НЕ СМОЖЕТЕ ВЕРНУТЬ ЗВЕЗДЫ",
        prices=prices,
        # provider_token Должен быть пустым
        provider_token="",
        # В пейлоайд можно передать что угодно,
        # например, айди того, что именно покупается
        payload=f"forever_sub",
        # XTR - это код валюты Telegram Stars
        currency="XTR"
    )

@dp.message(F.successful_payment)
async def on_successful_payment(
    message: Message
):
    await message.answer(   
        "<b>Огромное спасибо!</b>\nПодписка уже на счету!",
        message_effect_id="5046509860389126442",
    )

    create_sub_forever(message.from_user.id)

# Обработчик команды /start
@dp.message(Command('start'))
async def send_welcome(message: types.Message, bot: Bot):
    for j, i in enumerate(subs):
        if int(i['id']) == int(message.from_user.id):
            await message.answer("Добро пожаловать в NumFinder, у вас оплачена подписка! Выберете один из пунктов:", reply_markup=get_inline_keyboard(str(message.from_user.id)))
            break
    else:
        if usage_counts.get(message.from_user.id, 0) <= 3: 
            await message.answer("""
            ⚠️ <b>ОСНОВНОЙ СПОСОБ ОПЛАТЫ</b>\nДля покупки писать: @FinishType\n\nДобро пожаловать в NumFinder! Вам дали 3 *пробных использования, после чего надо оформить подписку!\nВыберете один из пунктов:\n\n*Подписка оформляется на всегда, через оплату создателю или оплату за 99 Telegram Stars
            """, reply_markup=get_inline_keyboard(str(message.from_user.id)))
        else:
            await get_pay_keyboard(message)

@dp.callback_query(StateFilter(None), F.data.in_(['search_by_number', 'search_by_ip', 'search_by_fio', 'admin', 'add']))
async def button_handler(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.answer()  # Уведомляем Telegram, что запрос обработан

    if callback_query.data == 'search_by_number':
        await callback_query.message.answer("Введите номер телефона:")
        await state.set_state(Form.waiting_for_phone)

    elif callback_query.data == 'search_by_ip':
        await callback_query.message.answer("Введите номер IP в формате: X.X.X.X")
        await state.set_state(Form.waiting_for_ip)

    elif callback_query.data == 'search_by_fio':
        await callback_query.message.answer("Введите ФИО и Дату рождения в формате: ФАМИЛИЯ ИМЯ ОТЧЕСТВО DD.MM.YYYY")
        await state.set_state(Form.waiting_for_fio)
    
    elif callback_query.data == 'admin':
        await callback_query.message.answer("Добро пожаловать в Admin панель!", reply_markup=get_admin_keyboard())
    
    elif callback_query.data == 'add':
        await callback_query.message.answer("Введите @username")
        await state.set_state(Form.waiting_for_username)

# Обработчик ввода Username
@dp.message(Form.waiting_for_username)
async def process_fio(message: types.Message, state: FSMContext):
    username = message.text.lower()
    id_ = await get_telegram_by_username(username)
    create_sub_forever(str(id_['id']))
    await message.answer(f"<b>ПОДПИСКА УСПЕШНО ВЫДАНА ID </b> {id_} ⚠️")
    await state.clear()  # Завершаем состояние

# Обработчик ввода ФИО
@dp.message(Form.waiting_for_fio)
async def process_fio(message: types.Message, state: FSMContext):
    for j, i in enumerate(subs):
        if int(i['id']) == int(message.from_user.id):
            break
    else:
        if usage_counts.get(message.from_user.id, 0) > 3:
            await get_pay_keyboard(message)
            return

    if len(message.text.lower().split()) != 4:
        await message.answer("Неверный ввод данных!", reply_markup=get_inline_keyboard(str(message.from_user.id)))
        await state.clear()  # Завершаем состояние
        return

    add_usage(message.from_user.id)

    surname, name, patronymic, birth = message.text.lower().split()

    result = {
        "phone": '',
        "name": name,
        "surname": surname,
        "patronymic": '',
        "ip": '',
        "birth": birth
    }
    
    r = await message.answer(text="Идет поиск, ожидайте... 👌\n⬜⬜⬜⬜⬜⬜")

    seek = False            

    msg = "🔎 Поиск по базе...\n\n"

    base_big = full_search(result['phone'], result['surname'], result['name'], result['patronymic'], result['ip'])
        
    if base_big != {}:
        result = {**result, **base_big}
        msg += "❤️‍🔥 Общие базы (Есть неточности):\n"
        msg += f"├ IP: {result.get('ip', 'Не найдено')}\n"
        msg += f"├ Фамилия: {result.get('surname', 'Не найдено')}\n"
        msg += f"├ Имя: {result.get('name', 'Не найдено')}\n"
        msg += f"├ Отчество: {result.get('patronymic', 'Не найдено')}\n"
        msg += f"├ Дата рождения: {result.get('birth', 'Не найдено')}\n"
        msg += f"├ Адрес: {result.get('address', 'Не найдено')}\n"
        msg += f"├ Почтовый индекс: {result.get('mail_index', 'Не найдено')}\n"
        msg += f"├ Номер и серия паспорта: {result.get('passport', 'Не найдено')}\n"
        msg += f"└ Email: {result.get('email', 'Не найдено')}\n\n"
    
        find = True

    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩⬜⬜⬜⬜",
                 chat_id=r.chat.id, message_id=r.message_id)

    result1 = base1_by_fio(name=name, surname=surname, patronymic=patronymic, birth=birth)

    if result1 != {}:
        result = {**result, **result1}
        
        msg += "🎲 НАЛОГОВАЯ РФ (БОЛЕЕ СВЕЖАЯ):\n"
        msg += f"├ Фамилия: {result['surname']}\n"
        msg += f"├ Имя: {result['name']}\n"
        msg += f"├ Отчество: {result['patronymic']}\n"
        msg += f"├ Дата рождения: {result['birth']}\n"
        msg += f"├ Снилс: {result['snils']}\n"
        msg += f"├ ИНН: {result['inn']}\n"
        msg += f"└ Email: {result['email']}\n\n"

        seek = True

    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩🟩⬜⬜⬜",
                chat_id=r.chat.id, message_id=r.message_id)

    base_t2 = full_search(result['phone'], result['surname'], result['name'], result['patronymic'], result['ip'])

    if base_t2 != {}:
        result = {**base_t2, **result}
        msg += "📕 БАЗА TELE2 (Есть неточности):\n"
        msg += f"├ Фамилия: {result.get('surname', 'Не найдено')}\n"
        msg += f"├ Имя: {result.get('name', 'Не найдено')}\n"
        msg += f"└ Отчество: {result.get('patronymic', 'Не найдено')}\n\n"
    
        find = True

    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩🟩🟩⬜⬜",
                 chat_id=r.chat.id, message_id=r.message_id)

    if result['phone']:
        msg += "📞 Информация по телефону:\n"
        msg += f"├ Телефон: +{result['phone']}\n"

        if (result['phone'].startswith("+7") or result['phone'].startswith("8") or result['phone'].startswith("7")):
            function = russia_num
        else:
            function = phnum_parse

        for infomation in function(result['phone']):
            result = {**result, **infomation}
            msg += f"├ Провайдер: {infomation['prov']}\n"
            msg += f"├ Приблизительный регион: {infomation['region']}\n"
            msg += f"├ Тайм-зона: {infomation['time_zone']}\n"
            msg += f"└ Территория: {infomation['territory']}\n\n"

            seek = True

    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩🟩🟩🟩⬜",
                 chat_id=r.chat.id, message_id=r.message_id)
            
    social = await social_search(result['name'].lower().title(), result['surname'].lower().title(), result['phone'], result['birth'])

    if social != {}:
        result = {**result, **social}
        msg += "🆔 Социальные сети:\n"
        
        if result.get('telegram', None) and result.get('vk', None) != {}:
            msg += f"├ Телеграм: @{result['telegram']['username']}:\n"

        if result.get('vk', None):
            msg += f"└ ВКонтакте: vk.ru/id{result['vk']['id']}\n"

        seek = True

    await bot.edit_message_text(text="Поиск завершен! 💫\n🟩🟩🟩🟩🟩🟩",
                    chat_id=r.chat.id, message_id=r.message_id)

    if not seek:
        await message.answer("Нам жаль... Мы ничего не нашли.", reply_markup=get_inline_keyboard(str(message.from_user.id)))
    else:
        await message.answer(msg, reply_markup=get_inline_keyboard(str(message.from_user.id)), message_effect_id="5046509860389126442")
    
    await state.clear()  # Завершаем состояние

# Обработчик ввода IP
@dp.message(Form.waiting_for_ip)
async def process_ip(message: types.Message, state: FSMContext):
    for j, i in enumerate(subs):
        if int(i['id']) == int(message.from_user.id):
            break
    else:
        if usage_counts.get(message.from_user.id, 0) > 3:
            await get_pay_keyboard(message)
            return

    add_usage(message.from_user.id)

    ip = message.text
    await message.answer("Идет поиск, ожидайте... 👌")
    i = ip_detect(ip)
    if i:
        msg = "🔎 Поиск по базе...\n\n"

        msg += f"ℹ️ IP: {i['ip']}\n"
        msg += f"├ Провайдер: {i['prov']}\n"
        msg += f"├ Тайм-зона: {i['time_zone']}\n"
        msg += f"├ Страна: {i['country']}"
        msg += f"├ Регион: {i['region']}\n"
        msg += f"├ Приблизительный город: {i['city']}\n"
        msg += f"└ Координаты: {i['loc']}\n"
        await message.answer(msg, reply_markup=get_inline_keyboard(str(message.from_user.id)), message_effect_id="5046509860389126442")
    else:
        await message.answer("Нам жаль... Мы ничего не нашли.", reply_markup=get_inline_keyboard(str(message.from_user.id)))
    
    await state.clear()  # Завершаем состояние

# Обработчик ввода номера телефона
@dp.message(Form.waiting_for_phone)
async def process_phone_number(message: types.Message, state: FSMContext):
    for j, i in enumerate(subs):
        if int(i['id']) == int(message.from_user.id):
            break
    else:
        if usage_counts.get(str(message.from_user.id), 0) > 3:
            await get_pay_keyboard(message)
            return

    if message.text.replace("-", "").replace("(", "").replace(")", "").replace(" ", "").replace("+", "") in blacklist:
        await message.answer("[-] Нам жаль... Мы ничего не нашли.", reply_markup=get_inline_keyboard(str(message.from_user.id)))
        await state.clear()  # Завершаем состояние
        return

    add_usage(message.from_user.id)

    phone = message.text.replace("-", "").replace("(", "").replace(")", "").replace(" ", "")

    r = await message.answer("Идет поиск, ожидайте... 👌\n⬜⬜⬜⬜⬜⬜")

    if (phone.startswith("+7") or phone.startswith("8") or phone.startswith("7")):
        function = russia_num
        phone = phone.replace("+", "")
    else:
        function = phnum_parse

    find = False

    result = {
        "phone": phone,
        "name": '',
        "surname": '',
        "patronymic": '',
        "ip": '',
        "birth": None
    }

    for i in function(phone):
        if "phone" not in i:
            continue

        result = {**result, **i}

        msg = f"🔎 Поиск по базе...\n\n"

        msg += "📞 Информация по телефону:\n"
        msg += f"├ Телефон: {result['phone']}\n"
        msg += f"├ Провайдер: {result['prov']}\n"
        msg += f"├ Приблизительный регион: {result['region']}\n"
        msg += f"├ Тайм-зона: {result['time_zone']}\n"
        msg += f"└ Территория: {result['territory']}\n\n"

        find = True
    
    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩⬜⬜⬜⬜⬜",
                 chat_id=r.chat.id, message_id=r.message_id)

    base_big = full_search(result['phone'], result['surname'], result['name'], result['patronymic'], result['ip'], result['birth'])
        
    if base_big != {}:
        result = {**result, **base_big}
        msg += "❤️‍🔥 Общие базы (Есть неточности):\n"
        msg += f"├ IP: {result.get('ip', 'Не найдено')}\n"
        msg += f"├ Фамилия: {result.get('surname', 'Не найдено')}\n"
        msg += f"├ Имя: {result.get('name', 'Не найдено')}\n"
        msg += f"├ Отчество: {result.get('patronymic', 'Не найдено')}\n"
        msg += f"├ Дата рождения: {result.get('birth', 'Не найдено')}\n"
        msg += f"├ Адрес: {result.get('address', 'Не найдено')}\n"
        msg += f"├ Почтовый индекс: {result.get('mail_index', 'Не найдено')}\n"
        msg += f"├ Номер и серия паспорта: {result.get('passport', 'Не найдено')}\n"
        msg += f"└ Email: {result.get('email', 'Не найдено')}\n\n"
    
        find = True
    
    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩⬜⬜⬜⬜",
                 chat_id=r.chat.id, message_id=r.message_id)

    base1 = base1_by_phone(result['phone'])
        
    if base1 != {}:
        result = {**result, **base1}
        msg += "🎲 НАЛОГОВАЯ РФ (БОЛЕЕ СВЕЖАЯ):\n"
        msg += f"├ Имя: {result['name']}\n"
        msg += f"├ Фамилия: {result['surname']}\n"
        msg += f"├ Отчество: {result['patronymic']}\n"
        msg += f"├ Дата рождения: {result['birth']}\n"
        msg += f"├ Email: {result['email']}\n"
        msg += f"├ Снилс: {result['snils']}\n"
        msg += f"└ ИНН: {result['inn']}\n\n"
    
        find = True
    
    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩🟩⬜⬜⬜",
                chat_id=r.chat.id, message_id=r.message_id)
    
    base_t2 = base2(result['phone'], result['surname'], result['name'], result['patronymic'], result['ip'])
        
    if base_t2 != {}:
        result = {**result, **base_big}
        msg += "📕 БАЗА TELE2 (Есть неточности):\n"
        msg += f"├ Фамилия: {result.get('surname', 'Не найдено')}\n"
        msg += f"├ Имя: {result.get('name', 'Не найдено')}\n"
        msg += f"└ Отчество: {result.get('patronymic', 'Не найдено')}\n\n"
    
        find = True
    
    base_contact = get_contact(result['phone'])
        
    if base_contact.get('tags', []) != []:
        result = {**result, **base_contact}
        msg += "🤖 БАЗА GetContact:\n"
        for i, teg in enumerate(base_contact.get('tags', [])):
            if i == len(base_contact.get('tags', []))-1:
                break

            msg += f"├ Тег {i+1}: {teg}\n"

        msg += f"└ Тег {i+1}: {base_contact.get('tags', [])[-1]}\n\n"
    
        find = True
    
    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩🟩🟩⬜⬜",
                 chat_id=r.chat.id, message_id=r.message_id)
    
    if result['ip']:
        i = ip_detect(result['ip'])
        if i:
            result = {**result, **i}
            msg += "🔎 IP ИНФОРМАЦИЯ:\n"
            msg += f"├ IP: {result['ip']}\n"
            msg += f"├ Провайдер: {result['prov']}\n"
            msg += f"├ Тайм-зона: {result['time_zone']}\n"
            msg += f"├ Страна: {result['country']}\n"
            msg += f"├ Регион: {result['region']}\n"
            msg += f"├ Приблизительный город: {result['city']}\n"
            msg += f"└ Координаты: {result['loc']}\n\n"
    
    await bot.edit_message_text(text="Идет поиск, ожидайте... 👌\n🟩🟩🟩🟩🟩⬜",
                 chat_id=r.chat.id, message_id=r.message_id)
 
    social = await social_search(result['name'].lower().title(), result['surname'].lower().title(), result['phone'], result['birth'])

    if social != {}:
        result = {**result, **social}
        msg += "🆔 Социальные сети:\n"
        
        if result.get('telegram', None) and result.get('vk', None) != {}:
            msg += f"├ Телеграм: @{result['telegram']['username']}:\n"

        if result.get('vk', None):
            msg += f"└ ВКонтакте: vk.ru/id{result['vk']['id']}\n"

        find = True

    await bot.edit_message_text(text="Поиск завершен! 💫\n🟩🟩🟩🟩🟩🟩",
                    chat_id=r.chat.id, message_id=r.message_id)

    if not find:
        await message.answer("[-] Нам жаль... Мы ничего не нашли.", reply_markup=get_inline_keyboard(str(message.from_user.id)))
    else:
        await message.answer(msg, reply_markup=get_inline_keyboard(str(message.from_user.id)), message_effect_id="5046509860389126442")
    
    await state.clear()  # Завершаем состояние

# Запуск процесса поллинга новых апдейтов
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())