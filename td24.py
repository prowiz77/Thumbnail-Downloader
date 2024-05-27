import os
import re
import argparse
import requests
from bs4 import BeautifulSoup

# Pornhub     ✅
# xHamster    ✅
# xvideos     ✅
# xnxx        ✅
# youporn     ✅
# redtube     ✅
# vrporn      ✅
# czechvr     🟧
# vrbangers   ✅
# vrsmash     ✅
# badoinkvr   ✅
# wankzvr     ✅
# sexlikereal ✅

PATH = None

class ElementAttributeFetcher:
    def __init__(self, url, class_name, attribute_type):
        self.url = url
        self.class_name = class_name
        self.attribute_type = attribute_type
        self.attribute_value = self.fetch_attribute_value()

    def fetch_attribute_value(self):
        # Fetch HTML content from the URL
        response = requests.get(self.url)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse HTML content using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find the element with the specified class name
            element = soup.find(class_=self.class_name)
            
            # Check if such element exists
            if element:
                # Get the specified attribute value
                attribute_value = element.get(self.attribute_type)
                download_image(attribute_value, 'test.jpg')
                return attribute_value
            else:
                print(f"No element with class '{self.class_name}' found.")
        else:
            print("Failed to fetch URL:", response.status_code)

def download_image(url, save_path):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        
        # Check if the request was successful
        if response.status_code == 200:
            # Open a file in binary write mode and save the image data
            with open(save_path, 'wb') as file:
                file.write(response.content)
            print("Image downloaded successfully!")
        else:
            print(f"Failed to download image: {response.status_code}")
    except Exception as e:
        print("An error occurred while downloading the image:", e)

def find_thumb_url(url, pattern):
    try:
        # Webseite abrufen
        response = requests.get(url)
        response.raise_for_status()

        # HTML-Inhalt der Webseite extrahieren
        html_content = response.text

        # Muster suchen
        match = re.search(pattern, html_content)

        # Wenn ein Treffer gefunden wurde, gib den Link zurück
        if match:
            thumb_url = match.group(1)
            download_image(thumb_url, PATH)
            return thumb_url
        else:
            return None

    except Exception as e:
        print("Fehler beim Abrufen der URL:", e)
        return None
    
def classify_domain(url, quality):
    if "pornhub.com" in url:
        ElementAttributeFetcher(url, 'videoElementPoster', 'src')
    elif "xhamster.com" in url:
        ElementAttributeFetcher(url, 'player-container__no-script-video', 'poster')
    elif "xvideos.com" in url:
        find_thumb_url(url, r"html5player\.setThumbUrl169\('(.+?)'\);")
    elif "xnxx.com" in url:
        find_thumb_url(url, r"html5player\.setThumbUrl169\('(.+?)'\);")
    elif "youporn.com" in url:
        ElementAttributeFetcher(url, 'videoPlayer', 'src')
    elif "redtube.com" in url:
        find_thumb_url(url, r'<link\s+rel="preload"\s+as="image"\s+href="(.+?)">')
    elif "vrporn.com" in url:
        find_thumb_url(url, r'<link\s+rel="preload"\s+fetchpriority="high"\s+as="image"\s+href="(.+?)">')
    elif "czechvr.com" in url:
        find_thumb_url(url, r'<dl8-video\s+format="([^"]*)"\s+poster="([^"]*)"\s*')
    elif "vrbangers.com" in url:
        if quality == '1':
            find_thumb_url(url, r'<div\s+data-testId="element_000087"\s+class="[^"]*"\s+data-v-[^>]*><img\s+src="([^"]*)"')
        else:
            find_thumb_url(url, r'<meta\s+data-n-head="ssr"\s+data-hid="og:image"\s+property="og:image"\s+content="([^"]*)"')
    elif "vrsmash.com" in url:
        find_thumb_url(url, r'<meta\s+property="og:image"\s+content="([^"]*)"')
    elif "badoinkvr.com" in url:
        ElementAttributeFetcher(url, 'video-image', 'src')
    elif "wankzvr.com" in url:
        find_thumb_url(url, r'<meta\s+property="og:image"\s+content="([^"]*)"')
    elif "sexlikereal.com" in url:
        find_thumb_url(url, r'<link\s+rel="preload"\s+href="([^"]*)"\s+as="image"')
    else:
        print(False)

def main():
    global PATH
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch attribute value of an element from a webpage.')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL of the webpage')
    parser.add_argument('-q', '--quality', type=str, required=False, help='Quality of Image(default=nothing, high-quality=1)')
    parser.add_argument('-n', '--name', type=str, required=True, help='Name of image without filetype')
    args = parser.parse_args()

    PATH = args.name + '.png'

    classify_domain(args.url, args.quality)

if __name__ == '__main__':
    main()
