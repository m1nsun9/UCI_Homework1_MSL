from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager

# URLs
nasa_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
mars_facts_url = "https://space-facts.com/mars/"
usgs_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

def init_browser():
    # Setup splinter
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

    # Step 1. Scrape the NASA Mars news site 
    browser.visit(nasa_url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    soup = bs(html, 'html.parser')

    # collect the latest News Title and Paragraph Text
    content = soup.find_all('div', class_="list_text")

    titles = []
    paragraphs = []

    # collect title and description for each article and append to lists
    for article in content:
        try:
            # find divs with content-title class and article_teaser_body class
            title_tag = article.find('div', class_='content_title')
            paragraph = article.find('div', class_='article_teaser_body').text.strip()
            
            title = title_tag.find('a').text.strip()
            
            if (title and paragraph):
                titles.append(title)
                paragraphs.append(paragraph)
        except AttributeError as a:
            print(a)
        
    # retrieve latest and assign to variables 'news_title' and 'news_p'
    news_title = titles[0]
    news_p = paragraphs[0]

    # Step 2: Use Splinter to navigate through JPL Featured Space site 
    browser.visit(jpl_url)
    browser.is_element_present_by_css('div.fancybox-lock div.fancybox-wrap', wait_time=1)

    html = browser.html
    soup = bs(html, 'html.parser')

    # find image url for current Featured Mars Image and make sure image url is full size .jpg 
    browser.links.find_by_partial_text('FULL IMAGE').click()

    # # assign url to variable called 'featured_image_url'
    imagebox = soup.find('div', class_='default floating_text_area ms-layer')
    image_link = imagebox.footer.a['data-fancybox-href']

    featured_image_url = f"https://www.jpl.nasa.gov/{image_link}"

    # Step 4: Scrape USGS site and collect high res images for each of Mars' hemispheres
    browser.visit(usgs_url)
    browser.is_element_present_by_css("section.results-accordian div.collapsable div.results div.item", wait_time=1)
    html = browser.html
    soup = bs(html, 'html.parser')

    # collect names of each of hemisphere buttons to click and collect images
    hemisphere_buttons = soup.find_all('div', class_='description')

    hemispheres = []


    for hemisphere in hemisphere_buttons:
        try:
            # get button name and title of each hemisphere
            button = hemisphere.find('a', class_='itemLink').text
            title = button.rsplit(' ', 1)[0]
            
            # click each of the links to hemisphere to find image in full resolution
            browser.links.find_by_partial_text(button).click()
            browser.is_element_present_by_css('div.container div.downloads', wait_time=1)
            html = browser.html
            soup = bs(html, 'html.parser')
            
            # save both image url string for the full resolution hemisphere image, and
            # the Hemisphere title containing the hemisphere name to a dictionary using keys 'image_url' and 'title'
            hemisphere_dict = {}
            
            link = soup.find('li')
            image_url = link.a['href']
            
            hemisphere_dict['image_url'] = image_url
            hemisphere_dict['title'] = title
            
            # append the dictionary with the image url string and the hemisphere title to a list. 
            # This list will contain one dictionary for each hemisphere.
            hemispheres.append(hemisphere_dict)
            
            # return to last page to gather other hemispheres
            browser.visit(usgs_url)
        except:
            print('Hemisphere Not Available')

    browser.quit()
    final_output = {'news_title': news_title, 'news_p': news_p, 
                    'featured_image_url': featured_image_url, 'hemispheres': hemispheres}

    # Return all of the Mars Data collected
    return final_output