from bs4 import BeautifulSoup as bs
import pandas as pd
from splinter import Browser
import requests
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()
    #NASA Mars News
    # URL of page to be scraped
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)

    #Set an HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find_all('div', class_='content_title')[1].text
    news_p = soup.find_all('div', class_='article_teaser_body')[0].text
    print(news_title)
    print(news_p)

    #JPL Mars Space Images - Featured Image
    space_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
    browser.visit(space_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    #Set HTML object
    html_space = browser.html

    # Parse HTML with BS
    soup2 = bs(html_space, 'html.parser')

    image_url = soup2.find('img',attrs={'class':'fancybox-image'})['src']
    #Website URL
    web_main_url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/'
    
    # Concatenate URL with image_url
    featured_image_url = web_main_url + image_url
    print(featured_image_url)

    #Mars Facts
    mars_url_facts = 'https://space-facts.com/mars/'

    #Create a data frame with the mars facts
    tables = pd.read_html(mars_url_facts)
    mars_fact_df = tables[0]
    

    mars_fact_df.columns = ['Description','Mars Data']
    

    mars_fact_df.set_index('Description', inplace=True)
    

    #mars_fact_df.to_html()
    with open('mars_facts_df.html', 'w') as fo:
        mars_fact_df.to_html(fo)

    #Mars Hemispheres
    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    # Set an HTML object
    html_hemi = browser.html

    # Parse HTML with Beautiful Soup
    soup_hemi = bs(html_hemi, 'html.parser')

    # Retrieve items that contain mars hemi info
    item = soup_hemi.find_all('div', class_='item')

    # Create a list
    hemi_list = []

    # URL
    hemi_main_url = 'https://astrogeology.usgs.gov'

    # For Loop
    for i in item:
        
        title = i.find('h3').text
        
        partial_img = i.find('a', class_='itemLink product-item')['href']
        
        browser.visit(hemi_main_url + partial_img)
        
        partial_html = browser.html
        
        soup_par = bs(partial_html, 'html.parser')
        
        image_url = hemi_main_url + soup_par.find('img', class_='wide-image')['src']
        
        hemi_list.append({"title": title, "img_url": image_url})
    
    hemi_list
    mars_data={
        'Mars_title':news_title,
        'Mars_paragraph': news_p,
        'Mars_featured_image': featured_image_url,
        'Mars_fact': mars_fact_df.to_html(),
        'Mars_hemispheres': hemi_list}
    browser.quit()
    return mars_data