from copy import Error
import json
from typing import Mapping
import requests
from marshmallow import Schema, fields, post_load, EXCLUDE, schema
from requests import exceptions

from requests.api import get
fin_hub_api_key = ''
fin_hub_base_url = 'https://finnhub.io/api/v1/'
class StockModel:
    def __init__(self,symbol=None, watchlist_count=None):
        self.symbol = symbol
        self.watchlist_count = watchlist_count

class QuoteModel:
    def __init__(self, o=None, c=None, pc=None):
        self.o= o
        self.c = c
        self.pc = pc

class StockSchema(Schema):
    symbol = fields.Str()
    watchlist_count = fields.Int()
    
    class Meta:
        unknown = EXCLUDE

    @post_load
    def make_stock(self,data,**kwargs):
        return StockModel(**data)

class QuoteSchema(Schema):
    o = fields.Float()
    c = fields.Float()
    pc = fields.Float()

    class Meta:
        unknown = EXCLUDE
    
    @post_load
    def make_quotes(self,data,**kwargs):
        return QuoteModel(**data)
#url = base_url + f'quote?symbol={ticker}&token={api_key}'
def trending_stocks():
    try:
        stock_schema = StockSchema(many=True)
        response = requests.get('https://api.stocktwits.com/api/2/trending/symbols/equities.json')
        return stock_schema.load(response.json()['symbols'])
    
    except requests.exceptions as e:
        raise(e)

def quote(ticker):
    try:
        url = fin_hub_base_url + f'quote?symbol={ticker}&token={fin_hub_api_key}'
        return requests.get(url).json()

    except requests.exceptions as e:
        raise(e)

#TODO Can possibly switch out to map function
def quotes(stocks):
    stock_dict = {}
    quote_schema = QuoteSchema()
    for stock in stocks:
       stock_dict[stock.symbol] = quote_schema.load(quote(stock.symbol))
    
    return stock_dict


