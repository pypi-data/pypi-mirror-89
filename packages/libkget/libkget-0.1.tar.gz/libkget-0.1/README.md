# libkget

Simple python3 lib to download files from a url

## example:
```py
from libkget import kget

def main():
    url = "https://www.kalekale.ga/html/img/ritsu.png"
    get = kget()
    get.download(url)

if __name__ == "__main__":
    main()
```