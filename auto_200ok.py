import requests
import time

def check_website(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print(f"Website {url} is up!")
        else:
            print(f"Website {url} returned a status code {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error checking website {url}: {e}")

url = 'https://example.com' while True: check_website(url) time.sleep(3600) # Check every hour
