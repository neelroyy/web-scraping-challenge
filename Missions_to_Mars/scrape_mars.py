# Dependencies

from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser

# Chomedriver path
from webdriver_manager.chrome import ChromeDriverManager

def scrape_info():

    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Scrape the Mars News Site and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.
    # NASA MARS website
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # BeautifulSoup object, html.parser
    html = browser.html
    soup = bs(html, "html.parser")

    # Collect the latest News Title and Paragraph Text
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # JPL Mars Space Images - Featured Image
    # Visit the url for the Featured Space Image site
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    # XPATH to capture 
    xpath = '/html/body/div[1]/img'

    # Use splinter for image 
    results = browser.find_by_xpath(xpath)
    img = results[0]
    img.click()

    # BeautifulSoup
    # html.parser
    html = browser.html
    soup = bs(html, "html.parser")
    image_url = soup.find("img", class_="headerimage fade-in")["src"]

    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    # Assign the url string to a variable called featured_image_url
    featured_image_url = url + image_url

    # Mars Facts
    # Use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.

    url = 'https://galaxyfacts-mars.com/'

    tables=pd.read_html(url)
    df=tables[1]
    df.columns = ['Description', 'Measurement']

    html_table = df.to_html(classes = 'table table-striped')

    # Mars Hemispheres
    # Gather images for each mar's hemispheres

    url = "https://marshemispheres.com/"
    browser.visit(url)
    html = browser.html

    # Use Beautifulsoup and parse
    soup = bs(html, "html.parser")

    # Use Python dictionary to store the data using the keys img_url and title.
    image_urls = []

    # Append the dictionary with the image url string and the hemisphere title to a list.  The list will contain on 
    #..dictionary for each hemisphere.
    results = soup.find("div", class_ = "collapsible results")
    pics = results.find_all("div", class_="item")

    # Save both the image url string for the full resolution hemisphere image, and the Hemisphere title.
    for pic in pics:
        
        title = pic.find("h3").text
        
        title = title.replace("Enhanced", "")
        
        link = pic.find("a")["href"]
        pic_link = url + link    
        browser.visit(pic_link)
        
        html = browser.html
        soup = bs(html, "html.parser")
        
        downloads = soup.find("div", class_="downloads")
        pic_url = downloads.find("a")["href"]
        
        image_urls.append({"title": title, "image_url": url + pic_url})

    mars_data = {
        "test_variable":"This is a test.", 
        "news_title":news_title, 
        "news_p":news_p,
        "htmltable":html_table,
        "featured_image_url":featured_image_url,
        "hemispheres":image_urls
        }

    browser.quit()
    return mars_data

