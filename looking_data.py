import json

# with open('stock_data.json') as file:
#     data = json.load(file)
#     last_2_days = (list(data['Time Series (Daily)'].items())[:2])
#     close_price = [float(i[1]['4. close']) for i in last_2_days]
#     delta = max(close_price) - min(close_price)
#     alert = close_price[0] /100 * 5
# from datetime import datetime, timedelta
# if datetime.now().weekday() < 5:
#     print(datetime.now().date() - timedelta(days=2))
# else:
#     print(datetime.now().date() - timedelta(days=3))
# with open('news.json') as file:
#     data = json.load(file)
#     most_relevant = data['articles'][:3]
#     most_relevant_dict = {}
#     for i in range(len(most_relevant)):
#         most_relevant_dict[i] = {
#             'source': most_relevant[i]['source']['name'],
#             'title': most_relevant[i]['title'],
#             'brief': most_relevant[i]['description'],
#             'url': most_relevant[i]['url'],
#         }
#         print(most_relevant_dict)