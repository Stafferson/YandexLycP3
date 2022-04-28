import json
import sqlite3
import types

import requests

#from telebot import types

import telebot

import Constants
from Dad_jokes import Dad_jokes
from GmailAPI import GmailAPI

bot = telebot.TeleBot("5201999855:AAHBknY49Tgo-BfVAKrQf7Lf4YE9M6LNCbU", parse_mode=None)

Status = 0

is_playing = False
is_random = False
is_dad_jokes = False

temp_email = "-1"

@bot.message_handler(commands=['start'])
def start(message):
    Constants.CURRENT_USER_EMAIL = None
    Constants.IS_LOGGED_IN = False
    global temp_email
    temp_email = "-1"
    bot.reply_to(message, "Welcome! If you want to know about some commands to start with, type the '/help' command")

@bot.message_handler(commands=['help'])
def help(message):
    if (Constants.IS_LOGGED_IN):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('/Apply_filter')
        markup.add(itembtn1)
        bot.reply_to(message, "Currently, bot support these functions: " + "\n" + "/dad_jokes")
    else:
        #bot.reply_to(message, "Before using any of my commands, you have to log into your account, if you have one, or register")
        markup = types.ReplyKeyboardMarkup(row_width=2)
        itembtn1 = types.KeyboardButton('Log in')
        itembtn2 = types.KeyboardButton('Register')
        itembtn3 = types.KeyboardButton('Forgot my password')
        markup.add(itembtn1, itembtn2, itembtn3)
        bot.send_message(str(message.chat.id), "Before using any of my commands, you have to log into your account, if you have one, or register", reply_markup=markup)

@bot.message_handler()
def checker(message):
    global Status
    global is_dad_jokes
    global is_random
    global is_playing
    global temp_email

    print(Status, "status")
    if (not Constants.IS_LOGGED_IN):
        if (message.text == 'Register'):
            bot.reply_to(message, "Send me your email")
            Status = 0
        elif (message.text == 'Log in'):
            bot.reply_to(message, "Send me your email")
            Status = 1
        elif (message.text == "Forgot my password"):
            bot.reply_to(message, "Send me your email")
            Status = 2
        else:
            print(temp_email, "tttttttttttttt", message.text)
            if (not (temp_email == "-1")):
                email = temp_email
                print("equalss\!!!!!")
            else:
                email = message.text
                temp_email = message.text
            print(temp_email)

            con = sqlite3.connect("yandex_lyc_p3.sqlite")
            cur = con.cursor()
            query = "SELECT EXISTS(SELECT 1 FROM Users WHERE email = '" + email + "');"
            res = cur.execute(query).fetchall()
            print(res, "DSDA")

            if (int(res[0][0]) == 1):
                if (Status == 0):
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    itembtn1 = types.KeyboardButton('Log in')
                    temp_email = "-1"
                    markup.add(itembtn1)
                    bot.send_message(str(message.chat.id), "Seems like you are already registered, try to log in", reply_markup=markup)
                elif (Status == 1):
                    #markup = types.ReplyKeyboardMarkup(row_width=2)
                    #itembtn1 = types.KeyboardButton('Register')
                    #markup.add(itembtn1)
                    temp_email = "-1"
                    bot.send_message(str(message.chat.id), "Send me your password")
                    Status = 3
                elif (Status == 2):
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    itembtn1 = types.KeyboardButton('Log in')
                    markup.add(itembtn1)
                    temp_email = "-1"
                    query = "SELECT password FROM Users WHERE email = '" + temp_email + "'"
                    res = cur.execute(query).fetchall()
                    print(res)
                    gapi = GmailAPI()
                    gapi.send_message_restore_password(email_to=email, user_password=str(res[0][0]))
                    bot.send_message(str(message.chat.id), "Password has just been sent! (Also try to check spam folder)", reply_markup=markup)
                elif (Status == 3):
                    query = "SELECT password FROM Users WHERE email = '" + temp_email + "'"
                    res = cur.execute(query).fetchall()
                    print(res)
                    if (str(res[0][0]) == message.text):
                        markup = types.ReplyKeyboardMarkup(row_width=2)
                        itembtn1 = types.KeyboardButton('/help')
                        markup.add(itembtn1)
                        Constants.IS_LOGGED_IN = True
                        bot.send_message(str(message.chat.id), "Log in successful, now you can try the help function",reply_markup=markup)
            else:
                if (Status == 0):
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    #itembtn1 = types.KeyboardButton('Log in')
                    #markup.add(itembtn1)
                    bot.send_message(str(message.chat.id), "Create a new password and send it to me", reply_markup=markup)
                    Status = 4
                elif (Status == 1):
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    #itembtn1 = types.KeyboardButton('Register')
                    #markup.add(itembtn1)
                    temp_email = "-1"
                    bot.send_message(str(message.chat.id), "There is no such account with this email", reply_markup=markup)
                elif (Status == 2):
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    #itembtn1 = types.KeyboardButton('Register')
                    #markup.add(itembtn1)
                    temp_email = "-1"
                    bot.send_message(str(message.chat.id), "There is no such account with this email", reply_markup=markup)
                elif (Status == 4):
                    markup = types.ReplyKeyboardMarkup(row_width=2)
                    itembtn1 = types.KeyboardButton('Log in')
                    markup.add(itembtn1)
                    password = message.text
                    query = "INSERT INTO Users(email, password) VALUES('" + temp_email + "', '" + password + "')";
                    cur.execute(query)
                    bot.send_message(str(message.chat.id), "Your account has just been created! Log in now", reply_markup=markup)
    else:
        if is_dad_jokes:
            dad_jokes = Dad_jokes()
            if (message.text == "Continue"):
                joke = dad_jokes.get_joke()
                bot.reply_to(message, joke['body'][0]['_id'] + '\n' + joke['body'][0]['setup'] + '\n' + joke['body'][0]['punchline'])
            elif (message.text == "Stop"):
                bot.reply_to(message, "Stop means stop, okay")
                is_dad_jokes = False

@bot.message_handler(commands=['dad_jokes'])
def dad_jokes(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Continue')
    itembtn2 = types.KeyboardButton('Stop')
    markup.add(itembtn1, itembtn2)
    bot.reply_to(message, "Hello '/dad_jokes', my name is Dad! If you want to lister some more, press the 'Continue' button, if you do not, then press the 'Stop' button")

bot.infinity_polling()