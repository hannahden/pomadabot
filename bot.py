import telebot

from nlp_utils import get_item_for_search
from utils import krisa, by_popular, by_rating, generate_irec_markup, get_answer_from_top, Buffer
from parser import get_parsed_list, get_top_5
from config import token

bot = telebot.TeleBot(token, parse_mode=None)

user_dict = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.send_message(message.chat.id, 'Привет, я помогаю найти варианты разных вещей по отзывам на Irecommend. Напиши, что ты хочешь, и я попробую помочь тебе.'+ krisa)

@bot.message_handler(func=lambda message: message.text == by_popular and user_dict)
def echo_search_by_popular(message):
	chat_id = message.chat.id

	item = user_dict[chat_id]
	to_find = item.saved
	result_list = get_parsed_list(to_find)
	top_results = get_top_5(result_list, 'feedback')

	answer = get_answer_from_top(top_results)


	bot.send_message(message.chat.id, answer, parse_mode='MarkdownV2')

@bot.message_handler(func=lambda message: message.text == by_rating and user_dict)
def echo_search_by_rating(message):
	chat_id = message.chat.id

	item = user_dict[chat_id]
	to_find = item.saved
	result_list = get_parsed_list(to_find)
	top_results = get_top_5(result_list, 'rating')

	answer = get_answer_from_top(top_results)

	bot.send_message(message.chat.id, answer, parse_mode='MarkdownV2')

@bot.message_handler(func=lambda message: True)
def echo_get_intention(message):
	wish = get_item_for_search(message.text)

	if 'fail' not in wish:
		chat_id = message.chat.id

		markup = generate_irec_markup()

		user = Buffer(wish)

		user_dict[chat_id] = user

		bot.send_message(message.chat.id, 'Выбери способ подбора:', reply_markup=markup)
	else:
		negative = ''.join(['Много хочешь ', u'\U0001F5FF', '\n', 'Попробуй написать по-другому.'])
		bot.reply_to(message, negative)





bot.polling()