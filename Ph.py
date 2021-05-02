from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import config
import telegram
from random import randint
TOKEN = config.token




def start(update, context) -> None:
    """Отправляет сообщение в ответ на команду /start."""
    reply_keyboard =["Проверить себя", "Разобраться в теме"]
    update.message.reply_text('Привет! Я помогу тебе разобраться в некоторых облостях физиологии',
                              reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),)
def hand(update, context):
    chat = update.effective_chat
    if update.message.text == "Проверить себя":
        reply_keyboard1 =[['ЭКГ тест'],['Процессы возбуждения тест'],[''],['d']]
        update.message.reply_text('Выбери тему по которой тебе прислать задание',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard1, one_time_keyboard=True))
    if update.message.text == "Разобраться в теме":
        reply_keyboard2 = [['ЭКГ разбор'], ['b'], ['c'], ['d']]
        update.message.reply_text('Выбери тему по которой тебе прислать объяснение',
                                  reply_markup=ReplyKeyboardMarkup(reply_keyboard2, one_time_keyboard=True) )
    if update.message.text == "ЭКГ тест":
        a=0
        #a=randint(0,10)
        reply_keyboard3 = [['зубец P'], ['зубец T'], ['комлекс зубцов QRS'],['сегмент P-Q'],['сегмент S-T']]
        if a==0:
            updater.bot.send_photo(chat_id=chat.id, photo=open('ЭКГкар.jpg', 'rb'))
            update.message.reply_text('Что соотвествует фазам деполяризации и быстрой реполяризациии потенциалов действия в кардиомиоцитах предсердий?',
                                          reply_markup=ReplyKeyboardMarkup(reply_keyboard3, one_time_keyboard=True))
            if update.message.text == "зубец P":
                context.bot.send_message(chat_id=chat.id, text='Правильно!')
            elif update.message.text != "зубец P":
                context.bot.send_message(chat_id=chat.id, text='Ой, кажется ты ошибся. Вот разъяснение')



    #else:
     #   reply_keyboard = [["Проверить себя"], ["Разобраться в теме"]]
      #  update.message.reply_text('Привет! Я помогу тебе разобраться в некоторых облостях физиологии',
       #                       reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True), )







updater = Updater(TOKEN, use_context=True)

dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.all, hand))

updater.start_polling()
updater.idle()
