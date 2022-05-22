from selenium import webdriver
from bs4 import BeautifulSoup
import lxml
urls=['https://gogoanime.gg/category/spy-x-family',]

def main():
    driver=webdriver.Chrome()
    for url in urls:
        driver.get(url)
        content=driver.page_source.encode('utf-8').strip()
        soup= BeautifulSoup(content,'lxml')
        video_urls = soup.findAll('div',class_="name")
        for video in video_urls[:10]:
            print(video.text)

main()

