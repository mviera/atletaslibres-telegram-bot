#!/usr/bin/env python3

import os
import sys
import re
sys.path.insert(0, './vendor')
import telebot


global CHAT_ID
# Atletas Libres (prod)
CHAT_ID = -1001423990122

# Atletas Libres v2 (dev)
# CHAT_ID = -1001274720989
BOT_TOKEN = os.environ['TELEGRAM_TOKEN']
bot = telebot.TeleBot(BOT_TOKEN)


text_messages = {
    'welcome':
        u'Bienvenido {name}!\n'
        u'Las bases de este grupo son el deporte,'
        u' compañerismo y motivación.\n'
        u'Algunos consejos:\n'
        u' 1) Evita temas conflictivos (política, religión, etc)'
        u' y mantén el buen ambiente en el grupo.\n'
        u' 2) Silencia el grupo si no quieres ser'
        u' molestado a cualquier hora.\n'
        u' 3) Si decides abandonar el grupo solo despídete, no es'
        u' necesario justificar nada, pero por cortesía'
        u' al menos unas palabras.\n'
        u' 4) No menciones a nadie pasadas las 00h. Así evitamos molestar'
        u' a otros compañeros.\n'
        u' 5) Digan lo que te digan en el grupo, no es obligatorio invitar'
        u' a cerveza :-D\n'
        u'Para cualquier otra cosa, dudas, ánimo u orientación'
        u' somos todo oídos.'
}


@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def on_user_joins(message):
    # name = message.new_chat_members.first_name
    name = ''
    if 'first_name' in message.json['new_chat_members'][0] and \
       message.json['new_chat_members'][0]['first_name'] is not None:
        name += u"{}".format(message.json['new_chat_members'][0]['first_name'])

    if 'username' in message.json['new_chat_members'][0] and \
       message.json['new_chat_members'][0]['username'] is not None:
        name += u"(@{})".format(message.json['new_chat_members'][0]['username'])

    bot.send_message(CHAT_ID, text_messages['welcome'].format(name=name))


@bot.message_handler(commands=['say'])
def say_something(message):
    msg = message.text.replace('/say ', '')
    bot.send_message(CHAT_ID, msg)


@bot.message_handler(func=lambda message: True)
def joke(message):
    matches = ["estoy", "gordo"]

    if all(x in message.text for x in matches):
        vowels = re.compile('[aeiou]', flags=re.I)
        mimimi = vowels.sub('i', message.text)
        bot.reply_to(message, mimimi)


bot.polling()
