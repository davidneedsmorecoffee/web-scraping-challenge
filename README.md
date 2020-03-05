# Web Scraping of NASA website content

This is a demo of creating a web app based on web scraping results of specific content from NASA websites.
See images of the final product in the `screenshots` folder

* `Splinter` was used to navigate the sites when needed
* `BeautifulSoup` was used to help find and parse out the necessary data.
* `PyMongo` was used for CRUD applications for the database. 
* `Bootstrap` was used to structure the HTML template.

This was done in two major steps.

## Step 1 - Scraping

* Initial scraping was done using a combination of  `Jupyter Notebook`, `BeautifulSoup`, `Pandas`, and `Requests/Splinter`.
* Each scraping code chunk was first tested individually (see `scrape_mars_testing_by_chunks.ipynb`) before consolidating into single function (see `scrape_mars.ipynb`)

Different web content from the NASA website was scraped, including:

### NASA Mars News

* Extracted the latest News Title and Paragraph Text from [NASA Mars News Site](https://mars.nasa.gov/news/)

### JPL Mars Space Images (Featured Image)

* Scraped JPL Featured Space Image from the [JPL NASA website](https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars).
 * `splinter` was used to navigate the site and find the full size current Featured Mars Image `.jpg` file. 
 * Identified the image url for full size image

### Mars Weather

* Scraped the latest Mars weather tweet from the Mars Weather twitter account [here](https://twitter.com/marswxreport?lang=en)

### Mars Facts

* Used `Pandas` to scrape the table containing facts about the Mars, including Diameter, Mass, etc, from the the Mars Facts webpage [here](https://space-facts.com/mars/)  
* Used `Pandas` to convert the data to a HTML table string for building a webpage later.

### Mars Hemispheres

* Obtain high resolution images for each of Mar's hemispheres from the the [USGS Astrogeology website](https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars).
* Set up scraper to click on each of the links to the hemispheres to identify the image url to the full resolution images.
* Scrape both the image url string for the full resolution hemisphere images, as well as the the Hemisphere title containing the hemisphere name. 
* Python dictionary was used to store the data using the keys - one for image of the url (`img_url`), and one for the title of the image (`title`) - to create a list which contains one dictionary for each Mars hemisphere.


## Step 2 - MongoDB and Flask Application

* Used MongoDB with Flask templating and created a new HTML page to displays all of the information that was scraped earlier (see above).

* The Jupyter notebook described earlier (`scrape_mars.ipynb`) was converted into a `Python` script (`scrape_mars.py`).
  * contains a function called `scrape` which will execute all of the scraping code (see above).
  * results in one Python dictionary containing all of the scraped data.

* Created a route called `/scrape` which imported the `scrape_mars.py` script and call the `scrape` function.
  * returned values in are stored in Mongo as a Python dictionary.

* Created a root route `/` which queried the Mongo database, and then pass the various scraped Mars data into an HTML to display the data.

* Created a template HTML file (`index.html`) which will utilize the Mars data dictionary (containing the scraped data described earlier), and display all of the data in the appropriate HTML elements. 
  * see images of the final product in the `screenshots` folder
