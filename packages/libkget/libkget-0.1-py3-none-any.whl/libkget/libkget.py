from requests import get  
import re

class kget:
    def __init__(self):
        pass
    def get_filename(self, url):
        pattern = '/'
        file_name = re.split(pattern, url)[-1]
        
        return file_name

    def download(self, url):
        with open(self.get_filename(url) , "wb") as file:
            print("Downloading : ", url)
            response = get(url)
            file.write(response.content)
            print("Completed: ", self.get_filename(url))