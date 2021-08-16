import typing

import requests

from bs4 import BeautifulSoup
from flask import Flask, jsonify
from pydantic import BaseModel


app = Flask(__name__)


class Quote(BaseModel):
    text : str
    author : str
    tags : typing.Sequence[str]


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

    return jsonify(quote.dict())

