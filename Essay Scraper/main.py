from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from tqdm import tqdm, trange
from threading import Thread
import os
import re
import string

regex = re.compile('[%s]' % re.escape(string.punctuation))
class EssayScraper(Thread):
    def __init__(self, driver, links, thread_id):
        super().__init__()
        self.thread_id = thread_id
        self.driver = driver
        self.links = links

    def run(self):
        for link in tqdm(self.links):
            try:
                filename = f"{regex.sub('', link.text)}.txt"
                self.driver.get(link.get_attribute('href'))
                content = self.driver.find_element(By.CLASS_NAME, 'entry-content').text

                with open(f"Data/{filename}", 'w') as f:
                    f.write(content)
            except Exception as e:
                continue
                print(f"[{e}] raised in Thread-{self.thread_id}")


driver = webdriver.Edge()
driver.get('https://www.toppr.com/guides/essays/')

content = driver.find_element(By.CLASS_NAME, 'entry-content')
links = content.find_elements(By.CSS_SELECTOR, 'ul > li > a')
#links = [link.get_attribute('href') for link in links]

os.makedirs('Data/')
num_threads = 5
links_per_thread = len(links) // num_threads
drivers = [webdriver.Edge() for _ in range(num_threads)]

for thread_id in range(num_threads):
    driver = drivers[thread_id]
    selected_links = links[thread_id*links_per_thread:thread_id*links_per_thread + links_per_thread]
    thread = EssayScraper(driver,selected_links, thread_id)
    thread.start()
