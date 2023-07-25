from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
import time

options = Options()
options.add_argument("--headless")

from fake_useragent import UserAgent
ua = UserAgent()
#a = ua.random
user_agent = ua.random
#print(user_agent)
options.add_argument(f'user-agent={user_agent}')

links = ['https://realty.ya.ru/offer/3024777034263824572/', 'https://realty.ya.ru/offer/3024777034263823422/']
listings = []

driver = webdriver.Firefox(options=options)

for link in links:
    driver.get('view-source:'+link)
    page_source = driver.page_source
    data = eval(re.findall('<span>window\.INITIAL_STATE = .{1,}};</span><span>&lt;', page_source)[0].replace('<span>window.INITIAL_STATE = ', '').replace(';</span><span>&lt;', '').replace('null', 'None').replace('true', 'True').replace('false', 'False'))
    info = data['offerCard']['card']
    listing = {}
    listing['ID'] = info['offerId']
    listing['Ссылка'] = link
    listing['Цена'] = info['price']['value']
    listing['Период аренды'] = info['price']['period']
    listing['Валюта'] = info['price']['currency']
    listing['Площадь'] = info['area']['value']
    listing['Ед. изм. цена'] = info['price']['unitPerPart']
    listing['Ед. изм. площадь'] = info['area']['unit']
    listing['Широта'] = info['location']['point']['latitude']
    listing['Долгота'] = info['location']['point']['longitude']
    listing['Адрес'] = info['location']['streetAddress']
    listing['Этаж'] = info['floorsOffered']
    listing['Время до метро'] = info['location']['metro']['timeToMetro']
    listing['Ссылки на фото'] = [x[2:] for x in info['mainImages']]
    listing['Дата публикации'] = info['creationDate'].split('T')[0]
    listing['Дата обновления'] = info['updateDate'].split('T')[0]
    listing['Текст'] = info['description']
    listing['Агент'] = info['author']['organization']
    listing['Тип агента'] = info['author']['category']
    """
    building = info['commercialInfo']['commercialBuilding']
    listing['Тип здания'] = building['buildingType']
    listing['Класс'] = building['buildingClass']
    listing['Этажей в здании'] = building['numberOfFloors']
    listing['Год постройки'] = building['yearConstruct']
    """
    listings.append(listing)

driver.quit()