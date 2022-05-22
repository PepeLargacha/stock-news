import json
import os
import requests
from datetime import datetime, timedelta
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_KEY = os.environ.get('###') # You have to save the Key in the env
NEWSAPI_KEY = os.environ.get('###') # You have to save the Key in the env

acc_sid = #Your sid
TWILIO_AUTH = os.environ.get('###') # You have to save the Auth in the env
twilio_phone = # Your Twilio phone
phone = #Authorized phone on Twilio


def get_from_day():
    if datetime.now().weekday() < 5:
        from_day = datetime.now().date() - timedelta(days=2)
    else:
        from_day = datetime.now().date() - timedelta(days=3)
    return from_day


def get_stocks_variation(stock):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&outputsize=compact' \
          f'&apikey={ALPHA_KEY}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    with open('stock_data.json', mode='w') as file:
        info = json.dumps(data)
        file.write(info)
    last_2_days = (list(data['Time Series (Daily)'].items())[:2])
    close_price = [float(i[1]['4. close']) for i in last_2_days]
    return close_price


def get_news(company_name):
    url = f'https://newsapi.org/v2/everything?q={company_name}&from={get_from_day()}&apiKey={NEWSAPI_KEY}'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    with open('news.json', mode='w') as file:
        info = json.dumps(data)
        file.write(info)
    most_relevant = data['articles'][:3]
    most_relevant_dict = {}
    for i in range(len(most_relevant)):
        most_relevant_dict[i] = {
            'source': most_relevant[i]['source']['name'],
            'title': most_relevant[i]['title'],
            'brief': most_relevant[i]['description'],
            'url': most_relevant[i]['url'],
        }
    return most_relevant_dict


def send_msg(phone, body):
    client = Client(acc_sid, TWILIO_AUTH)
    message = client.messages.create(
                                  body=f'{body}',
                                  from_=twilio_phone,
                                  to=f'{phone}'
                              )
    print(message.status)


def price_alert(stock, company_name, phone):
    last_2_closes = get_stocks_variation(stock)
    delta = last_2_closes[1] - last_2_closes[0]
    alert = last_2_closes[0] / 100 * 5

    if abs(delta) > alert:
        news = get_news(company_name)
        percentage = delta / last_2_closes[0] * 100
        body = f"{STOCK}: {'📈' if delta > 0 else '📉'} {percentage:.2f}%\n" \
               f"Headline: {news[0]['title']}\n" \
               f"Brief: {news[0]['brief']:<200}\n" \
               f"Url: {news[0]['url']}"
        send_msg(phone, body)


price_alert(STOCK, COMPANY_NAME, phone)

