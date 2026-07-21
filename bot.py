import os
import telebot

# جلب توكن البوت من متغيرات البيئة بأمان
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# أمر البداية /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت تليجرام الخاص بك، أعمل الآن بنجاح وعلى مدار 24 ساعة. 🚀")

# الرد التلقائي على أي رسالة نصية أخرى
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"لقد استلمت رسالتك: {message.text}")

# تشغيل البوت بشكل مستمر
if __name__ == "__main__":
    print("البوت يعمل الآن...")
    bot.infinity_polling()
