from requests import get  
import re

class kget:
    def __init__(self, url):
        pattern = '/'
        self.file_name = re.split(pattern, url)[-1]
        self.url = url

    def download(self):
        with open(self.file_name, "wb") as file:
            print("Downloading : ", self.url)
            response = get(self.url)
            file.write(response.content)
            print("Completed: ", self.file_name)