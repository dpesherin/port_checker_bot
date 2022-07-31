from nturl2path import url2pathname
from tabnanny import check
from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_del
from keyboards import kb_admin
from keyboards import kb_agreement
from core.db import cur, con
from core.tools import check_reg, myping
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime, timedelta


class FSMAddTask(StatesGroup):
    url = State()
    port = State()
    timing = State()
    check = State()

class FSMDelTask(StatesGroup):
    getId = State()
    result = State()

async def start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Бот успешно запущен', reply_markup=kb_admin)

#ADD TASK___________________________________________________________________________________________________

#Run add process
async def add_task(message: types.Message):
    res = check_reg(str(message.from_user.id))
    if(res):
        await FSMAddTask.url.set()
        await bot.send_message(message.from_user.id, 'Введите url (http://examlpe.com; http://examlpe.com; xxx.xxx.xxx.xxx)')
    else:
        await bot.send_message(message.from_user.id, 'Вы не зарегистрированы')

#Get target url
async def set_url(message: types.Message, state: FSMContext):
    count = 0
    global url
    url = message.text
    print(url)
    if('http://' in url or 'https://' in url):
        await FSMAddTask.next()
        await bot.send_message(message.from_user.id, 'Введите port. Пример: 80')
    else:
        if('192.168' in url):
            await FSMAddTask.url.set()
            await bot.send_message(message.from_user.id, 'Вы не можете слушать порты в локальной сети бота. Введите заново')
        else:
            try:
                if(url.count('.') == 3):
                    url_data = url.split('.')
                    for el in range(0, len(url_data)):
                        try:
                            check_data = int(url_data[el])
                            if(check_data <= 999):
                                pass
                            else:
                                count = count +1
                        except:
                            await FSMAddTask.url.set()
                            await bot.send_message(message.from_user.id, 'Неправильный URL. Введите заново')
                    if(count == 0):
                        await FSMAddTask.next()
                        await bot.send_message(message.from_user.id, 'Введите port. Пример: 80')
                    else:
                        await FSMAddTask.url.set()
                        await bot.send_message(message.from_user.id, 'Неправильный URL. Введите заново')
                else:   
                    await FSMAddTask.url.set()
                    await bot.send_message(message.from_user.id, 'Неправильный URL. Введите заново')
            except:
                await FSMAddTask.url.set()
                await bot.send_message(message.from_user.id, 'Неправильный URL. Введите заново')

#Get target port
async def set_port(message: types.Message, state: FSMContext):
    global port
    try:
        port = int(message.text)
        if(port > 0):
            print(port)
            await FSMAddTask.timing.set()
            await bot.send_message(message.from_user.id, 'Введите период опроса (мин)')
        else:
            await FSMAddTask.port.set()
            await bot.send_message(message.from_user.id, 'Порт должен быть положительным')
    except:
        await FSMAddTask.port.set()
        await bot.send_message(message.from_user.id, 'Порт не может быть строковым.')
    
# Get timing for request
async def set_timing(message: types.Message, state: FSMContext):
    global timing
    try:
        timing = int(message.text)
        if(timing > 0):
            await FSMAddTask.check.set()
            await bot.send_message(message.from_user.id, 'Проверяю данные...')
            global target_port
            target_port = str(port)
            res = myping(url, port)
            if(res):
                success = "YES"
            else:
                success = "NO"
            await bot.send_message(message.from_user.id, 'Host: '+url+'\nPort: '+target_port+'\nSuccess: '+success,reply_markup=kb_agreement)
        else:
            await FSMAddTask.timing.set()
            await bot.send_message(message.from_user.id, 'Период должен быть положительным') 
    except Exception as exc:
        print(exc)
        await FSMAddTask.timing.set()
        await bot.send_message(message.from_user.id, 'Период должен быть целым числом') 

#Check connection
async def check(message: types.Message, state: FSMContext):
    if(message.text == "Сохранить"):
        cur.execute("SELECT * FROM user WHERE tg_id =" + str(message.from_user.id) +";")
        res = cur.fetchone()
        print(res[0])
        data = (str(timing), url, str(port), str(res[0]))
        try:
            cur.execute("INSERT INTO services (period, url, port, user_created) VALUES(?, ?, ?, ?)", data)
            con.commit()
            service_id = str(cur.lastrowid)
            print(service_id)
            time = str((datetime.now() + timedelta(minutes=timing)).timestamp()).split('.')[0]
            data_runner = (time, service_id, '1')
            cur.execute("INSERT INTO tasks_runner(next_check, service_id, notify) VALUES(?, ?, ?)", data_runner)
            con.commit()
            await bot.send_message(message.from_user.id, 'Запись сохранена', reply_markup=kb_admin)
        except Exception as ex:
            print(ex)
            await bot.send_message(message.from_user.id, 'Server Error', reply_markup=kb_admin)
    else:
        await bot.send_message(message.from_user.id, 'Отмена сохранения', reply_markup=kb_admin)
    await state.finish()

#----Delete task__________________________________________________________________________________________

async def delete_task(message: types.Message, state=None):
    res = check_reg(str(message.from_user.id))
    if(res):
        cur.execute("SELECT * FROM user WHERE tg_id =" + str(message.from_user.id) +";")
        user_id = cur.fetchone()
        cur.execute("SELECT * FROM services WHERE user_created =" + str(user_id[0]) +";")
        service_list = cur.fetchall()
        if(len(service_list)==0):
            await bot.send_message(message.from_user.id, 'Список мониторинга пуст')
            await state.finish()
        else:
            body = ""
            for i3 in range(0, len(service_list)):
                body = body + "\nID: "+str(service_list[i3][0])+"\nАдрес: "+service_list[i3][2]+"\nПорт: "+str(service_list[i3][3])+"\nПроверяется: раз в "+str(service_list[i3][1])+" минут\n_____________"
            await FSMDelTask.getId.set()
            await bot.send_message(message.from_user.id, 'Выберите id записи для удаления:'+ body)
    else:
        await bot.send_message(message.from_user.id, 'Вы не зарегистрированы')

async def get_id(message: types.Message, state: FSMContext):
    global task_id
    task_id = message.text
    try:
        condidate = int(task_id)
        cur.execute("SELECT * FROM services WHERE id =" + task_id +";")
        res = cur.fetchone()
        body = "Выбранная запись:\nID: "+str(res[0])+"\nАдрес: "+res[2]+"\nПорт: "+str(res[3])+"\nПроверяется: раз в "+str(res[1])+" минут"
        await FSMDelTask.result.set()
        await bot.send_message(message.from_user.id, body, reply_markup=kb_del)
    except:
        await bot.send_message(message.from_user.id, 'ID должен быть числом')

async def result(message: types.Message, state: FSMContext):
    if(message.text == "Удалить"):
        cur.execute("DELETE FROM tasks_runner WHERE service_id =" + task_id +";")
        con.commit()
        cur.execute("DELETE FROM services WHERE id =" + task_id +";")
        con.commit()
        await bot.send_message(message.from_user.id, 'Удаление завершено', reply_markup=kb_admin)
    else:
        await bot.send_message(message.from_user.id, 'Удаление завершено', reply_markup=kb_admin)
    await state.finish()

async def view_tasks(message: types.Message):
    res = check_reg(str(message.from_user.id))
    if(res):
        cur.execute("SELECT * FROM user WHERE tg_id =" + str(message.from_user.id) +";")
        user_id = cur.fetchone()
        cur.execute("SELECT * FROM services WHERE user_created =" + str(user_id[0]) +";")
        service_list = cur.fetchall()
        if(len(service_list)==0):
            await bot.send_message(message.from_user.id, 'Список мониторинга пуст', reply_markup=kb_admin)
        else:
            body = ""
            for i3 in range(0, len(service_list)):
                body = body + "\nID: "+str(service_list[i3][0])+"\nАдрес: "+service_list[i3][2]+"\nПорт: "+str(service_list[i3][3])+"\nПроверяется: раз в "+str(service_list[i3][1])+" минут\n_____________"
            await bot.send_message(message.from_user.id, 'Список мониторинга:'+body, reply_markup=kb_admin)
async def register(message: types.Message):
    id = str(message.from_user.id)
    res = check_reg(id)
    if(res):
        await bot.send_message(message.from_user.id, 'Вы уже зарегистрированы')
    else:
        cur.execute("INSERT INTO user (tg_id) VALUES("+id+")")
        con.commit()
        await bot.send_message(message.from_user.id, 'Регистрация прошла успешно')

def register_handler_admin(dp : Dispatcher):
    dp.register_message_handler(start, commands=['start'])
    dp.register_message_handler(add_task, commands=['Добавить_задачу'], state=None)
    dp.register_message_handler(set_url, state=FSMAddTask.url)
    dp.register_message_handler(set_port, state=FSMAddTask.port)
    dp.register_message_handler(set_timing, state=FSMAddTask.timing)
    dp.register_message_handler(check, state=FSMAddTask.check)
    dp.register_message_handler(delete_task, commands=['Удалить_задачу'])
    dp.register_message_handler(get_id, state=FSMDelTask.getId)
    dp.register_message_handler(result, state=FSMDelTask.result)
    dp.register_message_handler(view_tasks, commands=['Показать_задачи'])
    dp.register_message_handler(register, commands=['Регистрация'])