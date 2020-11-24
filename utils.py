from telebot import types

by_popular = ''.join(['По популярности',u'\U00002728'])
by_rating = ''.join(['По качеству',u'\U0001F495'])

square = u'\U000025AA'
krisa = u'\U0001F42D'
class Buffer:
	def __init__(self, saved):
		self.saved = saved

def generate_irec_markup():
	markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

	choises = [by_popular, by_rating]
	for c in choises:
		markup.add(c)

	return markup

def prettify_rating(mark):
    string=str(mark)
    if len(string)==1:
        return string
    else:
        return string[0]+'\\' +string[1:]

def prettify_name(name):
    new_name = name.replace('_', '\\_') \
                   .replace('*', '\\*') \
                   .replace('[', '\\[') \
                   .replace(']', '\\]') \
                   .replace('(', '\\(') \
                   .replace(')', '\\)') \
                   .replace('-', '\\-') \
                   .replace('|', '\\|') \
                   .replace('.', '\\.') \
                   .replace('!', '\\!') \
                   .replace('`', '\\`') \
                   .replace('~', '\\~') \
                   .replace('>', '\\>') \
                   .replace('#', '\\#') \
                   .replace('+', '\\+') \
                   .replace('=', '\\=') \
                   .replace('{', '\\{') \
                   .replace('}', '\\}') 


    return new_name

def get_answer_from_top(top):
    start = 'Вот что я нашел\: \n \n'
    irec_str = 'https://irecommend\.ru'
    hyperlink_template = ' [тык]({})'
    
    for item in top:
        start += ''.join([prettify_name(item[0]), '\:', hyperlink_template.format(irec_str+item[1]), '\n'])
        start += ''.join([square, ' ', 'Отзывов\: {}\n'.format(item[2]), square, ' ', 'Средняя оценка\: {}\n \n'.format(prettify_rating(item[3]))])
        
    start += 'Обращайся\!' + krisa
    return start

