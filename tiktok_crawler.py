from selenium import webdriver 
import undetected_chromedriver.v2 as uc
import chromedriver_autoinstaller
import time
import random
import os 

class TikTok:
    def __init__(self, proxy=False, uc=True, headless=False) -> None:
        chromedriver_autoinstaller.install()
        self.chrome_version = chromedriver_autoinstaller.get_chrome_version().split('.')[0]
        if uc:
            self.driver = self._init_driver_uc(proxy=proxy, headless=headless)
        else:
            self.driver = self._init_driver(proxy, headless)
        self.path = os.path.dirname(__file__)
    
    def _init_driver(self, proxy, headless):
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--start-maximized')
        if headless:
            options.add_argument('--headless')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        driver = webdriver.Chrome(options=options)
        return driver
    
    def _init_driver_uc(self, proxy, headless):
        options = uc.ChromeOptions()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--start-maximized")
        if proxy:
            options.add_argument("--incognito")
        if headless:
            options.add_argument("--headless")
        driver = uc.Chrome(options= options, version_main=self.chrome_version)
        return driver
    
    def scroll_down(self):
        # Get scroll height
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        # Scroll down to bottom
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Calculate new scroll height and compare with last scroll height
        new_height = self.driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            return False 
        else:
            return True 
        
    
    def get_url(self, index):
        video_urls = self.driver.find_elements('xpath', '//a[contains(@href, "video")]')
        video_urls = [item.get_attribute('href') for item in video_urls]
        for url in set(video_urls[index:]):
            print(url)
            with open(self.channel_path, 'a') as f:
                f.write(url + '\n')
        return len(video_urls)

    def crawl(self, channel_url):
        # Create data file
        channel = channel_url.split('@')[-1]
        self.channel_path = os.path.join(self.path, f'{channel}.txt')
        self.driver.get(channel_url) 
        time.sleep(random.randint(2,3))
        index = 0
        while self.scroll_down():
            time.sleep(random.randint(2,3)) 
            index = self.get_url(index)
if __name__ == '__main__':
    bot = TikTok()
    bot.crawl(channel_url='https://www.tiktok.com/@theanh28entertainment')