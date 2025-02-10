import json
from datetime import datetime
import threading

# Глобальные переменные для хранения подписок и использований
subs = []
usage_counts = {}

def create_sub_forever(user_id: str):
    sub = {
        "id": user_id,
        "until": True
    }
    
    if sub not in subs:
        subs.append(sub)
        save_json('sub.json', subs)
        print(f'>> {user_id} subscription is valid forever!!')
        return True
    else:
        print(f'>> {user_id} already has a subscription!')
        return False
    
def delete_sub(user_id: int):
    for j, i in enumerate(subs):
        if i['id'] == user_id:
            subs.pop(j)
            save_json('sub.json', subs)
            del usage_counts[user_id]  # Удаляем счетчик использований
            save_json('usage_counts.json', usage_counts)
            return True
    else:
        return False

def add_usage(user_id: str):
    if str(user_id) in list(usage_counts.keys()):
        usage_counts[str(user_id)] += 1
        save_json('usage_counts.json', usage_counts)
    else:
        usage_counts[str(user_id)] = 0
        add_usage(user_id)

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def load_json():
    global subs, usage_counts
    try:
        subs = json.load(open('sub.json', 'r'))
    except FileNotFoundError:
        subs = []
    
    try:
        usage_counts = json.load(open('usage_counts.json', 'r'))
    except FileNotFoundError:
        usage_counts = {}

def new_user(user_id: int):
    if usage_counts.get(user_id, False):
        usage_counts[user_id] = 0  # Инициализируем счетчик использований
        save_json('usage_counts.json', usage_counts)
        print(f'>> New user: {user_id}!')

load_json()