import os
import telebot
import requests
import threading
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer

# 1. إعداد التوكنات وأمان السيرفر
BOT_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')
bot = telebot.TeleBot(BOT_TOKEN)

# كود إرضاء سيرفر Render لتجاوز فحص المنفذ مجاناً
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Firasah Bot is alive!")

def run_health_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()

# التلقين الصارم المعتمد على كتاب علم الفراسة وقواعده الشاملة للوجه
PROMPT_FIRASAH = (
    "أنت الآن خبير بروفيسور متخصص في علم الفراسة وتحليل الشخصية بناءً على ملامح الوجه البدنية بدقة. "
    "ستقوم بتحليل هذه الصورة الشخصية للمستخدم بناءً على أصول علم الفراسة المحددة في الكتاب التعليمي المعتمد لدينا. "
    "قم بفحص الملامح التالية بالترتيب إن ظهرت بوضوح في الصورة: "
    "1. شكل الجبهة (عريضة، ضيقة، مستوية، بارزة) وعلاقتها بالذكاء والتفكير والتخطيط. "
    "2. العيون (واسعة، غائرة، جاحظة، ضيقة، المسافة بينهما) وعلاقتها بالطباع والعاطفة والتركيز. "
    "3. الأنف (طويل، قصير، معقوف، عريض) وعلاقته بالعزة، الطموح، والتعامل المالي. "
    "4. الفم والشفايف (واسع، ضيق، شفة علوية أو سفلية ممتلئة) وعلاقته بالتعبير عن المشاعر والتواصل والخصال الاجتماعية. "
    "5. الحواجب (كثيفة، رقيقة، متصلة، متباعدة، مقوسة) وعلاقتها بالإرادة والاندفاع. "
    "6. شكل وتدويرة الوجه والفك (مربع، دائري، مثلث، بارز) وعلاقته بالصبر، العزيمة، أو العاطفة. "
    "اكتب التقرير النهائي باللغة العربية بأسلوب راقٍ، منظم، وواضح كقراءة فراسة علمية موثوقة ونبيلة، "
    "وقدم نصائح إيجابية للمستخدم لتطوير جوانب شخصيته بناءً على التحليل."
)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "مرحباً بك في بوت مستشار الفراسة التحليلي الخاص! 📸 الحاصل على تدريب مخصص وفقاً لكتاب وقواعد علم الفراسة الأصيلة.\n\n"
        "يرجى إرسال صورة شخصية واضحة للوجه (إضاءة جيدة وملامح بارزة وبدون فلاتر)، وسأقوم بتحليل سمات شخصيتك وطباعك بدقة فوراً."
    )

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    try:
        bot.reply_to(message, "جاري استلام الصورة وفحص الملامح وفقاً لقواعد علم الفراسة... انتظر دقيقة من فضلك 🔍📖")
        
        file_info = bot.get_file(message.photo[-1].file_id)
        file_url = f"https://telegram.org{BOT_TOKEN}/{file_info.file_path}"
        
        img_data = requests.get(file_url).content
        
        gemini_url = f"https://googleapis.com{GEMINI_KEY}"
        
        image_base64 = base64.b64encode(img_data).decode('utf-8')
        
        payload = {
            "contents": [{
                "parts": [
                    {"text": PROMPT_FIRASAH},
                    {
                        "inlineData": {
                            "mimeType": "image/jpeg",
                            "data": image_base64
                        }
                    }
                ]
            }]
        }
        
        res = requests.post(gemini_url, json=payload)
        res_json = res.json()
        
        try:
            report_text = res_json['candidates'][0]['content']['parts'][0]['text']
            bot.reply_to(message, f"📋 **تقرير الفراسة وتحليل الشخصية:**\n\n{report_text}")
        except:
            bot.reply_to(message, "تنبيه: تم استقبال الصورة بنجاح ولكن خادم التحليل يحتاج لإعادة المحاولة. يرجى التأكد من وضوح الصورة وإرسالها مجدداً.")
        
    except Exception as e:
        bot.reply_to(message, "حدث خطأ أثناء الاتصال بخادم التحليل، يرجى المحاولة مرة أخرى لاحقاً.")

if __name__ == "__main__":
    print("بوت الفراسة يعمل الآن...")
    threading.Thread(target=run_health_server, daemon=True).start()
    bot.infinity_polling()
