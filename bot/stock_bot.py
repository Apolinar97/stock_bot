from os import getcwdb
from os.path import join
from urllib.parse import quote
from marshmallow import schema
import tweepy
import stock_data
from datetime import datetime
import pickle
from jinja2 import Environment, FileSystemLoader
import os
import time
import schedule
from image_util import screenshot_element

consumer_key = ''
consumer_secret = ''

auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token('', '')
api = tweepy.API(auth)

stock_schema = stock_data.StockSchema(many=True)

def set_stocks():
    try:
        trending_symbols = stock_data.trending_stocks()
        stock_meta_data = stock_data.quotes(stocks=trending_symbols)
        return stock_meta_data
    except:
        print('In execpt')

# #testing purpose saved stocks object
# with open('stocks.pickle','rb') as input_file:
#     stocks = pickle.load(input_file)


#TODO: Might change so I only safe PNG files, and render HTML from disc mem
def safe_html_file(html):
    file_name = f'trending_stocks_{datetime.now().microsecond}.html'
    file_path = os.path.join('C:\\Users\\Apolinar\\stock_bot\\bot\\html_files',file_name)
    
    if not os.path.isfile(file_path):
        with open(file_path,'w') as f:
            f.write(html)
            return file_path


def generate_html(stocks):
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('table.html')
    return template.render(stocks=stocks)

def print_stocks(stocks):
    for key in stocks:
        print(key,stocks[key].o)

def make_post():
    stocks = set_stocks()
    html = generate_html(stocks=stocks)
    print_stocks(stocks)
    png_path = screenshot_element(safe_html_file(html))
    stock_tickers = ''
    for ticker in stocks:
        stock_tickers = stock_tickers + f'''${ticker} '''
    message = f'Trending stocks as of {datetime.now()}\n' + stock_tickers
    api.update_with_media(png_path,message)


schedule.every(1).hour.do(make_post)

make_post()

while True:
    if(datetime.now().hour > 13):
        break
    
    schedule.run_pending()
    time.sleep(1)









#pickle to save api calls
# stocks = set_stocks()

# with open('stocks.pickle','wb') as output_file:
#     pickle.dump(stocks,output_file)




