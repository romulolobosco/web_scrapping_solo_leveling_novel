import os
import re

from bs4 import BeautifulSoup
from requests_html import HTMLSession

session = HTMLSession()
url = 'https://boxnovel.com/novel/i-alone-level-up/chapter-1'

def request_content(url):
    ret = session.get(url).html.raw_html
    return BeautifulSoup(ret)

def getChapterContent(soap):
    main_content = soap.find('div',class_='text-left')
    chapter_text = main_content.find(re.compile('h[1-5]')).text
    for i in main_content.find_all('p'):
        chapter_text += f"{i.text}\n\n"
        
    return chapter_text

while True:
    soap = request_content(url).find('div', class_='main-col')
    try:
        next_page_url = soap.find('a', class_='next_page')['href']
    except TypeError:
        next_page_url = False
    with open('solo_leveling.txt','a+') as f:
        f.write(getChapterContent(soap))
    if next_page_url:
        print('has_next')
        url = next_page_url
    else:
        print('last one')
        break