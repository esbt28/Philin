import json
import datetime as dt
from pathlib import Path
import time

DB_NAME = 'bb'
db_path = Path(f'{DB_NAME}.txt')
if not db_path.exists():
    
    with open(DB_NAME + '.txt', 'w') as f:
        f.write('')
        print('bb file was created')
    
def add(user: str, arg: str):
    now = dt.datetime.now()
    time = now.strftime("%H:%M")
    day = now.strftime("%d")
    month = now.strftime("%m")
    print(f'{time} {day}.{month}: {user} - {arg}')
    with open(DB_NAME + '.txt', 'r') as f:
        data = f.read()
    with open(DB_NAME + '.txt', 'w') as f:
        f.write(data + f'{time} {day}.{month}: {user} - {arg}\n')
