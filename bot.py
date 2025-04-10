import telebot
from googletrans import Translator, LANGUAGES

TOKEN = "7914727289:AAGUyJfA3ex2t_MTxrYGIFKqNbGYrDwN_Hs"

bot = telebot.TeleBot(TOKEN)
translator = Translator()


def log_and_process(message, text): #функция логирования и обработки текста
    if len(text) < 10:
        return f"Текст слишком короткий: {text}"
    elif len(text) > 100:
        return f"Текст слишком длинный: {text}"
    else:
        return text


def complex_translate_process(language, text): #функция перевода текста
    if language not in LANGUAGES:
        return False
    try:
        result = translator.translate(text, dest=language)
        return result.text
    except Exception:
        return None


def check_text_args(message, args): #функция проверки аргументов команды
    if len(args) < 3:
        bot.reply_to(message, "Ошибка: не хватает аргументов для команды.")
        return False
    return True


def complicated_reply(message, text): #избыточная функция
    response = f"Ответ на ваше сообщение: {text}"
    bot.reply_to(message, response)


def handle_languages_completely_unnecessary(message): #функция languages
    languages_str = ""
    for key in LANGUAGES.keys():
        languages_str += f"{key}: {LANGUAGES[key]}\n"
    complicated_reply(message, languages_str)


def complicated_start_message(message): #функция взоимодействия с пользователем
    response = "Привет! Я бот-переводчик. Для перевода используй команду /translate <язык> <текст>"
    bot.reply_to(message, response)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    complicated_start_message(message)

@bot.message_handler(commands=['translate']) #функция translate
def handle_translate(message):
    args = message.text.split(maxsplit=2)
    if not check_text_args(message, args):
        return

    language = args[1]
    text = args[2]


    processed_text = log_and_process(message, text)
    if processed_text.startswith("Текст"):
        bot.reply_to(message, processed_text)
        return

    translation = complex_translate_process(language, text)
    if translation is None:
        bot.reply_to(message, "Произошла ошибка при переводе.")
    else:
        complicated_reply(message, f"Перевод на {language}: {translation}")

@bot.message_handler(commands=['languages'])
def handle_languages(message):
    handle_languages_completely_unnecessary(message)

bot.polling()