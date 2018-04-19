import telebot
import sqlite3
import constants
import random

bot = telebot.TeleBot(constants.token)
db = sqlite3.connect('players.db', check_same_thread=False)
c = db.cursor()

def shop(message):
    exp = random.randint(1,100)
    gold = random.randint(1,10)
    bot.send_message(message.chat.id, 'Ты вернудся из магазина. К счастью всё обошлось и ты вернулся невредимым.'
                                      'Да ещё и кассир ошибся и дал больше сдачи\n\n'
                                      'Получено:\n'
                                      'Опыт: '+str(exp)+'\nИнкруции: '+str(gold))
    c.execute("SELECT gold FROM player WHERE id="+str(message.chat.id))
    last1 = c.fetchone()
    print(last1[0])
    new_gold = last1[0] + gold
    c.execute("SELECT exp FROM player WHERE id="+str(message.chat.id))
    last2 = c.fetchone()
    print(last2[0])
    new_exp = last2[0] + exp
    print(int(new_exp))
    c.execute("UPDATE player SET gold = "+str(new_gold)+", exp = "+str(new_exp)+", status=1 WHERE id="+str(message.chat.id))
    db.commit()
    if int(new_exp) >= 10000:
        c.execute('SELECT lvl FROM player WHERE id='+str(message.chat.id))
        lvl = c.fetchone()
        new_lvl = lvl[0] + 1
        new_exp2 = new_exp - 10000
        c.execute('UPDATE player SET lvl = '+str(new_lvl)+', exp ='+str(new_exp2)+' WHERE id='+str(message.chat.id))
        db.commit()