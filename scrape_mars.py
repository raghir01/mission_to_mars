import requests
from bs4 import BeautifulSoup
import pymongo
from splinter import Browser
executable_path = {'executable_path': '/Users/raghi/Downloads/chromedriver'}
browser = Browser('chrome', **executable_path, headless=True)

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars
mars_collection = db.mars_collection


def get_data():
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C1\
    65%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    s = BeautifulSoup(browser.html, features="html.parser")
    title = s.find_all('div', class_='content_title')[0].text
    content = s.find_all('div', class_='rollover_description_inner')[0].text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    s = BeautifulSoup(requests.get(url).text, features="html.parser")
    img_url = s.findAll('article')[0]['style'].split(":")[1].split("'")[1]
    featured_image_url = "https://www.jpl.nasa.gov{}".format(img_url)

    url = 'https://twitter.com/marswxreport?lang=en'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    weather_data = soup.findAll('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    weather_data = filter(lambda x: x.text.lower().find('sol') != -1, weather_data)
    latest_weather = list(weather_data)[0].text.split('pic')[0]

    url = 'https://space-facts.com/mars/'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    facts_table =  soup.findAll('table', id='tablepress-mars')[0]
    rows = facts_table.findAll('tr')
    mars_facts = []
    for r in rows:
        cols = r.findAll('td')
        mars_facts.append((cols[0].text, cols[1].text))

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    items = soup.find_all('div', class_='item')
    image_data = []
    for item in items:
        description = item.find('div', class_='description').find('h3')
        item_link = item.find('a', class_='itemLink')['href'].split('/')[5]
        img_url = "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/{}.tif/full.jpg".format(item_link)
        image_data.append({
            "footer": description.text,
            "img_url": img_url
        })

    mars_data = {
        "title": title,
        "content": content,
        "featured_image_url": featured_image_url,
        "latest_weather": latest_weather,
        "mars_facts": mars_facts,
        "image_data": image_data,
    }
    existing = mars_collection.find_one()
    if existing:
        mars_data['_id'] = existing['_id']
        mars_collection.save(mars_data)
    else:
        mars_collection.save(mars_data)
    return mars_data


def get_from_db():
    return mars_collection.find_one()
