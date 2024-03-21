import telebot
import os
from gboost_classification import Emo_Classification
API_TOKEN = '6377473904:AAEl0HPD6PglgrImJ3kF8eby-MGJj-6FA5o'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, """\
Привет, пользователь!
Этот бот умеет распознавать эмоции в музыке и классифицировать их по 8 классам:\
усталость, спокойствие, скука, печаль, злость, радость, взволнованность и удовлетворение.\
Для того, чтобы распознать эмоцию отправьте аудио в бот.\
""")

@bot.message_handler(content_types=['audio'])
def handle_audio(message):
    if (message.content_type!='audio'):
        bot.send_message(message.chat.id, 'Данный формат не поддерживается.')
        return
    file_id = message.audio.file_name
    file_id_info = bot.get_file(message.audio.file_id)
    downloaded_file = bot.download_file(file_id_info.file_path)
    file_on_disk = os.getcwd() + '/' + file_id
    with open(file_on_disk, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Аудио получено")
    clf = Emo_Classification()
    emotion_class = clf.recognize_emotion(file_on_disk)
    bot.reply_to(message, "Аудио классифицируется эмоцией: " + emotion_class)

    os.remove(file_on_disk)

if __name__ == "__main__":
    try:
        bot.infinity_polling(none_stop=True)
    except (KeyboardInterrupt, SystemExit):
        pass
