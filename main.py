import discord
from discord.ext import commands
import random
import easydata2 as ed
from pathlib import Path
from localcd import cooldown_check, cooldown_set
import blackbox as bb

DB_NAME = 'philin_data'
db_path = Path(f'{DB_NAME}.json')
if not db_path.exists():
    bb.add('system', 'data base file was created')
    
    ed.create_database(DB_NAME)

CONFIG_NAME = 'config'
db_path = Path(f'{CONFIG_NAME}.json')
if not db_path.exists():
    ed.create_database(CONFIG_NAME)
    
    bb.add('system', 'config file was created')
    
    ed.give_id_data(CONFIG_NAME, 'config', {'prefix': '>', 'balance': 0, 'inc_balance': 500, 'currency': '$', 'bank_balance': 0, 'bank_limit': 200, 'inc_ad': 1, 'inc_building': 1, 'skill_hack': 1, 'skill_protect': 1, 'business_price': 1000, 'ad_price': 350, 'building_price': 1000, 'inc_stocks': 0, 'inc_workers': 0, 'inc_max_stocks': 20, 'inc_stock_percent': 2, 'inc_max_workers': 100, 'max_bonus': 400, 'bot_id': '998256502940905542', 'world_money': 10000000000000})

config = ed.get_id_data(CONFIG_NAME, 'config')

client_id = config['bot_id']

if ed.is_item_exist(DB_NAME, client_id, 'bank_balance') == False:
    ed.give_item_data(DB_NAME, client_id, 'bank_balance', config['world_money'])

messages = 0

client = commands.Bot(command_prefix=config['prefix'])

@client.event
async def on_ready():
    bb.add('system', '{0.user} is online'.format(client))
    await client.change_presence(status = discord.Status.idle, activity= discord.Activity(name=f'>help', type= discord.ActivityType.playing))

@client.command()
async def bal(message):
    user_id = str(message.author.id)
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_balance'):
        bank_balance = ed.give_item_data(DB_NAME, user_id, 'bank_balance', config['bank_balance'])
    bank_balance = ed.get_item_data(DB_NAME, user_id, 'bank_balance')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_limit'):
        bank_limit = ed.give_item_data(DB_NAME, user_id, 'bank_limit', config['bank_limit'])
    bank_limit = ed.get_item_data(DB_NAME, user_id, 'bank_limit')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'work'):
        work = ed.give_item_data(DB_NAME, user_id, 'work', 'Отсутствует')
    work = ed.get_item_data(DB_NAME, user_id, 'work')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')
    
    if business != 'Отсутствует':
        work = '**Бизнес**'
    
    embed1 = discord.Embed(
    title = 'Ваш баланс',
    description = f'💸 Наличка: {currency}**{balance}**\n💳 Банк: {currency}**{bank_balance}**\n💰 Лимит: {currency}**{bank_limit}**\n🔧 Работа: {work}',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def bonus(message):
    
    user_id = str(message.author.id)

    if cooldown_check(user_id, 'bonus', 43200) != True:
        wait = cooldown_check(user_id, 'bonus', 43200)
        embed2 = discord.Embed(
        title = '<a:no:998468646533869658> Пожалуйста, подождите',
        description = f'Осталось ждать: {wait} секунд',
        color = 0xffff00)
        await message.channel.send(embed = embed2)
        
        return

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    payment = random.randint(1, config['max_bonus'])
    
    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
    sub_client = client_bank_balance - int(payment)
    
    if sub_client < 0:
        payment = client_bank_balance
        sub_client = 0
    
    
    sum = int(balance) + payment
    
    ed.give_item_data(DB_NAME, user_id, 'balance', sum)
    
    ed.give_item_data(DB_NAME, client_id, 'bank_balance', sub_client)
    
    cooldown_set(user_id, 'bonus')

    embed1 = discord.Embed(
    title = 'Ежедневная выплата',
    description = f'📬 Оплата: {currency}**{payment}**\n💸 Итоговый баланс: {currency}**{sum}**',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def pay(message, *, content):
    user_id = str(message.author.id)

    content_split = content.split()
    another_id = content_split[0].replace('<', '').replace('@', '').replace('>', '')
    count = int(content_split[1])

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, another_id, 'balance'):
        another_balance = ed.give_item_data(DB_NAME, another_id, 'balance', config['balance'])
    another_balance = ed.get_item_data(DB_NAME, another_id, 'balance')

    count = str(int(count) / 100 * 95).split('.')[0]
    
    comission = str(int(count) / 100 * 5).split('.')[0]
    
    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
    sum_client = client_bank_balance + int(comission)

    sub = int(balance) - int(count)
    sum = int(str(int(another_balance) + int(count)).split('.')[0])

    if sub and sum and int(balance) >= int(count) and int(count) >= 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        ed.give_item_data(DB_NAME, another_id, 'balance', sum)
        
        ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)
        text = f'<a:yes:998468643627212860> **Успешная транзакция!**\n📤 Отправитель: <@{user_id}>\n📥 Получатель: <@{another_id}>\n💸 Сумма: {currency}**{count}**\n📄 Комиссия: **5**%'
    elif int(balance) < int(count):
        text = f'<a:no:998468646533869658> Нехватка средств!\nУ вас на балансе: {currency}*{balance}*'
    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\n**Возможные причины:**\n- Отсутствуют данные\n- Данное число не доступно'

    embed1 = discord.Embed(
    title = 'Перевод средств',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def deposit(message, *, content):
    user_id = str(message.author.id)
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_balance'):
        bank_balance = ed.give_item_data(DB_NAME, user_id, 'bank_balance', config['bank_balance'])
    bank_balance = ed.get_item_data(DB_NAME, user_id, 'bank_balance')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_limit'):
        bank_limit = ed.give_item_data(DB_NAME, user_id, 'bank_limit', config['bank_limit'])
    bank_limit = ed.get_item_data(DB_NAME, user_id, 'bank_limit')

    if content == 'all':
        content = balance
        
    payment = str(int(content) / 100 * 90).split('.')[0]
    
    comission = str(int(content) / 100 * 10).split('.')[0]
    
    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
    sum_client = client_bank_balance + int(comission)

    sub = int(balance) - int(content)
    sum = int(str(int(bank_balance) + int(payment)).split('.')[0])


    if int(balance) >= int(content) and int(bank_balance) + int(content) <= int(bank_limit) and int(content) > 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        ed.give_item_data(DB_NAME, user_id, 'bank_balance', sum)
        
        ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)
        text = f'<a:yes:998468643627212860> **Успешное пополнение!**\n📤 Отправитель: <@{user_id}>\n📥 Получатель: **Philin Bank**\n💸 Сумма: {currency}**{payment}**\n📄 Комиссия: **10**%'
    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\n**Возможные причины:**\n- Не хватка средств (Доступно: {currency}**{balance}**)\n- Данная сумма превысит лимит ({currency}**{bank_limit}**)\n- Данное число не доступно'

    embed1 = discord.Embed(
    title = 'Перевод средств',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def withdraw(message, *, content):
    user_id = str(message.author.id)
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_balance'):
        bank_balance = ed.give_item_data(DB_NAME, user_id, 'bank_balance', config['bank_balance'])
    bank_balance = ed.get_item_data(DB_NAME, user_id, 'bank_balance')  
    
    if not ed.is_item_exist(DB_NAME, user_id, 'bank_limit'):
        bank_limit = ed.give_item_data(DB_NAME, user_id, 'bank_limit', config['bank_limit'])
    bank_limit = ed.get_item_data(DB_NAME, user_id, 'bank_limit')

    if content == 'all':
        content = balance

    sub = int(bank_balance) - int(content)
    sum = int(balance) + int(content)
    sum = int(str(sum).split('.')[0])


    if int(bank_balance) >= int(content) and int(content) >= 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sum)
        ed.give_item_data(DB_NAME, user_id, 'bank_balance', sub)
        text = f'<a:yes:998468643627212860> **Успешное снятие!**\n📤 Отправитель: **Philin Bank**\n📥 Получатель: <@{user_id}>\n💸 Сумма: {currency}**{content}**\n📄 Комиссия: **0**%'
    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\n**Возможные причины:**\n- Не хватка средств (Доступно: {currency}**{bank_balance}**)\n- Данное число не доступно'

    embed1 = discord.Embed(
    title = 'Перевод средств',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def hack(message, *, content):
    user_id = str(message.author.id)

    content_split = content.split()
    another_id = content_split[0].replace('<', '').replace('@', '').replace('>', '')


    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, another_id, 'balance'):
        another_balance = ed.give_item_data(DB_NAME, another_id, 'balance', config['balance'])
    another_balance = ed.get_item_data(DB_NAME, another_id, 'balance')

    if not ed.is_item_exist(DB_NAME, another_id, 'skill_protect'):
        skill_protect = ed.give_item_data(DB_NAME, another_id, 'skill_protect', config['skill_protect'])
    skill_protect = ed.get_item_data(DB_NAME, another_id, 'skill_protect')

    if not ed.is_item_exist(DB_NAME, user_id, 'skill_hack'):
        skill_hack = ed.give_item_data(DB_NAME, user_id, 'skill_hack', config['skill_hack'])
    skill_hack = ed.get_item_data(DB_NAME, user_id, 'skill_hack')

    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))

    chance = random.randint(1, 100)

    if int(skill_protect) >= int(skill_hack):
        procent = 100 / (int(skill_protect) / int(skill_hack) + 1)
        procent = int(str(procent).split('.')[0])
    elif int(skill_protect) < int(skill_hack):
        procent = 100 - (100 / (int(skill_hack) / int(skill_protect) + 1))
        procent = int(str(procent).split('.')[0])
    
    
    if chance <= procent:
        count = int(another_balance) // 2
        
        sum = int(balance) + count
        sub = int(another_balance) - count
        
        ed.give_item_data(DB_NAME, another_id, 'balance', sub)
        ed.give_item_data(DB_NAME, user_id, 'balance', sum)
        text = f'<a:yes:998468643627212860> **Успешное ограбление!**\n📤 Жертва: <@{another_id}>\n📥 Грабитель: <@{user_id}>\n💸  Сумма: {currency}**{count}**\n📄 Шанс: **{procent}**%'
    else:
        count = int(balance) // 2
        sub = int(balance) - count
        sum_client = client_bank_balance + int(count)
        ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        text = f'<a:no:998468646533869658> Ограбление не удалось!\n⚖️ Штраф: {currency}**{count}**\n📄 Шанс: **{procent}**%'

    embed1 = discord.Embed(
    title = 'Ограбление',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def set_work(message, *, content):
    user_id = str(message.author.id)
    
    if not ed.is_item_exist(DB_NAME, user_id, 'work'):
        work = ed.give_item_data(DB_NAME, user_id, 'work', 'Отсутствует')
    work = ed.get_item_data(DB_NAME, user_id, 'work')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')
    
    if ed.is_item_exist(DB_NAME, content, 'grafic') and content != 'quit' and business == 'Отсутствует':
        inc_workers = ed.get_item_data(DB_NAME, content, 'workers')
        
        inc_max_workers = ed.get_item_data(DB_NAME, content, 'max_workers')
        
        if int(inc_max_workers) - int(inc_workers) > 0:
            
            ed.give_item_data(DB_NAME, user_id, 'work', content)
            
            workers = ed.get_item_data(DB_NAME, content, 'workers')
            
            ed.give_item_data(DB_NAME, content, 'workers', workers + 1)
            
            text = f'<a:yes:998468643627212860> **Успешное трудоустройство** на работу в {content}'
        
        else:
            
            text = '<:error:1001754203565326346> Свободные места отсутствуют'
        
    elif content == 'quit' and work != 'Отсутствует':
        workers = ed.get_item_data(DB_NAME, work, 'workers')
        
        ed.give_item_data(DB_NAME, user_id, 'work', 'Отсутствует')
            
        ed.give_item_data(DB_NAME, work, 'workers', workers - 1)
        
        text = f'<a:yes:998468643627212860> **Успешное увольнение** из {work}'
        
    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Данного бизнеса/параметра не существует\n- У вас есть свой бизнес\n- Вы и так нигде не работаете'

    embed1 = discord.Embed(
    title = 'Работа',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def skill_up(message, *, content):

    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if not ed.is_item_exist(DB_NAME, user_id, 'skill_hack'):
        skill_hack = ed.give_item_data(DB_NAME, user_id, 'skill_hack', config['skill_hack'])
    skill_hack = ed.get_item_data(DB_NAME, user_id, 'skill_hack')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'skill_protect'):
        skill_protect = ed.give_item_data(DB_NAME, user_id, 'skill_protect', config['skill_protect'])
    skill_protect = ed.get_item_data(DB_NAME, user_id, 'skill_protect')
    text = '<:error:1001754203565326346> Проверьте написание команды!'

    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))

    if content == 'hack':
        hack_price = int(skill_hack) * 50
        if int(balance) >= hack_price:

            skill_hack = int(skill_hack) + 1
            sub = int(balance) - hack_price
            sum_client = client_bank_balance + int(hack_price)
            
            ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)

            ed.give_item_data(DB_NAME, user_id, 'balance', sub)
            
            ed.give_item_data(DB_NAME, user_id, 'balance', skill_hack)
                
            text = f'🗡Вы успешно повысили навык взлома за {currency}**{hack_price}**\nВаш новый уровень: **{skill_hack}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸Нужная сумма: {currency}**{hack_price}**'

    if content == 'protect':
        protect_price = int(skill_protect) * 100
        if int(balance) >= protect_price:

            skill_protect = int(skill_protect) + 1
            sub = int(balance) - protect_price
            sum_client = client_bank_balance + int(protect_price)
            
            ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)

            ed.give_item_data(DB_NAME, user_id, 'balance', sub)
            
            ed.give_item_data(DB_NAME, user_id, 'balance', skill_hack)
            
            text = f'🔒Вы успешно повысили защиту от взлома за {currency}**{protect_price}**\nВаш новый уровень: **{skill_protect}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸Нужная сумма: {currency}**{protect_price}**'

    embed1 = discord.Embed(
    title = 'Улучшение',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_create(message, *, content):

    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
    
    business_price = int(config['business_price'])

    if int(balance) >= business_price and not ed.is_id_exist(DB_NAME, content) and content != None and business == 'Отсутствует':
        sub = int(balance) - business_price
        
        sum_client = client_bank_balance + business_price

        if content != 'Отсутствует':
            inc_name = ed.give_item_data(DB_NAME, user_id, 'business', content)
            
        inc_ad = ed.give_item_data(DB_NAME, content, 'ad', config['inc_ad'])
        inc_building = ed.give_item_data(DB_NAME, content, 'building', config['inc_building'])
        inc_grafic = ed.give_item_data(DB_NAME, content, 'grafic', '🔺')
        inc_balance = ed.give_item_data(DB_NAME, content, 'balance', config['inc_balance'])
        inc_workers = ed.give_item_data(DB_NAME, content, 'workers', config['inc_workers'])
        inc_stocks = ed.give_item_data(DB_NAME, content, 'stocks', config['inc_stocks'])
        inc_max_stocks = ed.give_item_data(DB_NAME, content, 'max_stocks', config['inc_max_stocks'])
        inc_stock_percent = ed.give_item_data(DB_NAME, content, 'stock_percent', config['inc_stock_percent'])
        inc_max_workers = ed.give_item_data(DB_NAME, content, 'max_workers', config['inc_max_workers'])

        stock_price = ed.give_item_data(DB_NAME, content, 'stock_price', int(str(int(inc_balance) / 100 * 2).split('.')[0]))

        ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        text = f'<a:yes:998468643627212860> **Успешно создан бизнес**: **{content} Inc.**\n💸 С вашего баланса списано {currency}**{business_price}**'

    else:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Нехватка средств ({currency}**{business_price}**)\n- Отсутствует название\n- У вас уже есть бизнес\n- Бизнес с таким названием уже существует\n- Данное наименование запрещено'
        
    embed1 = discord.Embed(
    title = 'Предприятие',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_up(message, *, content):

    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
    
    text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Непредусмотренный параметр\n- Отсутствие бизнеса'

    if content == 'ad' and business != 'Отсутствует':
        ad_price = int(ed.get_item_data(DB_NAME, business, 'ad')) * int(ed.get_item_data(CONFIG_NAME, 'config', 'ad_price'))
        if int(balance) >= ad_price:
            
            sub = int(balance) - ad_price
            sum_client = client_bank_balance + ad_price
            
            ed.give_item_data(DB_NAME, user_id, 'balance', sub)
            ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)
            ed.give_item_data(DB_NAME, business, 'ad', int(ed.get_item_data(DB_NAME, business, 'ad')) + 1)
                
            text = f'📈 Вы успешно повысили уровень распространенности своей компании за {currency}**{ad_price}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸Нужная сумма: {currency}**{ad_price}**'

    if content == 'building' and business != 'Отсутствует':
        building_price = int(ed.get_item_data(DB_NAME, business, 'building'))** 2 * int(ed.get_item_data(CONFIG_NAME, 'config', 'building_price'))
        if int(balance) >= building_price:

            sub = int(balance) - building_price
            sum_client = client_bank_balance + building_price
            
            ed.give_item_data(DB_NAME, user_id, 'balance', sub)
            ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)
            ed.give_item_data(DB_NAME, business, 'building', int(ed.get_item_data(DB_NAME, business, 'building')) + 1)
                
            text = f'📈 Вы успешно повысили уровень распространенности своей компании за {currency}**{building_price}**'
    
        else:
            text = f'<a:no:998468646533869658> Нехватка средств!\n💸 Нужная сумма: {currency}**{building_price}**'

    embed1 = discord.Embed(
    title = 'Улучшение',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_info(message): 
    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    text = '<a:no:998468646533869658> У вас отсутствует бизнес!'

    if business != 'Отсутствует':
        inc_ad = ed.get_item_data(DB_NAME, business, 'ad')
        inc_building = ed.get_item_data(DB_NAME, business, 'building')
        inc_grafic = ed.get_item_data(DB_NAME, business, 'grafic')
        inc_balance = ed.get_item_data(DB_NAME, business, 'balance')
        inc_workers = ed.get_item_data(DB_NAME, business, 'workers')
        inc_stocks = ed.get_item_data(DB_NAME, business, 'stocks')
        inc_max_stocks = ed.get_item_data(DB_NAME, business, 'max_stocks')
        inc_stock_percent = ed.get_item_data(DB_NAME, business, 'stock_percent')
        inc_max_workers = ed.get_item_data(DB_NAME, business, 'max_workers')

        stock_price = int(str(int(inc_balance) / 100 * int(inc_stock_percent)).split('.')[0])

        text = f'📌Название: **{business}**\n📨Уровень рекламы: **{inc_ad}**\n🏢Количество зданий: **{inc_building}**\n💸Бюджет: {currency}**{inc_balance}**\n📊Цена акции: {currency}**{stock_price}**{inc_grafic}\n🧷Процент акции: **{inc_stock_percent}%**\n📈Продано акций: **{inc_stocks}/{inc_max_stocks}**\n👤Сотрудников: {inc_workers}/{inc_max_workers}'
    
    embed1 = discord.Embed(
    title = 'Предприятие',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def badge(message):
    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'badges'):
        badges = ed.give_item_data(DB_NAME, user_id, 'badges', 'Отсутствуют')
    badges = ed.get_item_data(DB_NAME, user_id, 'badges')
    
    embed1 = discord.Embed(
    title = 'Инвентарь',
    description = f'🗃 Ваши значки: {badges}',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def set_currency(message, *, content):
    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'badges'):
        badges = ed.give_item_data(DB_NAME, user_id, 'badges', 'Отсутствуют')
    badges = ed.get_item_data(DB_NAME, user_id, 'badges')

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if badges != 'Отсутствуют':
        badges_split = badges.split()
        badges_count = len(badges_split)

    num = int(content) - 1

    if badges != '**Отсутствуют**' and num <= badges_count:
        ed.give_item_data(DB_NAME, user_id, 'currency', badges_split[num])
        
        text = f'<a:yes:998468643627212860> **Успешно изменена иконка!**\nНовая иконка: {badges_split[num]}'
    else:
        text = f'<a:no:998468646533869658> У вас нет значка с таким номером'

    embed1 = discord.Embed(
    title = 'Кастомизация',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def id(message, *, content):
    embed1 = discord.Embed(
    title = 'Поиск айди',
    description = f'Эмодзи: {content}\nАйди: ```{content}```',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_withdraw(message, *, content):
    user_id = str(message.author.id)

    count = int(content)

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')

    if not ed.is_item_exist(DB_NAME, user_id, 'business'):
        business = ed.give_item_data(DB_NAME, user_id, 'business', 'Отсутствует')
    business = ed.get_item_data(DB_NAME, user_id, 'business')

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')

    if not ed.is_item_exist(DB_NAME, business, 'inc_balance'):
        inc_balance = ed.give_item_data(DB_NAME, business, 'business', config['inc_balance'])
    inc_balance = ed.get_item_data(DB_NAME, business, 'business')

    sum = int(balance) + count
    sub = int(inc_balance) - count

    text = '<a:no:998468646533869658> У вас отсутствует бизнес!'
    if business != 'Отсутствует' and count > 0:
        ed.give_item_data(DB_NAME, user_id, 'balance', sum)
        ed.give_item_data(DB_NAME, business, 'balance', sub)
        ed.give_item_data(DB_NAME, business, 'grafic','🔻')
        text = f'<a:yes:998468643627212860> **Успешная транзакция!**\n📤Отправитель: {business}\n📥Получатель: <@{user_id}>\n💸Сумма: {currency}**{count}**\n📄Комиссия: **0**%'
    elif int(content) > 0:
        text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- У вас нет бизнеса\n- Снятие данной суммы невозможно'
    
    embed1 = discord.Embed(
    title = 'Предприятие',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_set(message, *, content):
    user_id = str(message.author.id)

    content_split = content.split()
    
    business = ed.get_item_data(DB_NAME, user_id, 'business')
    
    text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Непредусмотренный параметр\n- Отсутствие бизнеса\n- Превышение аргумента'
    
    if content_split[0] == 'max_workers' and content_split[1].isdigit() and business != 'Отсутствует':
        if int(content_split[1]) >= 0:
            ed.give_item_data(DB_NAME, business, 'max_workers', int(content_split[1]))
            text = f'⚙️ Вы изменили число допустимых сотрудников на {content_split[1]}'
        
    elif content_split[0] == 'stock_percent' and content_split[1].isdigit() and business != 'Отсутствует':
        if int(content_split[1]) * int(ed.get_item_data(DB_NAME, business, 'max_stocks')) <= 100 and int(content_split[1]) > 0:
            ed.give_item_data(DB_NAME, business, 'stock_percent', int(content_split[1]))
            text = f'⚙️ Вы изменили долю одной акции на {content_split[1]}%'
            
    elif content_split[0] == 'max_stocks' and content_split[1].isdigit() and business != 'Отсутствует' and int(content_split[1]) >= 0:
        if int(content_split[1]) * int(ed.get_item_data(DB_NAME, business, 'stock_percent')) <= 100:
            ed.give_item_data(DB_NAME, business, 'max_stocks', int(content_split[1]))
            text = f'⚙️ Вы изменили число доступных акций на {content_split[1]}'
            
    embed1 = discord.Embed(
    title = 'Настройка',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)
    
@client.command()
async def inc_store(message, *, content = 'None'):
    user_id = str(message.author.id)

    content_split = content.split()
    text = ''

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'inventory'):
        inventory = ed.give_item_data(DB_NAME, user_id, 'inventory', {})
    inventory = ed.get_item_data(DB_NAME, user_id, 'inventory')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Данного параметра не существует\n- Данного бизнеса не существует\n- Данное число не доступно\n- Нехватка средств'
    
    if content_split[0] == 'None':
        
        text = ''
    
        ids = ed.ids(DB_NAME)
        
        for id in ids:
            if ed.is_item_exist(DB_NAME, id, 'grafic'):
                inc_balance = ed.get_item_data(DB_NAME, id, 'balance')
                inc_grafic = ed.get_item_data(DB_NAME, id, 'grafic')
                stock_price = ed.give_item_data(DB_NAME, id, 'stock_price', int(str(int(inc_balance) / 100 * 2).split('.')[0]))

                text = text + f'{id}: {currency}**{stock_price}** {inc_grafic}\n'
                
    elif content_split[0] == 'buy':

        if ed.is_item_exist(DB_NAME, content_split[1], 'grafic'):

            price = int(ed.get_item_data(DB_NAME, content_split[1], 'stock_price')) * int(content_split[2].split('.')[0])
            
            if int(content_split[2]) <= int(ed.get_item_data(DB_NAME, content_split[1], 'max_stocks')) - int(ed.get_item_data(DB_NAME, content_split[1], 'stocks')) and int(content_split[2]) > 0 and balance >= price:
                
                if cooldown_check(user_id, f'inc_store buy {content_split[1]}', 172800) != True:
                    wait = cooldown_check(user_id, f'inc_store buy {content_split[1]}', 172800)
                    embed2 = discord.Embed(
                    title = '<a:no:998468646533869658> Пожалуйста, подождите',
                    description = f'Осталось ждать: {wait} секунд',
                    color = 0xffff00)
                    await message.channel.send(embed = embed2)
        
                    return
                price = int(ed.get_item_data(DB_NAME, content_split[1], 'stock_price')) * int(content_split[2].split('.')[0])
            
                inc_balance = ed.get_item_data(DB_NAME, content_split[1], 'balance')
                inc_stocks =  ed.get_item_data(DB_NAME, content_split[1], 'stocks')
                
                sum = int(inc_balance) + price
                sub = int(balance) - price
                
                ed.give_item_data(DB_NAME, content_split[1], 'balance', sum)
                ed.give_item_data(DB_NAME, user_id, 'balance', sub)
                
                inventory[content_split[1]] = inventory.get(content_split[1], 0) + int(content_split[2])
                
                ed.give_item_data(DB_NAME, user_id, 'inventory', inventory)
                
                sum = int(content_split[2]) + int(ed.get_item_data(DB_NAME, content_split[1], 'stocks'))
                
                ed.give_item_data(DB_NAME, content_split[1], 'stocks', sum)
                ed.give_item_data(DB_NAME, content_split[1], 'grafic', '🔺')
                
                cooldown_set(user_id, f'inc_store sell {content_split[1]}')
                
                text = f'<a:yes:998468643627212860> **Успешная покупка** {content_split[2]} акций компании {content_split[1]} за {currency}**{price}**'
                
    elif content_split[0] == 'sell':
        
        if ed.is_item_exist(DB_NAME, content_split[1], 'grafic'):

            if int(content_split[2]) <= int(ed.get_item_data(DB_NAME, user_id, 'inventory')[content_split[1]]) and int(content_split[2]) > 0:
                
                if cooldown_check(user_id, f'inc_store sell {content_split[1]}', 172800) != True:
                    wait = cooldown_check(user_id, f'inc_store sell {content_split[1]}', 172800)
                    embed2 = discord.Embed(
                    title = '<a:no:998468646533869658> Пожалуйста, подождите',
                    description = f'Осталось ждать: {wait} секунд',
                    color = 0xffff00)
                    await message.channel.send(embed = embed2)
        
                    return
                
                price = int(ed.get_item_data(DB_NAME, content_split[1], 'stock_price')) * int(content_split[2].split('.')[0])
            
                inc_balance = ed.get_item_data(DB_NAME, content_split[1], 'balance')
                inc_stocks =  ed.get_item_data(DB_NAME, content_split[1], 'stocks')
                
                sum = int(balance) + price
                sub = int(inc_balance) - price
                
                ed.give_item_data(DB_NAME, content_split[1], 'balance', sub)
                ed.give_item_data(DB_NAME, user_id, 'balance', sum)
                
                inventory[content_split[1]] = inventory.get(content_split[1], 0) - int(content_split[2])
                
                ed.give_item_data(DB_NAME, user_id, 'inventory', inventory)
                
                sub = int(ed.get_item_data(DB_NAME, content_split[1], 'stocks')) - int(content_split[2])
                
                ed.give_item_data(DB_NAME, content_split[1], 'stocks', sub)
                ed.give_item_data(DB_NAME, content_split[1], 'grafic', '🔻')
                
                cooldown_set(user_id, f'inc_store buy {content_split[1]}')
                
                text = f'<a:yes:998468643627212860> **Успешная продажа** {content_split[2]} акций компании {content_split[1]} за {currency}**{price}**'
        
    
    embed1 = discord.Embed(
    title = 'Рынок акций',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inc_stocks(message, *, content):
    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'inventory'):
        inventory = ed.give_item_data(DB_NAME, user_id, 'inventory', {})
    inventory = ed.get_item_data(DB_NAME, user_id, 'inventory')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
    
    if cooldown_check(user_id, f'inc_stocks {content}', 345600) != True:
        wait = cooldown_check(user_id, f'inc_store sell {content}', 345600)
        embed2 = discord.Embed(
        title = '<a:no:998468646533869658> Пожалуйста, подождите',
        description = f'Осталось ждать: {wait} секунд',
        color = 0xffff00)
        await message.channel.send(embed = embed2)
        
        return
    
    text = f'<a:no:998468646533869658> Данного бизнеса не существует'

    if ed.is_item_exist(DB_NAME, content, 'grafic'):
        inc_balance = ed.get_item_data(DB_NAME, content, 'balance')
        inc_stock_percent = ed.get_item_data(DB_NAME, content, 'stock_percent')
        inv_stocks = inventory[content] or 0

        price = int(inc_stock_percent) * int(inc_balance) // 1000 * int(inv_stocks)

        sum = int(balance) + price
        sub = int(inc_balance) - price

        ed.give_item_data(DB_NAME, user_id, 'balance', sum)
        ed.give_item_data(DB_NAME, content, 'balance', sub)
        ed.give_item_data(DB_NAME, content, 'grafic', '🔻')
        
        cooldown_set(user_id, f'inc_stocks {content}')

        text = f'<a:yes:998468643627212860> **Успешная транзакция!**\n📤Отправитель: {content}\n📥Получатель: <@{user_id}>\n💸Сумма: {currency}**{price}**\n📄Комиссия: **0**%'
    
    embed1 = discord.Embed(
    title = 'Дивиденды',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def inventory(message):
    user_id = str(message.author.id)
    
    text = ''
    
    if not ed.is_item_exist(DB_NAME, user_id, 'inventory'):
        inventory = ed.give_item_data(DB_NAME, user_id, 'inventory', {})
    inventory = ed.get_item_data(DB_NAME, user_id, 'inventory')
    
    for item in inventory:
        if int(inventory[item]) != 0:
            text = text + f'{item}: {inventory[item]}\n'

    embed1 = discord.Embed(
    title = 'Инвентарь',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)
    
@client.command()
async def bank_up(message):

    user_id = str(message.author.id)

    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')

    if not ed.is_item_exist(DB_NAME, user_id, 'bank_limit'):
        bank_limit = ed.give_item_data(DB_NAME, user_id, 'bank_limit', config['bank_limit'])
    bank_limit = ed.get_item_data(DB_NAME, user_id, 'bank_limit')
    
    client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
    
    if int(balance) >= int(bank_limit) * 2:

        sub = int(balance) - int(bank_limit) * 2
        sum_client = client_bank_balance + int(bank_limit) * 2
        
        ed.give_item_data(DB_NAME, client_id, 'bank_balance', sum_client)
        ed.give_item_data(DB_NAME, user_id, 'balance', sub)
        ed.give_item_data(DB_NAME, user_id, 'bank_limit', int(bank_limit) * 2)
        text = f'📈 Вы успешно повысили свой лимит в банке в 2 раза за {currency}**{int(bank_limit) * 2}**'
    
    else:
        text = f'<a:no:998468646533869658> Нехватка средств!\n💸Нужная сумма: {currency}**{int(bank_limit) * 2}**'
    
    embed1 = discord.Embed(
    title = 'Банк',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def shop(message, *, content = 'None'): #обновить

    user_id = str(message.author.id)
    
    content_split = content.split()

    if not ed.is_item_exist(DB_NAME, user_id, 'balance'):
        balance = ed.give_item_data(DB_NAME, user_id, 'balance', config['balance'])
    balance = ed.get_item_data(DB_NAME, user_id, 'balance')
        
    if not ed.is_item_exist(DB_NAME, user_id, 'currency'):
        currency = ed.give_item_data(DB_NAME, user_id, 'currency', config['currency'])
    currency = ed.get_item_data(DB_NAME, user_id, 'currency')
    
    guild = client.get_guild(int(message.guild.id))

    if content_split[0] == 'add' and message.author.guild_permissions.administrator and len(content_split) == 3:
        
        role_id = ''
        for l in content_split[1]:
            if l.isdigit():
                role_id = role_id + str(l)
        
        role = guild.get_role(int(role_id))
        
        if role and content_split[2].isdigit():
            
            ed.give_item_data(DB_NAME, str(message.guild.id), str(role_id), content_split[2])
            
            text = f'<a:yes:998468643627212860> **Вы успешно выставили роль** {content_split[1]} за **{currency}{content_split[2]}**'

    elif content_split[0] == 'None':
        text = ''
        shop = ed.get_id_data(DB_NAME, str(message.guild.id))
        
        for i in shop:
            
            text = text + f'<@&{i}>: **{currency}{shop[i]}**\n'
        
    elif content_split[0] == 'reset' and message.author.guild_permissions.administrator:
        
        ed.delete_id_data(DB_NAME, str(message.guild.id))
        
        text = f'<a:yes:998468643627212860> **Вы успешно сбросили магазин сервера**'
        
    elif content_split[0] == 'buy' and len(content_split) == 2:
        
        role_id = ''
        for l in content_split[1]:
            if l.isdigit():
                role_id = role_id + str(l)
                
        if ed.is_item_exist(DB_NAME, str(message.guild.id), role_id):
            
            role = guild.get_role(int(role_id))
            
            if balance > int(ed.get_item_data(DB_NAME, str(message.guild.id), role_id)):
                price = int(ed.get_item_data(DB_NAME, str(message.guild.id), role_id))
                
                sub = balance - price
                
                ed.give_item_data(DB_NAME, user_id, 'balance', sub)
                
                await message.author.add_roles(role)
                
                text = f'<a:yes:998468643627212860> **Вы успешно купили** роль {content_split[1]}'
        else:
            text = f'<a:no:998468646533869658> Ошибка взаимодействия\nВозможные причины:\n- Нехватка средств\n- Данная роль не продается'
                
        
        
        
    
    embed1 = discord.Embed(
    title = 'Офицальный магазин',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.command()
async def news(message):
    version = '2.0.1'
    when = '01.05.2024'
    text = f'**Версия**: *v.{version}*\n**Дата обновления**: {when}\n**Изменения:**\n- Теперь в мире деньги не бесконечны. Они берутся из фонда, который конечен.\n- Сделана команда `>inc_set` для настройки показателей бизнеса, например кол-во акций и их доля.\n- Здания бизнеса были сбалансированны'
    embed1 = discord.Embed(
    title = 'Обновления',
    description = text,
    color = 0xffff00)
    await message.channel.send(embed = embed1)

client.remove_command('help')
@client.command()
async def help(message):
    embed1 = discord.Embed(
    title = 'Помощь',
    description = 'Документация: [Click](https://docs.google.com/document/d/1QI_4Ye-nl4sGJo4N6G45699uZ6UwIhgSeuf_cWwejFw/edit?usp=sharing)',
    color = 0xffff00)
    await message.channel.send(embed = embed1)

@client.event
async def on_command_error(message, error):  

    if isinstance(error, commands.MissingRequiredArgument):
        embed1 = discord.Embed(
        title = 'Ошибка',
        description = f'<a:no:998468646533869658> Проверьте написание команды или запрошенные ею аргументы! (в команде `>help`, то что `<`в скобочках`>`)',
        color = 0xffff00)
        await message.channel.send(embed = embed1)

        user = await client.fetch_user(user_id=986313671661727744)
        await user.send(error)
        
        bb.add('system', error)


    elif isinstance(error, commands.errors.CommandInvokeError):    
        embed1 = discord.Embed(
        title = 'Ошибка',
        description = f'<a:no:998468646533869658> Отсутствие данных',
        color = 0xffff00)
        await message.channel.send(embed = embed1)

        user = await client.fetch_user(user_id=986313671661727744)
        await user.send(error)
        
        bb.add('system', error)

    elif isinstance(error, commands.CommandNotFound):
        embed1 = discord.Embed(
        title = 'Ошибка',
        description = f'<a:no:998468646533869658> Такой команды **не существует**, проверьте в `>help`!',
        color = 0xffff00)
        await message.channel.send(embed = embed1)

        user = await client.fetch_user(user_id=986313671661727744)
        await user.send(error)
        
        bb.add('system', error)


    else:
        embed1 = discord.Embed(
        title = 'Неизвестная ошибка',
        description = f'<a:no:998468646533869658> {error}',
        color = 0xffff00)
        await message.channel.send(embed = embed1)

        user = await client.fetch_user(user_id=986313671661727744)
        await user.send(error)
        
        bb.add('system', error)

@client.event
async def on_message(message):
    await client.process_commands(message)
    user_id = str(message.author.id)

    global messages
    messages += 1
    
    cmd_list = ['help', 'news', 'shop', 'bank_up', 'inventory', 'inc_stocks', 'inc_store', 'inc_set', 'inc_withdraw', 'set_currency', 'badge', 'inc_info', 'inc_up', 'inc_create', 'bal', 'bonus', 'pay', 'deposit', 'withdraw', 'hack', 'set_work', 'skill_up']
    
    if message.content.startswith('>'):
        if message.content.replace('>', '').split()[0] in cmd_list:
            bb.add(user_id, message.content.replace('>', ''))
            return
        
    
    elif messages % 10 == 0:
        for i in ed.ids(DB_NAME):
            if ed.is_item_exist(DB_NAME, i, 'grafic'):
                stock_price = int(ed.get_item_data(DB_NAME, i, 'balance')) * int(ed.get_item_data(DB_NAME, i, 'stock_percent')) // 100
                ed.give_item_data(DB_NAME, i, 'stock_price', stock_price)
    
    elif messages % 4 == 0:
        work = ed.get_item_data(DB_NAME, user_id, 'work')
        business = ed.get_item_data(DB_NAME, user_id, 'business')
        if work != 'Отсутствует' and business == 'Отсутствует':
            inc_ad = ed.get_item_data(DB_NAME, work, 'ad')
            balance = ed.get_item_data(DB_NAME, user_id, 'balance')
            client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
            
            try:
                sum = balance + inc_ad
                sub_client = client_bank_balance - inc_ad
        
                ed.give_item_data(DB_NAME, client_id, 'bank_balance', sub_client)
                ed.give_item_data(DB_NAME, user_id, 'balance', sum)
            except:
                bb.add('system', f'salary payment error')
            
        elif business != 'Отсутствует':
            inc_ad = ed.get_item_data(DB_NAME, business, 'ad')
            inc_building = ed.get_item_data(DB_NAME, business, 'building')
            balance = ed.get_item_data(DB_NAME, business, 'balance')
            client_bank_balance = int(ed.get_item_data(DB_NAME, client_id, 'bank_balance'))
            
            try:
                sum = int(balance) + int(inc_ad) * int(inc_building) ** 2
                
                sub_client = client_bank_balance - int(inc_ad) * int(inc_building) ** 2
        
                ed.give_item_data(DB_NAME, client_id, 'bank_balance', sub_client)
                ed.give_item_data(DB_NAME, business, 'balance', sum)
            except:
                bb.add('system', f'business salary payment error')
            
client.run("OTk4MjU2NTAyOTQwOTA1NTQy.GMbFaw.OXPEQs0-zFZ6ahWXu3nlrW3WX-Xi1yzcRDLXkg", bot=True) #запускаем бота
