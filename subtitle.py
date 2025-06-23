from youtube_transcript_api import YouTubeTranscriptApi
from pytube import extract
import telebot
from io import StringIO
import re

BOT_TOKEN = '7123220842:AAF_gORqLshyJ43B5_J3pl1T59g69-tftaI'    

bot = telebot.TeleBot(BOT_TOKEN)

def get_subs_safe(video_id):
    """Безопасное получение субтитров с обработкой ошибок"""
    try:
        subs = YouTubeTranscriptApi.get_transcript(
            video_id,
            languages=['ru', 'en']  # Убрали прокси
        )
        return " ".join([item['text'] for item in subs])
    except Exception as e:
        print(f"Ошибка получения субтитров: {e}")
        return None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Присылай мне ссылки на YouTube (формат: https://youtu.be/...)")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text.startswith("https://youtu.be/"):
        try:
            video_id = extract.video_id(message.text)
            subs = get_subs_safe(video_id)
            
            if subs:
                # Очистка и отправка
                subs = re.sub(r'\[.*?\]', '', subs)
                file_data = StringIO(subs)
                file_data.name = f"subs_{video_id}.txt"
                bot.send_document(message.chat.id, file_data)
            else:
                bot.reply_to(message, "❌ Не удалось получить субтитры (видео приватное или нет русских субтитров)")
        
        except Exception as e:
            bot.reply_to(message, f"🚫 Ошибка обработки: {str(e)}")
    else:
        bot.reply_to(message, "Это не YouTube-ссылка в формате https://youtu.be/...")

if __name__ == "__main__":
    print("Бот запущен...")
    bot.infinity_polling()




