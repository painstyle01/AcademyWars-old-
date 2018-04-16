import telebot
import sqlite3
import constants
import threading
import quests
import TextData
from telebot import types

########################################DATA_CONTAINER######################################################
bot = telebot.TeleBot(constants.token)
markup_guild = types.ReplyKeyboardMarkup(True)
markup_guild.row('🌸Академия Сияющих Лепестков', '🛡⚔️Академия Защитников')
markup_guild.row('❄️Академия Города Инея', '🖤Академия Бездушных', '🐉Академия Города Драконов')
markup_main = types.ReplyKeyboardMarkup(True)
markup_main.row('🎫Профиль', '⚙️Квесты', '🏃Перемещение')
markup_main.row('Общение', 'Лавка академии')
markup_move = types.ReplyKeyboardMarkup(True)
markup_move.row('Столица', 'Арена', 'Тёмный уголок')
markup_move.row('❄️Академия Города Инея', '🖤Академия Бездушных', '🐉Академия Города Драконов')
markup_move.row('🌸Академия Сияющих Лепестков', '🛡⚔️Академия Защитников')
markup_move.row('❌Отмена')
markup_quests = types.ReplyKeyboardMarkup(True)
markup_quests.row('🍪Поход в магазин')
conn_players = sqlite3.connect('players.db', check_same_thread=False)
c_players = conn_players.cursor()
conn_stats = sqlite3.connect('stats.db',check_same_thread=False)
c_stats = conn_stats.cursor()
texts = TextData
############################################################################################################


@bot.message_handler(commands=['set_lvl'])
def new_lvl(message):
    bot.send_message(message.chat.id, '1')
    c_players.execute('UPDATE player SET exp = 10000 WHERE id='+str(message.chat.id))



@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        c_players.execute('SELECT status FROM player WHERE id='+str(message.chat.id))
        last = c_players.fetchone()
        print(last)
        if last is None:
            bot.send_message(message.chat.id, 'Добро пожаловать. Выбери свою академию:', reply_markup=markup_guild)
            c_players.execute("INSERT INTO player VALUES ('" + str(message.chat.id) + "','" + str(message.from_user.first_name) + "','1','5','0','0','1','0')")
            c_stats.execute("INSERT INTO stats VALUES ('"+str(message.chat.id)+"','1','1','1','1')")
            conn_players.commit()
            conn_stats.commit()
        else:
            if last[0] == 5:
                bot.send_message(message.chat.id, 'Ты не выбрал академию до продолжения', reply_markup=markup_guild)
            else:
                bot.send_message(message.chat.id,'С возвращением!', reply_markup=markup_main)
                print('lol')


@bot.message_handler(commands=['me'])
def me(message):
    try:
        c_stats.execute("SELECT * FROM stats WHERE id=" + str(message.chat.id))
        c_players.execute("SELECT * FROM player WHERE id=" + str(message.chat.id))
        stats = c_stats.fetchall()
        info = c_players.fetchall()
        stats2 = [str(x) for x in stats[0]]
        stats3 = [str(x) for x in info[0]]
        print(stats3)
        print(stats2)
        guild = 'None'
        if stats3[4] == '1':
            guild = '🌸Академии Сияющих Лепестков'
        if stats3[4] == '2':
            guild = '🛡⚔️Академии Защитников'
        if stats3[4] == '3':
            guild = '❄️Академии Города Инея'
        if stats3[4] == '4':
            guild = '🖤Академии Бездушных'
        if stats3[4] == '5':
            guild = '🐉Академии Города Драконов'
        bot.send_message(message.chat.id, 'Профиль ученика ' + guild + ''
                                                                   '\nНик - ' + stats3[1] + '\n'
                                                                                            'Уровень: '+stats3[6]+'\n'
                                                                                          'Статус -' + stats3[3] + '\n\n'
                                                                                                                 'Текущие характеристики:\n'
                                                                                                                 'Интеллект - ' + stats2[1] + '     Сила - ' + stats2[2] + '\nЛовкость - ' + stats2[3] + '     Телосложение - ' + stats2[4] + '\n\nИнкруции: '+stats3[7]+'\nОпыт: '+stats3[5], reply_markup=markup_main)
    except:
        print('NONONONONONON')

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
            c_players.execute("SELECT nick_change FROM player WHERE id="+str(message.from_user.id))
            nick_change = c_players.fetchone()
            if nick_change[0] == 0:
                bot.send_message(message.chat.id,'Ты не можешь сменить ник. Обратись к администратору.')
            else:
                c_players.execute("UPDATE player SET nick = '"+str(new_nick[1]+"', nick_change = '0' WHERE id = "+str(message.from_user.id)))
                conn_players.commit()
                bot.send_message(message.chat.id, 'Надеюсь тебе нравится новое имя, '+str(new_nick[1]))
        except:
            print('Err. no2 - Nick not Unique')

@bot.message_handler(content_types=['text'])
def text_handler(message):
    if message.chat.type == 'private':
        try:
            c_players.execute("SELECT status FROM player WHERE id="+str(message.from_user.id))
            status = c_players.fetchone()
            if message.text == '🎫Профиль':
                c_stats.execute("SELECT * FROM stats WHERE id=" + str(message.chat.id))
                c_players.execute("SELECT * FROM player WHERE id=" + str(message.chat.id))
                stats = c_stats.fetchall()
                info = c_players.fetchall()
                stats2 = [str(x) for x in stats[0]]
                stats3 = [str(x) for x in info[0]]
                print(stats3)
                print(stats2)
                guild = 'None'
                status = ' None'
                if stats3[3] == '1':
                    status = ' Свободен'
                if stats3 == '2':
                    status = ' Ушел в магазин'

                if stats3[4] == '1':
                    guild = '🌸Академии Сияющих Лепестков'
                if stats3[4] == '2':
                    guild = '🛡⚔️Академии Защитников'
                if stats3[4] == '3':
                    guild = '❄️Академии Города Инея'
                if stats3[4] == '4':
                    guild = '🖤Академии Бездушных'
                if stats3[4] == '5':
                    guild = '🐉Академии Города Драконов'
                bot.send_message(message.chat.id, 'Профиль ученика ' + guild + ''
                                                                               '\nНик - ' + stats3[1] + '\n'
                                                                                                        'Уровень: ' +
                                 stats3[6] + '\n'
                                             'Статус -' + status + '\n\n'
                                                                      'Текущие характеристики:\n'
                                                                      'Интеллект - ' + stats2[1] + '     Сила - ' +
                                 stats2[2] + '\nЛовкость - ' + stats2[3] + '     Телосложение - ' + stats2[
                                     4] + '\n\nИнкруции: ' + stats3[7] + '\nОпыт: ' + stats3[5] + '/10000',
                                 reply_markup=markup_main)
            if status[0] == 0:
                c_players.execute("SELECT nick FROM player WHERE id="+str(message.chat.id))
                nick = c_players.fetchone()
                bot.send_message(message.chat.id, 'Ты был изгнан из своей академии, <b>' + str(nick[0])+'</b>.'
                                                                                              '\nДругие академии не хотят тебя принимать.'
                                                                                              ' Вечный позор тебе.', parse_mode='HTML')
            if status[0] == 1:
                if message.text == '❌Отмена':
                    c_stats.execute("SELECT * FROM stats WHERE id=" + str(message.chat.id))
                    c_players.execute("SELECT * FROM player WHERE id=" + str(message.chat.id))
                    stats = c_stats.fetchall()
                    info = c_players.fetchall()
                    stats2 = [str(x) for x in stats[0]]
                    stats3 = [str(x) for x in info[0]]
                    print(stats3)
                    print(stats2)
                    guild = 'None'
                    if stats3[4] == '1':
                        guild = '🌸Академии Сияющих Лепестков'
                    if stats3[4] == '2':
                        guild = '🛡⚔️Академии Защитников'
                    if stats3[4] == '3':
                        guild = '❄️Академии Города Инея'
                    if stats3[4] == '4':
                        guild = '🖤Академии Бездушных'
                    if stats3[4] == '5':
                        guild = '🐉Академии Города Драконов'
                    bot.send_message(message.chat.id, 'Профиль ученика ' + guild + ''
                                                                                   '\nНик - ' + stats3[1] + '\n'
                                                                                                            'Уровень: ' +
                                     stats3[6] + '\n'
                                                 'Статус -' + stats3[3] + '\n\n'
                                                                          'Текущие характеристики:\n'
                                                                          'Интеллект - ' + stats2[1] + '     Сила - ' +
                                     stats2[2] + '\nЛовкость - ' + stats2[3] + '     Телосложение - ' + stats2[
                                         4] + '\n\nИнкруции: ' + stats3[7] + '\nОпыт: ' + stats3[5],
                                     reply_markup=markup_main)

                if message.text == '🏃Перемещение':
                    bot.send_message(message.chat.id, 'На данный момент ворота академии закрыты. '
                                                      'Следи за газетой. Наверное скоро откроют.')
                    #bot.send_message(message.chat.id, 'Выбери локацию для перемещения.', reply_markup=markup_move)
                if message.text == '🍪Поход в магазин':
                    bot.send_message(message.chat.id,
                                     'Ты отправился за покупками.'
                                     'В такое время может случится всякое, по этому будь на чеку.'
                                     'У тебя есть 5 минут что б вернуться в академию до темени. Не тормози!', reply_markup=markup_main)
                    c_players.execute("UPDATE player SET status=2 WHERE id=" + str(message.chat.id))
                    conn_players.commit()
                    threading.Timer(1, quests.shop, [message]).start()
                if message.text == '⚙️Квесты':
                    bot.send_message(message.chat.id, 'Выбери один из доступных квестов:', reply_markup=markup_quests)
            if status[0] == 5:
                if message.text == '🌸Академия Сияющих Лепестков':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!', reply_markup=markup_main)
                    c_players.execute("UPDATE player SET status = 1, guild = 1 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '🛡⚔️Академия Защитников':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!', reply_markup=markup_main)
                    c_players.execute("UPDATE player SET status = 1, guild = 2 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '❄️Академия Города Инея':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!', reply_markup=markup_main)
                    c_players.execute("UPDATE player SET status = 1, guild = 3 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '🖤Академия Бездушных':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!', reply_markup=markup_main)
                    c_players.execute("UPDATE player SET status = 1, guild = 4 WHERE id="+str(message.chat.id))
                    conn_players.commit()
                if message.text == '🐉Академия Города Драконов':
                    bot.send_message(message.chat.id, 'Добро пожаловать в новую академию!', reply_markup=markup_main)
                    c_players.execute("UPDATE player SET status = 1, guild = 5 WHERE id="+str(message.chat.id0))
                    conn_players.commit()
        except:
            print('1')





try:
    bot.polling(none_stop=True)
except:
    print('Упал')


