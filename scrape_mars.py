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
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    #Set an HTML object
    html = browser.html

    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').text
    news_p = soup.find('div', class_='article_teaser_body').text
    print(news_title)
    print ('----------')
    print(news_p)

    #JPL Mars Space Images - Featured Image
    space_url = 'https://spaceimages-mars.com/'
    browser.visit(space_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    #Set HTML object
    html_space = browser.html

    # Parse HTML with BS
    soup2 = bs(html_space, 'html.parser')

    image_url = soup2.find("img", class_="headerimage fade-in")["src"]

    # Concatenate URL with image_url
    featured_image_url = space_url + image_url
    print(featured_image_url)

    #Mars Facts
    mars_url_facts ='https://galaxyfacts-mars.com/'

    #Create a data frame with the mars facts
    tables=pd.read_html(mars_url_facts)
    mars_factsdf=tables[1]
    mars_factsdf.columns = ['Description', 'Mars']
    mars_factsdf.set_index('Description', inplace=True)
    mars_factsdf
    

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
    hemi_main_url = 'https://marshemispheres.com/'

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