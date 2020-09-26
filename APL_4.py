from pprint import pprint
from lxml import html
import requests

header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 YaBrowser/20.8.3.115 Yowser/2.5 Safari/537.36'}
main_link_mail = 'https://news.mail.ru/'
main_link_lenta = 'https://lenta.ru'
main_link_yandex = 'https://yandex.ru/news/'

print('майл новости')
response_m = requests.get(main_link_mail,headers=header)
dom = html.fromstring(response_m.text)

goods = dom.xpath("//ul[@data-module='TrackBlocks']")

news_m =[]
for good in goods:

    news_href = good.xpath(".//a[@class]/@href")
    name_news = good.xpath(".//a[@class]/text()")

    a = 0
    for pr in name_news:
        news = {}
        pr = [pr.replace('\xa0',' ')]
        news['name_news'] = pr
        response = requests.get(news_href[a], headers=header)
        dom2 = html.fromstring(response.text)
        news_time = dom2.xpath("//span[@datetime]/@datetime")
        news['news_time'] = news_time
        news['news_href'] = news_href[a]
        name_sourse = dom2.xpath("//span[@class='note']/*/span/text()")
        news['name_sourse'] = name_sourse
        news_m.append(news)
        a += 1
pprint(news_m)


print('лента новости')
response_l = requests.get(main_link_lenta,headers=header)
dom = html.fromstring(response_l.text)

goods = dom.xpath("//section[contains(@class,'b-top7-for-main')]")

news_l =[]
for good in goods:

    name_sourse = 'lenta'
    news_time = good.xpath(".//time[@datetime]/@datetime")
    news_href = good.xpath(".//time[@datetime]/../@href")
    name_news = good.xpath(".//time[@datetime]/../text()")
    a = 0
    for pr in name_news:
        news = {}
        pr = [pr.replace('\xa0',' ')]
        news['name_news'] = pr
        news['news_time'] = news_time[a]
        news['news_href'] = main_link_lenta + news_href[a]
        news['name_sourse'] = name_sourse
        news_l.append(news)
        a += 1
pprint(news_l)

print('яндекс новости')
response_y = requests.get(main_link_yandex,headers=header)
dom = html.fromstring(response_y.text)

goods = dom.xpath("//div[@class='mg-grid__row mg-grid__row_gap_8 news-top-stories news-app__top']")

news_y =[]
for good in goods:

    name_sourse = good.xpath(".//span[@class='mg-card-source__source']/a/text()")
    news_time = good.xpath(".//span[@class='mg-card-source__time']/text()")
    news_href = good.xpath(".//span[@class='mg-card-source__source']/a/@href")
    name_news = good.xpath(".//div[@class='news-card__inner']/a/h2/text()|.//div[@class='mg-grid__col mg-grid__col_xs_4']/article/a/h2/text()")

    a = 0
    for pr in name_news:
        news = {}
        pr = [pr.replace('\xa0',' ')]
        news['name_news'] = pr
        news['news_time'] = news_time[a]
        news['news_href'] = news_href[a]
        news['name_sourse'] = name_sourse[a]
        news_y.append(news)
        a += 1

pprint(news_y)