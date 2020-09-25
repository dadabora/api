# https://stavropol.hh.ru/vacancies/podrabotka?L_is_autosearch=false&clusters=true&enable_snippets=true&is_part_time_clusters_enabled=true&text=Data&page=0
# https://www.superjob.ru/vacancy/search/?keywords=data&noGeo=1
from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient
import numpy as np
import pandas as pd
nambe = 0
vacancy_list_hh = []
page = 0
while True:

    main_link_hh = 'https://stavropol.hh.ru'
    params = {'L_is_autosearch': 'false',
              'clusters': 'true',
              'enable_snippets': 'true',
              'items_on_page' : 20,
              'text': 'Data science',
              'page': {page}
              }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    html = requests.get(main_link_hh + '/vacancies/podrabotka', params=params, headers=headers)

    soup = bs(html.text, 'html.parser')

    vacancies_block = soup.find('div', {'class': 'vacancy-serp'})
    vacancies_list = vacancies_block.find_all('div', {'class': 'vacancy-serp-item'})

    p = soup.find('div', {'data-qa':'pager-block'}).text

    p = (re.search(r'дальше', p))
# подготовка данных для записи
    for i in vacancies_list:
        vacancy_name = i.find('a').text
        vacancy_info = i.find('a')['href']
        vacancy_info_z1 = i.find('div', {'class':"vacancy-serp-item__sidebar"}).getText()
        vacancy_info_z = [vacancy_info_z1.replace('\xa0', '')]
        match1=[]
        if vacancy_info_z[0] != '':
            for a in re.split(r'-', vacancy_info_z[0]):
                m = [el for el in re.findall(r'\d+', a)]
                match1.append(m[0])
            currency = vacancy_info_z1.split()[-1]
        else:
            currency = ''
        min_c = None
        max_c = None
        if vacancy_info_z1.startswith('от'):
            min_c = int(match1[0])
            max_c = None
        elif vacancy_info_z1.startswith('до'):
            min_c = None
            max_c = int(match1[0])
        elif ('-') in vacancy_info_z1:
            min_c = int(match1[0])
            max_c = int(match1[1])
# Заполнение словаря и запись в список.
        vacancy_dict = {}
        vacancy_dict['name'] = vacancy_name
        vacancy_dict['link'] = vacancy_info
        vacancy_dict['min'] = min_c
        vacancy_dict['max'] = max_c
        vacancy_dict['currency'] = currency
        vacancy_list_hh.append(vacancy_dict)
        nambe += 1
       #pprint(vacancy_dict)

    if p != None and p[0] == 'дальше':
        page += 1
        print(page, end='\r')

    else:
        break
print(nambe)
#pprint(vacancy_list_hh)


vacancy_list_sj = []
nambe = 0
page = 0
while True:

    main_link_sj = 'https://www.superjob.ru'
    params = {'keywords': 'Data',
              'noGeo': 1,
              'page': {page}
              }

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36'}
    html = requests.get(main_link_sj + '/vacancy/search/', params=params, headers=headers)

    soup = bs(html.text, 'html.parser')

    vacancies_block = soup.find('div', {'class': '_1Ttd8 _2CsQi'})

    vacancies_list = vacancies_block.find_all('div', {'class': 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'})
    #pprint(vacancies_list)
    p = soup.find('div', {'class':'_3zucV L1p51 undefined _1Fty7 _2tD21 _3SGgo'}).text
    p = (re.search(r'\d+', p))


    for i in vacancies_list:
       # pprint(i)
        vacancy_info = (main_link_sj + i.find('a')['href'])
        #print(vacancy_info)
        vacancy_name = i.find('a').text
        #print(vacancy_name)


        vacancy_info_z1 = i.find('span', {'class':'_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()
        #print(vacancy_info_z1)
        min_c = ''
        max_c = ''
        currency = ''
        match1=[]
# Подготовка цифр для записи
        if vacancy_info_z1 != 'По договорённости':
            currency = vacancy_info_z1.split()[-1]
            vacancy_info_z = [vacancy_info_z1.replace('\xa0', '')]
            for a in re.split(r'—', vacancy_info_z[0]):
                m = [el for el in re.findall(r'\d+', a)]
                match1.append(m[0])
                #print(match1)
        else:
            min_c = None
            max_c = None
        if vacancy_info_z1.startswith('от'):
            min_c = int(match1[0])
            max_c = None
        elif vacancy_info_z1.startswith('до'):
            min_c = None
            max_c = int(match1[0])
        elif ('—') in vacancy_info_z1:
            min_c = int(match1[0])
            max_c = int(match1[1])
# Заполнение словаря и списка вакансий
        vacancy_dict = {}
        vacancy_dict['name'] = vacancy_name
        vacancy_dict['link'] = vacancy_info
        vacancy_dict['min'] = min_c
        vacancy_dict['max'] = max_c
        vacancy_dict['currency'] = currency
        vacancy_list_sj.append(vacancy_dict)
        nambe += 1
        #pprint(vacancy_dict)

    if page < len(p[0])-1 :
        page += 1
    else:
        break

# количество выбранных записей
print(nambe)

client = MongoClient('127.0.0.1', 27017)
db = client['vacancy_db']
sj = db.sj
hh = db.hh
# заполнение базы обновленными данными
def filter(vacancy_list_sj, vacancy_list_hh):
    for v in vacancy_list_sj:
        sj.update({'link': v['link']},
                  {'$set': {'name': v['name'],
                            'link': v['link'],
                            'min': v['min'],
                            'max': v['max'],
                            'currency': v['currency']}},True)
    for v in vacancy_list_hh:
        hh.update({'link': v['link']},
                  {'$set': {'name': v['name'],
                            'link': v['link'],
                            'min': v['min'],
                            'max': v['max'],
                            'currency': v['currency']}}, True)

# сортировка по минимальному значению
def vacancy_min(min_salary):
    for corrent in sj.find({'$or': [{'min': {'$gt': min_salary}},{'max':{'$gt':min_salary}}]}):
        pprint(corrent)
    for corrent in hh.find({'$or': [{'min': {'$gt': min_salary}},{'max': {'$gt': min_salary}}]}):
        pprint(corrent)

filter(vacancy_list_sj, vacancy_list_hh)

min_salary = 100000
vacancy_min(min_salary)
