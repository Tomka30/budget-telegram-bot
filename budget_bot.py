import telebot
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

TELEGRAM_TOKEN = 'YOUR_TELEGRAM_TOKEN'
SPREADSHEET_NAME = "Місячний бюджет"

# Авторизація через Railway змінну середовища
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"]

creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1ZoDSqlVy36239CsTWjO0u-tE1OBn9xjn-BLXe-9hq48")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привіт! Надішли мені суму та категорію, наприклад: 250 Продукти")

@bot.message_handler(func=lambda m: True)
def handle_expense(message):
    try:
        text = message.text.strip()
        amount_str, category = text.split(maxsplit=1)
        amount = float(amount_str.replace(",", "."))

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        month_name_ukr = now.strftime("%B %Y")

        try:
            worksheet = sheet.worksheet(month_name_ukr)
        except:
            worksheet = sheet.add_worksheet(title=month_name_ukr, rows="1000", cols="3")
            worksheet.append_row(["Дата", "Сума", "Категорія"])

        worksheet.append_row([date_str, amount, category])
        bot.send_message(message.chat.id, f"✅ Додано: {amount} грн на {category}")
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Помилка: {e}")

bot.polling()
