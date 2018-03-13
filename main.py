import telebot
import sqlite3
import constants
import TextData
from telebot import types

########################################DATA_CONTAINER######################################################
bot = telebot.TeleBot(constants.token)
markup_guild = types.ReplyKeyboardMarkup(True)
markup_guild.row('🌸Академия Сияющих Лепестков', '🛡⚔️Академия Защитников')
markup_guild.row('❄️Академия Города Инея', '🖤Академия Бездушных', '🐉Академия Города Драконов')
conn_players = sqlite3.connect('players.db', check_same_thread=False)
c_players = conn_players.cursor()
conn_stats = sqlite3.connect('stats.db',check_same_thread=False)
c_stats = conn_stats.cursor()
texts = TextData
############################################################################################################


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        c_players.execute('SELECT status FROM player WHERE id='+str(message.chat.id))
        last = c_players.fetchone()
        print(last)
        if last is None:
            try:
                bot.send_message(message.chat.id, 'Добро пожаловать. Выбери свою академию:', reply_markup=markup_guild)
                c_players.execute("INSERT INTO player VALUES ('" + str(message.chat.id) + "','" + str(message.from_user.first_name) + "','1','5','0')")
                c_stats.execute("INSERT INTO stats VALUES ('"+str(message.chat.id)+"','1','1','1','1')")
                conn_players.commit()
                conn_stats.commit()
            except:
                bot.send_message(message.chat.id,'Ты не выбрал академию до продолжения', reply_markup=markup_guild)
        else:
            bot.send_message(message.chat.id, texts.profile)


@bot.message_handler(commands=['me'])
def me(message):
    c_stats.execute("SELECT * FROM stats WHERE id=" + str(message.chat.id))
    c_players.execute("SELECT * FROM player WHERE id=" + str(message.chat.id))
    stats = str(c_stats.fetchall())
    info = str(c_players.fetchall())
    print(stats + ' ' + info)


@bot.message_handler(commands=['change_nick'])
def change_nick(message):
    text = message.text
    new_nick = text.split(' ')
    try:
        print(new_nick[1])
    except:
        bot.send_message(message.chat.id, 'Правильное использование команды - /change_nick новый_ник.'
                                          ' ВНИМАНИЕ! Ник может состоять только из одного слова. '
                                          'В ином случае в качестве ника'
                                          'будет выступать только первое слово.')
    else:
        try:
            c.execute("SELECT nick_change FROM player WHERE id="+str(message.from_user.id))
            nick_change = c.fetchone()
            if nick_change[0] == 0:
                bot.send_message(message.chat.id,'Ты не можешь сменить ник. Обратись к администратору.')
            else:
                c_players.execute("UPDATE player SET nick = '"+str(new_nick[1]+"', nick_change = '0' WHERE id = "+str(message.from_user.id)))
                conn_players.commit()
                bot.send_message(message.chat.id, 'Надеюсь тебе нравится новое имя, '+str(new_nick))
        except:
            print('Err. no2 - Nick not Unique')

@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.chat.type == 'private':
        try:
            c_players.execute("SELECT status FROM player WHERE id="+str(message.from_user.id))
            status = c_players.fetchone()
            if status[0] == 0:
                c_players.execute("SELECT nick FROM player WHERE id="+str(message.chat.id))
                nick = c_players.fetchone()
                bot.send_message(message.chat.id, 'Ты был изгнан из своей академии, <b>' + str(nick[0])+'</b>.'
                                                                                              '\nДругие академии не хотят тебя принимать.'
                                                                                              ' Вечный позор тебе.', parse_mode='HTML')
            if status[0] == 1:
                if message.text == 'Профиль':
                    c_stats.execute("SELECT * FROM stats WHERE id=" + str(message.chat.id))
                    c_players.execute("SELECT * FROM player WHERE id="+str(message.chat.id))
                    stats = str(c_stats.fetchall())
                    info = str(c_players.fetchall())
                    print(stats + ' ' + info)
                    intl = stats[1]
                    dex = stats[3]
                    str = stats[2]
                    telo = stats[4]
                    nick = info[1]
                    status = info[3]
                    if info[5] == 1:
                        guild = '🌸Академии Сияющих Лепестков'
                    if info[5] == 2:
                        guild = '🛡⚔️Академии Защитников'
                    if info[5] == 3:
                        guild = '❄️Академии Города Инея'
                    if info[5] == 4:
                        guild = '🖤Академии Бездушных'
                    if info[5] == 5:
                        guild = '🐉Академии Города Драконов'
                    bot.send_message(message.chat.id, 'Профиль ученика ' + str(guild) + '\n'
                                                                                        'Ник - '+str(nick)+'\n'
                                                                                        'Статус -'+str(status)+'\n'
                                                                                        '\n'
                                                                                        'Текущие характеристики:\n'
                                                                                        'Интеллект - '+ str(intl)+'     Сила - '+str(strg)
                                                                                        '\nЛовкость - '+ str(dex) + '     Телосложение - '+str(telo))
            if status[0] == 5:
                if message.text == '🌸Академия Сияющих Лепестков':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!')
                    c_players.execute("UPDATE player SET status = 1, guild = 1 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '🛡⚔️Академия Защитников':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!')
                    c_players.execute("UPDATE player SET status = 1, guild = 2 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '❄️Академия Города Инея':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!')
                    c_players.execute("UPDATE player SET status = 1, guild = 3 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '🖤Академия Бездушных':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!')
                    c_players.execute("UPDATE player SET status = 1, guild = 4 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '🐉Академия Города Драконов':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!')
                    c_players.execute("UPDATE player SET status = 1, guild = 5 WHERE id="+str(message.chat.id))
                    conn_players.commit()
            else:
               bot.send_message(message.chat.id,'Админ чуть накосячил. Уже об этом знает. Сейчас исправит.')
        except:
            print('1')





try:
    bot.polling(none_stop=True)
except:
    print('Упал')


