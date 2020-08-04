import scrapy
from scrapy.selector import Selector
from selenium import webdriver
from shutil import which
from selenium.webdriver.chrome.options import Options

    

class coinSpiderSelenium(scrapy.Spider):
    name = 'seleniumcoins'
    allowed_domains = ['www.livecoin.net/en']
    start_urls = [
        'https://www.livecoin.net/en'
    ]   
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')

        chrome_driver = which ('chromedriver')
        driver =  webdriver.Chrome(chrome_driver ,options= chrome_options)
        driver.set_window_size(1920,1080)

        driver.get("https://www.livecoin.net/en") 
        othercoins = driver.find_elements_by_class_name('filterPanelItem___2z5Gb')
        othercoins[5].click()
        self.html = driver.page_source
        driver.close()

    def parse(self, response):
        resp =  Selector(text=self.html)
        for currency in resp.xpath('//div[contains(@class,"ReactVirtualized__Table__row tableRow___3EtiS " )]'):
            yield {
                'Coin' : currency.xpath('.//div[1]/div/text()').get(),
                'Volume ' : currency.xpath('.//div[2]/span/text()').get(),
                'Change ' : currency.xpath('.//div[4]/span/span/text()').get()
                }
        
