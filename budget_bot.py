import telebot
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

TELEGRAM_TOKEN = '7939857891:AAE5vSDJTnrnCFopFEHq1vRXsHF843m6slc'
SPREADSHEET_NAME = 'Месячный бюджет'

# === 2. Авторизація з credentials.json ===
import os
import json

scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Зчитуємо ключ із змінної середовища
creds_json = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS_JSON")
creds_dict = json.loads(creds_json)

# Авторизуємося через словник
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1ZoDSqlVy36239CsTWj0Ou-te1OBn9xjn-BLXe-9hq48")

# === 3. Старт бота ===
bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, "Привіт! Надішли мені суму та категорію, наприклад:\n\n200 Їжа")

@bot.message_handler(func=lambda m: True)
def handle_expense(message):
    try:
        text = message.text.strip()
        amount_str, category = text.split(maxsplit=1)
        amount = float(amount_str.replace(",", "."))

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        month_name_ukr = "червень2025"

        try:
            worksheet = sheet.worksheet(month_name_ukr)
        except:
            worksheet = sheet.add_worksheet(title=month_name_ukr, rows=1000, cols=3)
            worksheet.append_row(["Дата", "Сума", "Категорія"])

        worksheet.append_row([date_str, amount, category])
        bot.send_message(message.chat.id, f"Додано: {amount} грн на \"{category}\"")
    except Exception as e:
        bot.send_message(message.chat.id, f"Помилка: {e}\nФормат: 200 Їжа")

# === 4. Запускаємо бота ===
print("Бот запущено...")
bot.polling()