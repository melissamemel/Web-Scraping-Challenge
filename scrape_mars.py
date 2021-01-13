from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pandas as pd
import time

def scrape():
    
    executable_path = {'executable_path': 'chromedriver.exe'}
 
    browser = Browser('chrome', **executable_path, headless=False)    
    
    # create mars_data dict that we can insert into mongo

    mars_data = {}

    # visit NASA Mars News site and scrape headlines
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    time.sleep(1)
    news_html = browser.html
    news_soup =bs(news_html, 'html.parser')


    # Scrape the Latest News Title
    slide_element = news_soup.select_one("ul.item_list li.slide")
    #slide_element.find("div", class_="content_title")

    news_title = slide_element.find("div", class_="content_title").get_text()
    print(f"The latest news title is: {news_title}")

    # Scrape the Latest Paragraph Text
    news_paragraph = slide_element.find("div", class_="article_teaser_body").get_text()
    print(f"The lanews_paragraphtest news paragraph is: {news_paragraph}")

    # Visit the JPL website and scrape the featured image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    time.sleep(1)
    

    # Ask Splinter to Go to Site and Click Button with Class Name full_image
    full_image_button = browser.find_by_id("full_image")
    full_image_button.click()

    # Find "More Info" Button and Click It
    browser.is_element_present_by_text("more info", wait_time=1)
    more_info_element = browser.find_link_by_partial_text("more info")
    more_info_element.click()

    # Parse Results HTML with BeautifulSoup
    html = browser.html
    image_soup = bs(html, "html.parser")

    img_url = image_soup.select_one("figure.lede a img").get("src")
    img_url

    # Use Base URL to Create Absolute URL
    img_url = f"https://www.jpl.nasa.gov{img_url}"
    print(img_url)

    mars_df= pd.read_html("https://space-facts.com/mars/")[0]
    mars_df.columns= ["Description", "Value"]
    mars_df.set_index("Description", inplace=True)

    mars_df_html= mars_df.to_html(header= False, index= False)


    hemisphere_image_urls = [
    {"title": "Cerberus Hemisphere", "img_url":"https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg"},
    {"title": "Valles Marineris Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg"},
        {"title": "Schiaparelli Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg"},
        {"title": "Syrtis Major Hemisphere", "img_url": "https://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg"} 
    ]

    scrape_data = {
        "news_title": news_title, 
        "news_paragraph": news_paragraph ,
        "image_URL": img_url,
        "mars_data": mars_df_html,
        "hemisphere_image": hemisphere_image_urls }
    
    return scrape_data


    