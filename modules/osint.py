import asyncio
from pyrogram import Client
from pyrogram.errors import PhoneNumberInvalid, UserNotParticipant, UsernameNotOccupied
import vk_api
from datetime import datetime

# Замените эти значения на свои
api_id = '29265675'
api_hash = '6996ad4a4cb218536f86e3bb918a537e'
TOKEN = 'vk1.a.O8lqeKUkKsSBD4UujUi_hHms3UBkedp8VZIkJ-NvmdzdpcLokREnBCQqe0UEX571MVnkdf732qZ0fMGNwVG9Dc68xdC_jDUO6OAiHiNFytTGAf739kTGuuLMpinGOgaBEldaEv3EHLlpIKRmxFJhcf0FeO9X5g8uD67WtD86-1PdXMHy9KtKdAOH4kzmzx0aZ-D6MHY1RkfaYuhRpr9VLQ'

# Функции для Telegram
async def get_telegram_by_phone(phone):
    data = {}
    async with Client("telegram", api_id, api_hash) as app:
        try:
            user = await app.get_users(phone)
            data['username'] = user.username if user.username else "Нету"
        except (PhoneNumberInvalid, UserNotParticipant):
            pass
        except Exception:
            pass
    return data

async def get_telegram_by_username(user):
    data = {}
    async with Client("telegram", api_id, api_hash) as app:
        try:
            user = await app.get_users(user)
            data['id'] = user.id
        except (PhoneNumberInvalid, UserNotParticipant):
            pass
        except Exception:
            pass
    return data

# Функции для VK
def vk_by_name(first_name, last_name, birth):
    vk_session = vk_api.VkApi(token=TOKEN)
    vk = vk_session.get_api()
    try:
        users = vk.users.search(q=f"{first_name} {last_name}", fields='id, first_name, last_name, photo_200, city, bdate, phone')
        for user in users['items']:
            bdate = user.get('bdate', None)
            formatted_bdate = format_bdate(bdate)
            if formatted_bdate == birth or formatted_bdate[:5] == birth[:5]:
                return user
    except vk_api.exceptions.ApiError as e:
        print(f"Ошибка API: {e}")
        return None

def format_bdate(bdate):
    if bdate:
        if len(bdate) in [3, 4 ,5]:
            date_obj = datetime.strptime(bdate, '%d.%m').strftime('%d.%m')
            return date_obj
        elif len(bdate) in [8, 9, 10]:
            date_obj = datetime.strptime(bdate, '%d.%m.%Y').strftime('%d.%m.%Y')
            return date_obj
        else:
            print(bdate)
    else:
        return '**.**.**'

# Функция для объединенного поиска
async def social_search(first_name, last_name, phone, birth):
    results = {}

    if first_name and last_name and birth:
        # Поиск пользователя в VK
        vk = vk_by_name(first_name, last_name, birth)
        if vk:
            results['vk'] = vk
    
    if phone:
        # Поиск пользователя в Telegram
        tg = await get_telegram_by_phone(phone)
        if tg:
            results['telegram'] = tg
    
    return results