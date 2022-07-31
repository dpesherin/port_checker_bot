from datetime import datetime, timedelta
from core.ping import myping
from aiogram import Bot
from create_bot import dp, bot
import asyncio
import sqlite3 as sl

con = sl.connect('ping.db')

cur = con.cursor()

async def message(id, body):
    await bot.send_message(id, body)

now = str(datetime.now().timestamp()).split('.')[0]
next_time = str((datetime.now() + timedelta(minutes=2)).timestamp()).split('.')[0]
print(now)
print(next_time)

cur.execute("SELECT * FROM tasks_runner WHERE next_check BETWEEN "+now+" AND "+next_time+";")
res = cur.fetchall()
if(len(res) > 0):
    for i3 in range(0, len(res)):
        service_id = res[i3][2]
        notify = res[i3][3]
        cur.execute("SELECT url, port, user_created, period FROM services WHERE id="+str(service_id)+";")
        service = cur.fetchone()
        print(service)
        responce = myping(service[0], service[1])
        time = str((datetime.now() + timedelta(minutes=service[3])).timestamp()).split('.')[0]
        cur.execute("UPDATE tasks_runner SET next_check="+time+" WHERE id="+str(res[i3][0])+";")
        con.commit()
        if(responce):
            if(notify == 0):
                cur.execute("SELECT * FROM user WHERE id="+str(service[2])+";")
                user = cur.fetchone()
                cur.execute("UPDATE tasks_runner SET notify=1 WHERE id="+str(res[i3][0])+";")
                con.commit()
                loop = asyncio.get_event_loop()
                loop.run_until_complete(message(user[1], "Сервис "+service[0]+ " снова доступен. Порт: "+str(service[1])))
            else:
                pass
        else:
            if(notify == 0):
                pass
            else:
                cur.execute("UPDATE tasks_runner SET notify=0 WHERE id="+str(res[i3][0])+";")
                con.commit()
                cur.execute("SELECT * FROM user WHERE id="+str(service[2])+";")
                user = cur.fetchone()
                loop = asyncio.get_event_loop()
                loop.run_until_complete(message(user[1], "Сервис "+service[0]+ " недоступен. Порт: "+str(service[1])))

else:
    pass


