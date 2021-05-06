import logging
import config
import json
import random
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

CHOOSING, SELECTTEST, LEARNTOPIC, TESTRUNNING, TESTRUNNING2, TESTRUNNING3 = range(6) # это состояния которые могут быть во время тестирования

class Question:
    # класс шаблон для вопросов
    def __init__(self, qid, question, answers, correct, photoRequired, photo, explanation):
        # id вопроса
        self.qid = qid
        # текст вопроса
        self.text = question
        # варианты ответов вопроса
        self.answers = {}
        # правильный ответ вопроса
        self.correct = correct
        # фото вопроса
        self.photo = photo
        # объяснение вопроса
        self.explanation = explanation
        # нужно ли фото вопросу
        self.photoRequired = photoRequired
        for ans in answers:
            ansId = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[len(self.answers)]
            self.answers[ansId] = ans
def loadQuestions(name):
    QUESTIONS = {}
    data = json.load(open("questions.json", "rb"))
    for q in data[name]:
        QUESTIONS.update({
            q['id']: Question(q['id'], q['question_text'], q['answers'], q['correct'], q['photoRequired'], q['photo'],
                              q['explanation'])
        })
    return QUESTIONS

QUESTIONS = loadQuestions('questions_topic_1')
QUESTIONS2 = loadQuestions('questions_topic_2')
QUESTIONS3 = loadQuestions('questions_topic_3')

def start(update, context) -> int:
    reply_keyboard = [['Проверить себя', 'Разобраться в теме']]

    update.message.reply_text(
        'Привет! Я помогу тебе разобраться в некоторых областях физиологии\n'
        'Что ты хочешь сделать',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )

    return CHOOSING

def chooseTopic(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['ЭКГ тест', 'Процессы возбуждения тест', 'Нервная система тест']]

    update.message.reply_text(
        'Выбери тему по которой тебе прислать задание '
        'Отправь /menu чтобы вернуться\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return SELECTTEST


def checkAnswer(update, context, question):
    if update.message.text == question.correct:
        context.bot.send_message(chat_id=update.message.chat.id, text='Правильно!')
    else:
        context.bot.send_message(chat_id=update.message.chat.id, text='Не верно!\nОбъяснение - ')
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(question.explanation[0], 'rb'))
        context.bot.send_photo(chat_id=update.message.chat_id, photo=open(question.explanation[1], 'rb'))


def firstTest(update: Update, context: CallbackContext) -> int:
    try:
        current_question = context.user_data['quiz']['current_question']
        checkAnswer(update, context, current_question)
    except:
        pass

    # в user_data создаем переменную quiz куда будем записывать все данные во время теста
    if 'quiz' not in context.user_data:
        context.user_data['quiz'] = {}
        context.user_data['quiz']['answers'] = {}

    else:
        context.user_data['quiz']['answers'][context.user_data['quiz']['current_qid']] = update.message.text

    # здесь идет вычисление оставшегося кол-ва вопросов в тесте
    questions_left = set(QUESTIONS) - set(context.user_data['quiz']['answers'])

    if len(questions_left) > 0:

        question = QUESTIONS[random.sample(questions_left, 1)[0]]

        if question.photoRequired:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open(question.photo, 'rb'))
            context.bot.send_message(update.message.chat_id, text=f'{question.text}\n' + '\n'.join(
                f'{aid}. {text}' for aid, text in sorted(question.answers.items())),
                                     reply_markup=ReplyKeyboardMarkup([[aid for aid in sorted(question.answers)]]))
        else:
            context.bot.send_message(update.message.chat_id, text=f'{question.text}\n' + '\n'.join(
                f'{aid}. {text}' for aid, text in sorted(question.answers.items())),
                                     reply_markup=ReplyKeyboardMarkup([[aid for aid in sorted(question.answers)]]))
        context.user_data['quiz']['current_qid'] = question.qid
        context.user_data['quiz']['current_question'] = question

        return TESTRUNNING

    else:
        context.bot.send_message(update.message.chat_id, text=f'Тест пройден!', reply_markup=ReplyKeyboardRemove())
        context.user_data['quiz']['current_qid'] = None

        return ConversationHandler.END


def secondTest(update: Update, context: CallbackContext) -> int:
    try:
        current_question = context.user_data['quiz']['current_question']
        checkAnswer(update, context, current_question)
    except:
        pass

    if 'quiz' not in context.user_data:
        context.user_data['quiz'] = {}
        context.user_data['quiz']['answers'] = {}

    else:
        context.user_data['quiz']['answers'][context.user_data['quiz']['current_qid']] = update.message.text

   
    questions_left = set(QUESTIONS2) - set(context.user_data['quiz']['answers'])

    if len(questions_left) > 0:

        question = QUESTIONS2[random.sample(questions_left, 1)[0]]  # тут QUESTIONS изменилось на QUESTIONS1

        if question.photoRequired:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open(question.photo, 'rb'))
            context.bot.send_message(update.message.chat_id, text=f'{question.text}\n' + '\n'.join(
                f'{aid}. {text}' for aid, text in sorted(question.answers.items())),
                                     reply_markup=ReplyKeyboardMarkup([[aid for aid in sorted(question.answers)]]))
        else:
            context.bot.send_message(update.message.chat_id, text=f'{question.text}\n' + '\n'.join(
                f'{aid}. {text}' for aid, text in sorted(question.answers.items())),
                                     reply_markup=ReplyKeyboardMarkup([[aid for aid in sorted(question.answers)]]))
        context.user_data['quiz']['current_qid'] = question.qid
        context.user_data['quiz']['current_question'] = question

        return TESTRUNNING2

    else:
        context.bot.send_message(update.message.chat_id, text=f'Тест пройден!', reply_markup=ReplyKeyboardRemove())
        context.user_data['quiz']['current_qid'] = None

        return ConversationHandler.END
def thirdTest(update: Update, context: CallbackContext) -> int:
    try:
        
        current_question = context.user_data['quiz']['current_question']
        checkAnswer(update, context, current_question)
    except:
        pass

   
    if 'quiz' not in context.user_data:
        context.user_data['quiz'] = {}
        context.user_data['quiz']['answers'] = {}

    else:
        context.user_data['quiz']['answers'][context.user_data['quiz']['current_qid']] = update.message.text

    # здесь идет вычисление оставшегося кол-ва вопросов в тесте
    questions_left = set(QUESTIONS3) - set(context.user_data['quiz']['answers'])

    if len(questions_left) > 0:

        question = QUESTIONS3[random.sample(questions_left, 1)[0]]  # тут QUESTIONS изменилось на QUESTIONS1

        if question.photoRequired:
            context.bot.send_photo(chat_id=update.message.chat_id, photo=open(question.photo, 'rb'))
            context.bot.send_message(update.message.chat_id, text=f'{question.text}\n' + '\n'.join(
                f'{aid}. {text}' for aid, text in sorted(question.answers.items())),
                                     reply_markup=ReplyKeyboardMarkup([[aid for aid in sorted(question.answers)]]))
        else:
            context.bot.send_message(update.message.chat_id, text=f'{question.text}\n' + '\n'.join(
                f'{aid}. {text}' for aid, text in sorted(question.answers.items())),
                                     reply_markup=ReplyKeyboardMarkup([[aid for aid in sorted(question.answers)]]))
        context.user_data['quiz']['current_qid'] = question.qid
        context.user_data['quiz']['current_question'] = question

        return TESTRUNNING3

    else:
        context.bot.send_message(update.message.chat_id, text=f'Тест пройден!', reply_markup=ReplyKeyboardRemove())
        context.user_data['quiz']['current_qid'] = None

        return ConversationHandler.END

def learnTopic(update: Update, context: CallbackContext) -> int:
    reply_keyboard = [['ЭКГ разбор', 'Процессы возбуждения', 'Синапс']]

    update.message.reply_text(
        'Выбери тему по которой тебе прислать объяснение '
        'Отправь /menu чтобы вернуться\n\n',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True),
    )
    return LEARNTOPIC

def showEcg(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Внимательно прочитай')
    context.bot.send_photo(chat_id=chat.id, photo=open('ЭКГоб1.jpg', 'rb'))
    context.bot.send_photo(chat_id=chat.id, photo=open('ЭКГоб2.jpg', 'rb'))
    return ConversationHandler.END
def showVozh(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Тут подробно написано объяснение')
    context.bot.send_photo(chat_id=chat.id, photo=open('ВозбОб1.jpg', 'rb'))
    context.bot.send_photo(chat_id=chat.id, photo=open('ВозбОб2.jpg', 'rb'))
    return ConversationHandler.END
def showSynapse(update: Update, context: CallbackContext) -> int:
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Тут подробно написано объяснение')
    context.bot.send_photo(chat_id=chat.id, photo=open('СинапсОб.jpg', 'rb'))
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
                MessageHandler(Filters.regex('^(ЭКГ тест)$'), firstTest),  # обработчик входа в 1 тест
                MessageHandler(Filters.regex('^(Процессы возбуждения тест)$'), secondTest),
                # обработчик входа во 2 тест
                MessageHandler(Filters.regex('^(Нервная система тест)$'), thirdTest),
            ],
            TESTRUNNING: [
                MessageHandler(None, firstTest),  # обработчик первого теста
            ],
            TESTRUNNING2: [
                MessageHandler(None, secondTest),  # обработчик второго теста
            ],
            TESTRUNNING3: [
                MessageHandler(None, thirdTest),  # обработчик третьего теста
            ],
            LEARNTOPIC: [
                MessageHandler(Filters.regex('^(ЭКГ разбор)$'), showEcg),
                MessageHandler(Filters.regex('^(Процессы возбуждения)$'), showVozh),
                MessageHandler(Filters.regex('^(Синапс)$'), showSynapse),
            ]
        },
        fallbacks=[CommandHandler('menu', start)],
    )
    dispatcher.add_handler(convHandler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
