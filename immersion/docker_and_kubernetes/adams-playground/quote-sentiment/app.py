import typing

import requests

from bs4 import BeautifulSoup
from flask import Flask, jsonify
from google.cloud import language_v1
from pydantic import BaseModel


app = Flask(__name__)


class Quote(BaseModel):
    text : str
    author : str
    tags : typing.Sequence[str]
    sentiment : typing.Optional[float]
    magnitude : typing.Optional[float]
    
    def calc_sentiment(self):
        client = language_v1.LanguageServiceClient()
        doc = {
          'content': self.text,
          'type_': language_v1.Document.Type.PLAIN_TEXT,
          'language': 'en' 
        }
        
        request = {
            'document': doc,
            'encoding_type': language_v1.EncodingType.UTF8
        }
        response = client.analyze_sentiment(request)
        
        self.sentiment = response.document_sentiment.score
        self.magnitude = response.document_sentiment.magnitude
        
        
@app.route('/')
def index():
    quote_url = 'https://quotes.toscrape.com/random'

    response = requests.get(quote_url)

    soup = BeautifulSoup(response.content, 'html.parser')

    quote_el = soup.find('div', class_='quote')

    quote = Quote(
        text=quote_el.find('span', class_='text').get_text(),
        author=quote_el.find('small', class_='author').get_text(),
        tags=[el.get_text() for el in quote_el.find_all('a', class_='tag')]
    )

    quote.calc_sentiment()
    
    return jsonify(quote.dict())

