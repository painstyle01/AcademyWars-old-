import sqlite3
import telebot
import constants

bot = telebot.TeleBot(constants.keeper_token)
c_players = sqlite3.connect('players.db', check_same_thread=False)
cur = c_players.cursor()


@bot.message_handler(content_types=['new_chat_members'])
def check_guild(message):
    uchatid = message.from_user.id
    cur.execute("SELECT guild WHERE id="+str(uchatid))
    guild = cur.fetchone()
    if message.chat.id == -1001387097774:
        if guild[0] is not 1:
            bot.kick_chat_member(message.chat.id, uchatid)
    if message.chat.id == #:
        if guild[0] is not 2:
            bot.kick_chat_member(message.chat.id, uchatid)
    if message.chat.id == -1001387097774:
        if guild[0] is not 3:
            bot.kick_chat_member(message.chat.id, uchatid)
    if message.chat.id == #:
        if guild[0] is not 4:
            bot.kick_chat_member(message.chat.id, uchatid)
    if message.chat.id == #:
        if guild[0] is not 5:
            bot.kick_chat_member(message.chat.id, uchatid)



@bot.message_handler(commands=['id'])
def id(message):
    bot.send_message(message.chat.id, 'ИД чата - ' + str(message.chat.id))


if __name__ == '__main__':
    try:
        bot.polling(none_stop=True)
    except:
        print('Мне плохо')
