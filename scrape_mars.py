from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
from pprint import pprint

#############################################################
# define a function to initiate browser
def init_browser():
    executable_path = {"executable_path": "C:/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


# the scrape_all utilizes the other functions defined, e.g. scrape_mars_twitter()
# and put the returned values from these functions in a dictionary
def scrape_all():
    browser = init_browser()
    ########################################################
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
    # Assign the text to variables that you can reference later.
    # Example:
    # news_title = "NASA's Next Mars Mission to Investigate Interior of Red Planet"
    # news_p = "Preparation of NASA's next spacecraft to Mars, InSight, has ramped up this summer, on course for launch next May from Vandenberg Air Force Base in central California -- the first interplanetary launch in history from America's West Coast."
    
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    news_soup = bs(html, "html.parser")
    
    latest_news_title = news_soup.find("div", class_="content_title").text
    latest_news_p = news_soup.find("div", class_="article_teaser_body").text
    
    ########################################################
    # Visit the url for JPL Featured Space Image here.
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    # Make sure to find the image url to the full size .jpg image.
    # Make sure to save a complete url string for this image.
    # # Example:
    # featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'

    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(2)

    #https://splinter.readthedocs.io/en/latest/elements-in-the-page.html
    #.click_link_by_partial_text
    #.click_link_by_text('my link')
    browser.click_link_by_partial_text('FULL IMAGE') 
    time.sleep(2)
    browser.click_link_by_partial_text('more info')
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    feat_img_soup = bs(html, 'html.parser')
    
    featured_image_url = feat_img_soup.find('figure', class_='lede').a['href']
    featured_full_image_url = f'https://www.jpl.nasa.gov{featured_image_url}'

    ###########################################################
    # Mars Weather
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 
    # Save the tweet text for the weather report as a variable called mars_weather.
    # # Example:
    # mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'
    # https://twitter.com/marswxreport?lang=en

    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    twitter_soup = bs(html, 'html.parser')
    
    #https://www.datacamp.com/community/tutorials/scraping-reddit-python-scrapy
    #https://stackoverflow.com/questions/53586149/split-string-from-beautifulsoup-output-in-a-list
    
    # sometimes the tweet has an image which can result in a link in the text scraping
    # the 'try' tries to extract and remove the image link via .find('a') if it's present
    # if the image link is not present then 'except AttributeError' will kick in,
    # which is just a straight forward scrape
    try:
        mars_weather = twitter_soup.find('p', class_='TweetTextSize')
        mars_weather.find('a').extract()
        mars_weather = mars_weather.text
    except AttributeError:
        mars_weather = twitter_soup.find('p', class_='TweetTextSize').text.replace('\n', ' ')

    ############################################################
    # Mars Facts
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet 
    # including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    url = 'https://space-facts.com/mars/'
    
    mars_facts = pd.read_html(url)
    mars_facts = mars_facts[0].rename(columns={0: "Facts", 1:"Values"})
    
    mars_facts.set_index('Facts', inplace=True)
    mars_facts_html = mars_facts.to_html()

    ##############################################################
    # Mars Hemispheres
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.
    # You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.
    # Save both the image url string for the full resolution hemisphere image, 
    # and the Hemisphere title containing the hemisphere name. 
    # Use a Python dictionary to store the data using the keys img_url and title.
    # Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.
    # # Example:
    # hemisphere_image_urls = [
    #     {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #     {"title": "Cerberus Hemisphere", "img_url": "..."},
    #     {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #     {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    # ]

    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    time.sleep(2)

    # Scrape page into Soup
    html = browser.html
    hemi_soup = bs(html, 'html.parser')
    
    hemi_title_temp = []
    hthrees = hemi_soup.find_all('h3')
    
    for i in hthrees:
        hemi_title_temp.append(i.text)
        
    #pprint(hemi_title_temp)
    
    # Create an emtpy list named hemisphere_image_urls per guide
    hemisphere_image_urls = []

    # Loop through the hemisphere links to obtain the images
    for k in hemi_title_temp:
        # Create an empty dictionary for the hemisphere titles and urls
        hemi_dict = {}
        
        # https://splinter.readthedocs.io/en/latest/finding.html
        # Click on link by partial text (from the k-th entry in hemi_title)
        browser.click_link_by_partial_text(k)
        
        # Put the the k-th title into dictionary
        hemi_dict["title"] = k
        
        # Look for the url string with text 'sample' and put into img_url part of the dict
        # hemi_dict["img_url"] = browser.find_by_text('Sample')['target'] #this returned '_blank' instead 
        hemi_dict["img_url"] = browser.find_by_text('Sample')['href'] #works
        
        # Append to the hemi_dict, which has titles and img_urls, to the list hemisphere_image_urls
        hemisphere_image_urls.append(hemi_dict)
    
        #pprint(hemisphere_image_urls)
    
        # Go back to the previous page to start the loop again
        # https://splinter.readthedocs.io/en/latest/browser.html
        browser.back()
        time.sleep(1)

    mars_all = {
        "news_title": latest_news_title,
        "news_paragraph": latest_news_p,
        "featured_image_url": featured_full_image_url,
        "weather": mars_weather,
        "facts": mars_facts_html,
        "hemispheres": hemisphere_image_urls,
    }
    
    browser.quit()  
    return mars_all








