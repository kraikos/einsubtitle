from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
import telebot
from io import StringIO
import re

BOT_TOKEN = '7123220842:AAF_gORqLshyJ43B5_J3pl1T59g69-tftaI'    
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Присылай мне ссылки на YouTube (формат: https://youtu.be/...)")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith("https://youtu.be/"):
        try:
            video_id = extract.video_id(message.text)
            
            # Встроенная логика получения субтитров (бывшая get_subs_safe)
            try:
                subs = YouTubeTranscriptApi.get_transcript(
                    video_id,
                    languages=['ru', 'en']
                )
                subs_text = " ".join([item['text'] for item in subs])
                subs_text = re.sub(r'\[.*?\]', '', subs_text)  # Очистка от меток
                
                # Отправка файла
                file_data = StringIO(subs_text)
                file_data.name = f"subs_{video_id}.txt"
                bot.send_document(message.chat.id, file_data)
                
            except Exception as subs_error:
                bot.reply_to(message, f"❌ Не удалось получить субтитры: {str(subs_error)}")
        
        except Exception as e:
            bot.reply_to(message, f"🚫 Ошибка обработки ссылки: {str(e)}")
    else:
        bot.reply_to(message, "Это не YouTube-ссылка в формате https://youtu.be/...")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()




