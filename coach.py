#!/usr/bin/env python3

import os
import sys
import re
import random
import time
from threading import Thread
from time import sleep
sys.path.insert(0, './vendor')
import telebot
import schedule


global CHAT_ID
# Atletas Libres (prod)
CHAT_ID = -1001423990122

# Atletas Libres v2 (dev)
#CHAT_ID = -1001274720989
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
        u' somos todo oídos.',

    'motivation_quotes': [
        u'Nunca he sido pobre, solo he estado sin dinero.\nSer pobre es un' \
        u' estado mental. No tener dinero es una condición temporal',
        u'Si hay que empezar de cero, pues se empieza',
        u'Si quires algo que nunca has tenido, tendrás que hacer algo que' \
        u' nunca has hecho',
        u'Eres tu contra ti mismo',
        u'No te enfades. La gente no te hace cosas, simplemente hace cosas.' \
        u' Tú decides si te afectan o no',
        u'Si mejoras cada día un 1%, en un año habrás mejorado un 365%',
        u'Entrenar es como el matrimonio, si haces trampa no funciona',
        u'La pregunta no es ¿puedes? La pregunta es ¿quieres?',
        u'Me visto de negro cuando voy al Gym porque es el funeral de mis' \
        u' calorías',
        u'Integridad es hacer lo correcto aunque nadie esté mirando',
    ]
}

single_exercises = {
    'Pushups': [10, 25, 50],
    'Negative Pushups': [10, 25, 50],
    'Situps': [10, 25, 50],
    'Squats': [10, 25, 50],
    'Lunges': [10, 25, 50],
    'Bear Walk': ['1x10m', '2x10m'],
    'Burpees': [10, 25],
    'Cat Cow': [10, 25, 50],
    'Climbers': [10, 25, 50],
    'Jumping Jacks': [10, 25, 50],
    'Leg Raises': [10, 25, 50],
    'Pikes': [10, 25, 50],
    'Plank Knees-to-chest': [10, 25, 50],
    'Scissors Kicks': [10, 25, 50],
}


@bot.message_handler(commands=['challenge'])
def weekly_challenge(message):

    challenge_lock = 'weekly_challenge.lock'

    def create_challenge():
        NUM_MAX_EXERCISES = 5
        NUM_ROUNDS = 3
        challenge = {}
        for n in range(NUM_MAX_EXERCISES):
            exercise = random.choice(list(single_exercises.keys()))
            reps = random.choice(single_exercises[exercise])
            challenge[exercise] = reps
            single_exercises.pop(exercise)

        msg = u"¡Atletas!\nEl reto para esta semana es:\n" + str(NUM_ROUNDS) + " RONDAS\n"
        for i in challenge:
            if i == 'Bear Walk':
                msg += u" » " + str(challenge[i]) + " " + i + "\n"
            else:
                msg += u" » " + str(challenge[i]) + "x " + i + "\n"

        msg += u"\n¡Ánimo! #NOEXCUSES"
        print(msg)
        bot.send_message(CHAT_ID, msg, parse_mode= 'Markdown')


    if not os.path.exists(challenge_lock):
        open(challenge_lock, 'w')
        create_challenge()

    else:
        now = time.time()
        #a_week = 7 * 86400
        a_week = 60

        if os.stat(challenge_lock).st_mtime < now - a_week:
            os.remove(challenge_lock)
            create_challenge()

        else:
            msg = u"¡Atletas! ¿Cómo lleváis el reto semanal?\n" \
                    "Aún hay tiempo, ¡Vamos! #NOEXCUSES"
            bot.send_message(CHAT_ID, msg, parse_mode= 'Markdown')


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)


def monday_message():
    text = u'Burros días!\nEs Lunes, vamos a darlo todo esta semana!'
    audio = open('media/good-morning-vietnam.mp3', 'rb')
    bot.send_message(CHAT_ID, text)
    bot.send_audio(CHAT_ID, audio)


def daily_message():
    #text = u'¡Burros días!\n¡Vamos a por el día!\n'
    text = u'¡Burros días!\n¿Qué tal esos cuerpos serranos?!\n'
    random_quote = random.randint(0, len(text_messages['motivation_quotes']) -1)
    audio = open('media/good-morning-vietnam.mp3', 'rb')
    bot.send_message(CHAT_ID, text + "«" + text_messages['motivation_quotes'][random_quote] + '»',
                     parse_mode= 'Markdown')
#   bot.send_audio(CHAT_ID, audio)


@bot.message_handler(func=lambda m: True, content_types=['new_chat_members'])
def on_user_joins(message):
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


@bot.message_handler(commands=['motivation'])
def say_something(message):
    random_quote = random.randint(0, len(text_messages['motivation_quotes']) -1)
    bot.send_message(CHAT_ID, "«" +
                     text_messages['motivation_quotes'][random_quote] + '»',
                     parse_mode= 'Markdown')


@bot.message_handler(func=lambda message: True)
def joke(message):
    matches = ["estoy", "gordo"]

    if all(x in message.text for x in matches):
        vowels = re.compile('[aeiou]', flags=re.I)
        mimimi = vowels.sub('i', message.text)
        bot.reply_to(message, mimimi)

schedule.every().monday.at("09:00").do(monday_message)
schedule.every().day.at("09:05").do(daily_message)
Thread(target=schedule_checker).start()
bot.polling()
