import pandas as pd
import numpy as np
import requests as req
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()

    #
    ### NASA Mars News 
    #

    # Visit url for NASA Mars News -- Latest News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get article title and paragraph text
    article = soup.find("div", class_='list_text')
    news_title = article.find("div", class_="content_title").text
    news_p = article.find("div", class_ ="article_teaser_body").text

    #
    ### JPL Mars Space Images
    #

    # Visit url for JPL Featured Space Image
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    # Parse HTML with Beautiful Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get featured image
    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov" + image

    #
    ### Mars Weather
    #

    # Visit Twitter url for latest Mars Weather
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Extract latest tweet
    tweet_container = soup.find_all('div', class_="js-tweet-text-container")

    # Loop through latest tweets and find the tweet that has weather information
    for tweet in tweet_container: 
        mars_weather = tweet.find('p').text
        if 'Sol' and 'pressure' in mars_weather:
            print(mars_weather)
            break
        else: 
            pass
    
    #
    ### Mars Facts
    #

    # Visit Mars Facts webpage for interesting facts about Mars
    facts_url = "https://space-facts.com/mars/"
    browser.visit(facts_url)
    html = browser.html

    # Use Pandas to scrape the table containing facts about Mars
    mars_data = pd.read_html(facts_url)
    mars_data = pd.DataFrame(mars_data[1])

    # Rename columns
    mars_data.columns = ['Description','Value']

    # Reset Index to be description
    mars_data = mars_data.set_index('Description', inplace=True)

    # Use Pandas to convert the data to a HTML table string
    mars_facts = mars_data.to_html(index=True, header=True)

    #
    ### Mars Hemispheres
    #

    # Visit USGS webpage for Mars hemispehere images
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, "html.parser")

    # Create dictionary to store titles & links to images
    hemisphere_image_urls = []

    # Retrieve all elements that contain image information
    reults = soup.find("div", class_ = "result-list" )
    hemispheres = results.find_all("div", class_="item")

    # Iterate through each image
    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup = bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

    #
    ### Store Data
    #

    # Store data in a dictionary
    mars_data = {
        "News_Title": news_title,
        "News_Paragraph": news_p,
        "Featured_Image": featured_image_url,
        "Mars_Weather": mars_weather,
        "Mars_Facts": mars_facts,
        "Hemisphere_Image": hemisphere_image_urls
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
