import os
import telebot
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# جلب توكن البوت من متغيرات البيئة بأمان
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

# كود إضافي لفتح منفذ وهمي لإرضاء سيرفر Render ليعمل 24 ساعة
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# أمر البداية /start
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك! أنا بوت تليجرام الخاص بك، أعمل الآن بنجاح وعلى مدار 24 ساعة. 🚀")

# الرد التلقائي على أي رسالة نصية أخرى
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"لقد استلمت رسالتك: {message.text}")

# تشغيل البوت والسيرفر معاً
if __name__ == "__main__":
    print("البوت يعمل الآن...")
    # تشغيل السيرفر الوهمي في الخلفية
    threading.Thread(target=run_health_server, daemon=True).start()
    # تشغيل البوت
    bot.infinity_polling()
