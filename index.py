import random
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests

url = 'https://www.brainyquote.com/topics'
source = requests.get(url)

print('Status Code: ', source.status_code)
if source.status_code != 200:
    raise Exception("Can't get url: " + url)

soup = BeautifulSoup(source.text, 'html.parser')

topic_scrapped = soup.find('main').select('div.bqLn')
topics_text = ['Sports', 'Success', 'Technology', 'Motivational', 'Humor', 'Wisdom', 'Life', 'Inspirational', 'Money', 'Freedom']
topic_elements = []

for topic in topic_scrapped:
    if str(topic.a.text).strip() in topics_text and str(topic.a.text).strip() not in list(map(lambda x: str(x.a.text).strip() ,topic_elements)):
        topic_elements.append(topic)


def quote_soup(topic_element):
    q_url = 'https://www.brainyquote.com' + topic_element.a['href']
    q_source = requests.get(q_url)
    if q_source.status_code != 200:
        raise Exception("Can't get the category url: " + q_url)
    q_soup = BeautifulSoup(q_source.text, 'html.parser')
    q_elements = q_soup.select_one('main').find_all('div', class_='grid-item qb clearfix bqQt')
    q_source.close()
    return q_elements


all_quotes_elements = sum(list(map(quote_soup, topic_elements)), [])
print(len(all_quotes_elements))

#function to extract the quote text and author from the div element.
def quotes(element):
    quote = element.find('a', class_='b-qt').text
    author = element.find('a', class_='bq-aut').text
    return (quote, author)


app = Flask(__name__, template_folder='./templates', static_folder='./static')
@app.route('/')
def index():
    selected_elements = random.choices(all_quotes_elements, k=12)

    [(first_quote, first_author),
    (second_quote, second_author),
    (third_quote, third_author),
    (fourth_quote, fourth_author),
    (fifth_quote, fifth_author),
    (sixth_quote, sixth_author),
    (seventh_quote, seventh_author),
    (eighth_quote, eighth_author),
    (ninth_quote, ninth_author),
    (tenth_quote, tenth_author),
    (eleventh_quote, eleventh_author),
    (twelfth_quote, twelfth_author)] = list(map(quotes, selected_elements))


    return render_template('index.html', **locals())



if __name__ == '__main__':
   app.run()
