import urllib.request, time
from selenium import webdriver

#urls to test with
url1 = "https://makershare.com/projects/sunrise-light-part-1-makevember-002"
url2 = "https://makershare.com/projects/urban-data-posts"

project_info = []

def download_file(download_url):
    """
    Requires full http url of file to download
    
    Downloads files accessed from get_project_info
    uses the end of the public/ folder as a starting
    point to name the file, and the question mark put
    after the file by Maker Share to define the end.
    """
    name_start = download_url.find("/public/") + 8
    name_end = download_url.find("?")
    name = download_url[name_start:name_end]
    project_info.append(name)
    urllib.request.urlretrieve(download_url, name)

def print_to_file(project_list):
    """
    Requires list created by get_project_info
    and a test.txt file in the code directory

    Writes test.txt to a variable, then creates
    a file texttwo.txt and rewrites test.text
    with items in list inserted individually
    into the file.
    """

    #write template to variable
    with open("test.txt") as f:
        text_template = f.read()
    f.closed

    #output html
    print("writing file")
    with open("project_text.txt", "w") as text_file:
        print(text_template.format(*project_list), file=text_file)
    

def get_project_info (url):
    """
    Requires full http url of Maker Share project

    Scrapes Maker Share project for key elements:
    title, short description, tags, and author info,
    including project and author images.

    After scraping, project and author images are
    sent to download_file for downloading
    """
    
    #choose browser (Firefox/Chrome) and import url (change url link above)
    driver = webdriver.Firefox()
    driver.get(url)

    print("start")
    #delay - change depending on connection speed and load times
    time.sleep(3)
    
    #grab project and author data in the following order
    project_info.append(url)
    project_info.append(driver.find_element_by_class_name("img-responsive").get_attribute('src'))
    project_info.append(driver.find_element_by_class_name("card-title").text)
    project_info.append(driver.find_element_by_xpath("//p[@class='inner-html']").text)
    project_info.append(driver.find_element_by_xpath("//*[@class='project-tag']/span").text)
    try:
        project_info.append(driver.find_element_by_class_name("card-owner-media").get_attribute('src'))
    except:
        project_info.append("no image found")

    project_info.append(driver.find_element_by_class_name("card-owner-link").get_attribute('href'))
    project_info.append(driver.find_element_by_class_name("card-owner-link").text)
    try:
        project_info.append(driver.find_element_by_class_name("maker-description").text)
    except:
        project_info.append("Concocting a pithy quote")
        
    try:
        project_info.append(driver.find_element_by_class_name("maker-city").text)
    except:
        project_info.append("Location Unknown")

    #close browser
    driver.quit()

    #download images
    try:
        download_file(project_info[1])
    except:
        print("Unable to find project image")
    try:
        download_file(project_info[5])
    except:
        print("Unable to find profile photo")


get_project_info(url2)

print_to_file(project_info)
print("done")
