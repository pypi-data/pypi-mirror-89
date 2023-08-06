# libkget

Simple python3 lib to download files from a url

## example:
```py
from libkget import kget

def main():
    url = "https://www.kalekale.ga/html/img/ritsu.png"
    kget(url).download()

if __name__ == "__main__":
    main()
```