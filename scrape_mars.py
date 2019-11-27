#importing the following libraries.
import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd

def init_browser():
    # https://splinter.readthedocs.io/en/latest/drivers/chrome.html
    #  !which chromedriver
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    return browser

def scrape():
    browser = init_browser()

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    news_title = soup.find('div', class_="content_title").text
    news_p = soup.find('div', class_="article_teaser_body").text

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    image_name= soup.find('article', class_='carousel_item')['alt'] 

    base_url = 'https://www.jpl.nasa.gov'
    img_url = soup.find(attrs={'data-title':image_name})["data-fancybox-href"] 
    featured_image_url = base_url + img_url

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars_weather= soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    url = 'https://space-facts.com/mars/'

    tables = pd.read_html(url)
    mars_df = tables[1]
    mars_df.columns = ['Mars - Earth Comparison', 'Mars','Earth']
    html_table = mars_df.to_html(header=None,index=False)
    html_table.replace('\n', '')

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    product = soup.find('div', class_="collapsible results")
    hemisphere_items = product.find_all('div', class_="item")
    hemisphere_img_urls = []

    for item in hemisphere_items:
        try:
            hemisphere_title  = item.find('h3').text
            hemisphere_href = item.find('a')['href']
            hemisphere_url = "https://astrogeology.usgs.gov"+hemisphere_href
            hemisphere_page = requests.get(hemisphere_url).text
            soup = BeautifulSoup(hemisphere_page, 'html.parser')

            hemisphere_page_img = soup.select('#wide-image > div > ul > li:nth-child(1) > a')
            hemisphere_img_url =  hemisphere_page_img[0]['href']
            hemisphere_img_dict = { "image title": hemisphere_title, "image url": hemisphere_img_url }
            hemisphere_img_urls.append(hemisphere_img_dict)

        except Exception as e:
            print(e)

    mars_info = {
            "News_Title": news_title,
            "Paragraph_Text": news_p,
            "Most_Recent_Mars_Image": featured_image_url,
            "Mars_Weather": mars_weather,
            "Mars_Table": html_table,
            "Mars_Hemispheres": hemisphere_img_urls
        }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_info

