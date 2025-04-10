import telebot
from googletrans import Translator, LANGUAGES

TOKEN = "7914727289:AAGUyJfA3ex2t_MTxrYGIFKqNbGYrDwN_Hs"

bot = telebot.TeleBot(TOKEN)
translator = Translator()

MIN_TEXT_LENGTH = 10
MAX_TEXT_LENGTH = 100

def send_reply(message, text):
    bot.reply_to(message, text)

def validate_text(text):
    if len(text) < MIN_TEXT_LENGTH:
        return f"Текст слишком короткий: {text}"
    elif len(text) > MAX_TEXT_LENGTH:
        return f"Текст слишком длинный: {text}"
    return None

def translate_text(language, text):
    if language not in LANGUAGES:
        return None
    try:
        result = translator.translate(text, dest=language)
        return result.text
    except Exception:
        return None

@bot.message_handler(commands=['start'])
def handle_start(message):
    send_reply(message, "Привет! Я бот-переводчик. Для перевода используй команду /translate <язык> <текст>")

@bot.message_handler(commands=['languages'])
def handle_languages(message):
    languages_str = "\n".join([f"{code}: {name}" for code, name in LANGUAGES.items()])
    send_reply(message, languages_str)

@bot.message_handler(commands=['translate'])
def handle_translate(message):
    args = message.text.split(maxsplit=2)
    if len(args) < 3:
        send_reply(message, "Ошибка: не хватает аргументов для команды.")
        return

    language, text = args[1], args[2]

    error = validate_text(text)
    if error:
        send_reply(message, error)
        return

    translation = translate_text(language, text)
    if translation is None:
        send_reply(message, "Произошла ошибка при переводе.")
    else:
        send_reply(message, f"Перевод на {language}: {translation}")

bot.polling()