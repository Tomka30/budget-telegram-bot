
import telebot
import os
import datetime
import gspread
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import json

# Авторизація Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
google_creds_json = os.environ["GOOGLE_CREDENTIALS"]
google_creds = json.loads(google_creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(google_creds, scope)
client = gspread.authorize(creds)

# Telegram токен
bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])

# Назва Google таблиці
SPREADSHEET_NAME = "Месячный бюджет"

def get_or_create_month_sheet():
    now = datetime.datetime.now()
    month_name = now.strftime("%B_%Y")  # Наприклад: June_2025
    try:
        sheet = client.open(SPREADSHEET_NAME).worksheet(month_name)
    except gspread.exceptions.WorksheetNotFound:
        sheet = client.open(SPREADSHEET_NAME).add_worksheet(title=month_name, rows="1000", cols="4")
        sheet.append_row(["Дата", "Сума", "Опис", "Категорія"])
    return sheet

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Введи витрату у форматі: `Сума Опис Категорія`\nНаприклад: `200 таксі Транспорт`")

@bot.message_handler(func=lambda m: True)
def add_expense(message):
    try:
        parts = message.text.strip().split()
        amount = float(parts[0])
        description = parts[1]
        category = " ".join(parts[2:])
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        sheet = get_or_create_month_sheet()
        sheet.append_row([date, amount, description, category])
        bot.send_message(message.chat.id, f"✅ Додано: {amount} грн — {description} ({category})")
    except Exception as e:
        bot.send_message(message.chat.id, f"⚠️ Помилка: {e}")

bot.polling(none_stop=True)
