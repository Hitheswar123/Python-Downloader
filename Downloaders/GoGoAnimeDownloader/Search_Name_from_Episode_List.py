from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
site_url=input("Enter the url : ")
urls=[site_url,]
search = input("Enter the wild search : ")
def main():
    driver=webdriver.Chrome()
    for url in urls:
        driver.get(url)
        content=driver.page_source.encode('utf-8').strip()
        soup= BeautifulSoup(content,'lxml')
        video_urls = soup.findAll('h3',class_="film-name")
        for video in video_urls[:10]:
            if search.lower() in video.text.lower():
                print(video.text)

main()

