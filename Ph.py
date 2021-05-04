import logging
import config
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
TOKEN = config.token
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CHOOSING, SELECTTEST, LEARNTOPIC, CHECKANSWER = range(4)

def start(update, context) -> int:
    reply_keyboard = [['Проверить себя', 'Разобраться в теме']]

    update.message.reply_text(
        'Привет! Я помогу тебе разобраться в некоторых областях физиологии\n'
        'Что ты хочешь сделать',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CHOOSING

def chooseTopic(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['ЭКГ тест', 'Процессы возбуждения тест']]

    update.message.reply_text(
        'Выбери тему по которой тебе прислать задание '
        'Отправь /menu чтобы вернуться\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return SELECTTEST

def testProcess(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    reply_keyboard = [['зубец P', 'зубец T', 'комлекс зубцов QRS', 'сегмент P-Q', 'сегмент S-T']]
    context.bot.send_photo(chat_id=chat.id, photo=open('ЭКГкар.jpg', 'rb'))
    update.message.reply_text(
        'Что соотвествует фазам деполяризации и быстрой реполяризациии потенциалов действия в кардиомиоцитах предсердий?'
        'Отправь /menu чтобы вернуться\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CHECKANSWER

def checkCorrect(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Правильно!')
    return ConversationHandler.END

def checkIncorrect(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Ой, кажется ты ошибся. Вот разъяснение!')
    context.bot.send_photo(chat_id=chat.id, photo=open('ЭКГоб1.jpg', 'rb'))
    context.bot.send_photo(chat_id=chat.id, photo=open('ЭКГоб2.jpg', 'rb'))
    return ConversationHandler.END

def learnTopic(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['ЭКГ разбор', 'a', 'b', 'c']]

    update.message.reply_text(
        'Выбери тему по которой тебе прислать объяснение '
        'Отправь /menu чтобы вернуться\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return LEARNTOPIC

def showEcg(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Что-то тут написано')
    return ConversationHandler.END

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    convHandler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CHOOSING: [
                MessageHandler(Filters.regex('^(Проверить себя)$'), chooseTopic),
                MessageHandler(Filters.regex('^(Разобраться в теме)$'), learnTopic),
            ],
            SELECTTEST: [
                MessageHandler(Filters.regex('^(ЭКГ тест)$'), testProcess),
            ],
            LEARNTOPIC: [
                MessageHandler(Filters.regex('^(ЭКГ разбор)$'), showEcg),
            ],
            CHECKANSWER:[
                MessageHandler(Filters.regex('^(зубец P)$'), checkCorrect),
                MessageHandler(Filters.regex('^\w+'), checkIncorrect),
            ]
        },
        fallbacks=[CommandHandler('menu', start)],
    )
    dispatcher.add_handler(convHandler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
