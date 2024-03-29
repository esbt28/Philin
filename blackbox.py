import easydata2 as ed
import datetime as dt
from pathlib import Path
import time

DB_NAME = 'bb'
db_path = Path(f'{DB_NAME}.json')
if not db_path.exists():
    ed.create_database(DB_NAME)
    print('Файл ящика не обнаружен!')
    
def add(user: str, arg: str):
    now = dt.datetime.now()
    time = now.strftime("%H:%M")
    day = now.strftime("%d")
    month = now.strftime("%m")
    if ed.is_id_exist(DB_NAME, user):
        print(f'{time} {day}.{month}: {user} выполнил {arg}')
        ed.give_item_data(DB_NAME, user, arg, f'{time} {day}.{month}')

    else:
        print(f'{time} {day}.{month}: {user} впервые выполнил {arg}')
        ed.give_id_data(DB_NAME, user, {})
        ed.give_item_data(DB_NAME, user, arg, f'{time} {day}.{month}')