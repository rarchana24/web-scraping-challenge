# Import Dependecies 
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests


    # @NOTE: Replace the path with your actual path to the chromedriver
executable_path = {"executable_path": "chromedriver.exe"}
browser = Browser("chrome", **executable_path, headless=False)
# Create Mission to mars dictionary 

# Defining scrape & dictionary
def scrape():
    final_data = {}
    output = scrape_mars_news()
    final_data["mars_news"] = output[0]
    final_data["mars_paragraph"] = output[1]
    final_data["mars_image"] = scrape_mars_jpl_image()
    final_data["mars_weather"] = scrape_mars_twitter_weather()
    final_data["mars_facts"] = scrape_mars_facts()
    final_data["mars_hemisphere"] = scrape_mars_hemisphere()

    return final_data

def scrape_mars_news():
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    #article = soup.find("div", class_='list_text')
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find_all("div", class_="content_title")[2].text.strip()
    output = [news_title, news_p]
    return output        


        
def scrape_mars_jpl_image():
   
        # Visit Nasa news url through splinter module
    JPL_Mars_Image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
        
    browser.visit(JPL_Mars_Image)
        
        # HTML Object
    JPL_Mars_image = browser.html
        # Parse HTML with Beautiful Soup
    soup_JPL_Mars_Image = BeautifulSoup(JPL_Mars_image, 'html.parser')
        #featured image URL
    featured_img_url=soup_JPL_Mars_Image.find("div", class_="carousel_items")
        #background image
    background_img_url=soup_JPL_Mars_Image.find('article')['style']
        #Splitting the image
    background_img_url_split=background_img_url.split("'")
    background_img_url_split_index=background_img_url_split[1]
        #Website URL
    base_url='https://www.jpl.nasa.gov'
        #Concatenate with the background image url
    featured_url =base_url+background_img_url_split_index
        #Display featured image
    featured_url
    return featured_url

        

        
def scrape_mars_twitter_weather():
    
    mars_weather_info = []
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    response = requests.get(url)
    twitter_soup = BeautifulSoup(response.text, 'lxml')
    twitter_data = twitter_soup.find_all('div', class_='js-tweet-text-container')
    tweet_text = twitter_soup.find_all('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')
    weather_text = 'InSight '
        
    for tweet in tweet_text:
        if weather_text in tweet.text:
            mars_weather = tweet.text
            mars_weather_info.append(mars_weather)
    return mars_weather_info
        
        
def scrape_mars_facts():
    
        #URL to get the facts
    facts_url = "https://space-facts.com/mars/"
        #Read the HTML from the URL
    facts_url_data = pd.read_html(facts_url)
        #time.sleep(2)
        #Create a dataframe
    facts_url_data_df = facts_url_data[0]
        #Rename the columns of the dataframe
    facts_url_data_df.columns =['Description','Value']
        #Set the index 
    facts_df = facts_url_data_df.set_index('Description')
        #convert to html
    facts = facts_df.to_html(index=True, header=True)
    return facts

        
def scrape_mars_hemisphere():
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    response_hemisphere = requests.get(hemispheres_url)
    soup_hemisphere = BeautifulSoup(response_hemisphere.text, 'lxml')
    mars_hemisphere = soup_hemisphere.find_all('div', class_='item')
    hemisphere_image_urls = []
        
        # Loop through each link of hemispheres on page
    for image in mars_hemisphere:
        hemisphere_url = image.find('a', class_='itemLink')
        hemisphere = hemisphere_url.get('href')
        hemisphere_link = 'https://astrogeology.usgs.gov' + hemisphere
            #print(hemisphere_link)
        browser = Browser('chrome', headless=False)
        browser.visit(hemisphere_link)
            # Create dictionary to hold title and image url
        
            # Need to parse html again for each of the hemisphere_link
        mars_hemispheres_html = browser.html
        mars_hemispheres_soup = BeautifulSoup(mars_hemispheres_html, 'html.parser')
            #print(mars_hemispheres_soup.body.prettify())
            # Get image link
        #hemisphere_image_link = mars_hemispheres_soup.find('a', text='Original').get('href')
        hemisphere_image_link = mars_hemispheres_soup.find('a', text='Sample').get('href')
            #print(hemisphere_image_link)
            # Get title text
        hemisphere_title = mars_hemispheres_soup.find('h2', class_='title').text.replace(' Enhanced', '')
        dictionary = {"title": hemisphere_title, "img_url": hemisphere_image_link}
        hemisphere_image_urls.append(dictionary)
    return hemisphere_image_urls

