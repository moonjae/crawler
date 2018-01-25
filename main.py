from bs4 import BeautifulSoup
import requests
from utils import get_top100_list

# source = requests.get('https://www.melon.com/chart/index.htm')
# soup = BeautifulSoup(source.text, 'lxml')
#
# list = []
#
#
# for tr in soup.find_all('tr', class_ ='lst50'):
#     title = tr.find('div', class_='rank01').find('a').text
#     artist = tr.find('div', class_='rank02').find('a').text
#     rank = tr.find('span', class_='rank').text
#     album = tr.find('div', class_='rank03').find('a').text
#
#     list.append({
#      'title' : title, 'artist' : artist, 'rank' : rank , 'album': album
#     })
#
#
#
#
# print(list)
get_top100_list()





