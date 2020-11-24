from operator import itemgetter

import requests
from bs4 import BeautifulSoup

def get_names(soup):
    names_list = soup.find_all('div', {'class': 'title'})
    names = [name.text for name in names_list]
    
    return names[:-1]

def get_links(soup):
    links_list = soup.find_all('a', {'class': 'read-all-reviews-link-bottom'})
    links = [link['href'] for link in links_list]
    
    return links

def get_feedbacks(soup):
    feedback_list = soup.find_all('span', {'class': 'counter'})
    feedbacks = [int(fb.get_text()) for fb in feedback_list][::2]
    
    return feedbacks

def get_rating(soup):
    rating_list = soup.find_all('span', {'class': 'average-rating'})
    rating = [float(r.get_text()[9:-1]) for r in rating_list]
    
    return rating
    
def get_parsed_list(str_list):
    joined = '%20'.join(str_list)
    
    vgm_url = ''.join(['https://irecommend.ru/srch?query=', joined]) 
    html_text = requests.get(vgm_url).text
    soup = BeautifulSoup(html_text, 'html.parser')
    
    names = get_names(soup)
    links = get_links(soup)
    feedbacks = get_feedbacks(soup)
    rating = get_rating(soup)
    
    res_list = [x for x in zip(names, links, feedbacks, rating)]
    
    return res_list

def get_top_5(res_list, how):
    if how == 'rating':
        ind = 3
    elif how == 'feedback':
        ind = 2
        
    res = sorted(res_list, key=itemgetter(ind), reverse=True)
    
    return res[:4]