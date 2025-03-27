import os
import datetime
import feedparser
import requests
from bs4 import BeautifulSoup
from weasyprint import HTML
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import random

# List of User-Agent strings to rotate between
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.41 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

def get_top_articles(rss_url, num_articles=3):
    """
    Fetch the top articles from an RSS feed.
    
    Args:
        rss_url (str): URL of the RSS feed.
        num_articles (int): Number of articles to retrieve (default: 3).
    
    Returns:
        list: List of dictionaries containing article title, summary, and link.
    """
    feed = feedparser.parse(rss_url)
    articles = []
    for entry in feed.entries[:num_articles]:
        title = entry.get('title', 'No title')
        summary = entry.get('summary', 'No summary')
        link = entry.get('link', 'No link')
        articles.append({'title': title, 'summary': summary, 'link': link})
    return articles

def fetch_article_content(url):
    """
    Fetch and clean the article content using BeautifulSoup.
    
    Args:
        url (str): URL of the article.
    
    Returns:
        str: Cleaned article content.
    """
    try:
        # Use a randomly chosen User-Agent from the list
        headers = {
            'User-Agent': random.choice(USER_AGENTS),
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        article_body = ''
        for paragraph in soup.find_all('p'):
            article_body += paragraph.get_text() + '\n\n'
        
        return article_body.strip() or 'Content could not be extracted.'
    except Exception as e:
        print(f"Failed to fetch article content: {e}")
        return None

def save_article_as_txt(article, file_path):
    """
    Save article details to a TXT file.
    
    Args:
        article (dict): Dictionary with title, summary, and link.
        file_path (str): Path where the TXT file will be saved.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(f"Title: {article['title']}\n\n")
        f.write(f"Summary: {article['summary']}\n\n")
        f.write(f"Link: {article['link']}\n\n")

def save_article_as_pdf(article, file_path):
    """
    Save extracted article content as a PDF file.
    
    Args:
        article (dict): Dictionary with the article link.
        file_path (str): Path where the PDF file will be saved.
    """
    content = fetch_article_content(article['link'])
    if content:
        # Fix: Use a standard string concatenation to avoid issues with f-strings
        html_content = (
            "<html>"
            "<head><meta charset='utf-8'><title>" + article['title'] + "</title></head>"
            "<body><h1>" + article['title'] + "</h1><p>" + content.replace('\\n', '</p><p>') + "</p></body>"
            "</html>"
        )
        try:
            HTML(string=html_content).write_pdf(file_path)
        except Exception as e:
            print(f"Failed to convert article to PDF: {e}. Trying screenshot instead.")
            save_article_screenshot(article['link'], file_path.replace('.pdf', '.png'))

def save_article_screenshot(url, file_path):
    """
    Use Selenium to take a screenshot of the article.
    
    Args:
        url (str): URL of the article.
        file_path (str): Path where the screenshot will be saved.
    """
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1280,3000')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        driver.save_screenshot(file_path)
        driver.quit()
        print(f"Saved screenshot: {file_path}")
    except Exception as e:
        print(f"Failed to save screenshot: {e}")

def main():
    # List of news channels with their RSS feed URLs
    news_channels = [
        {
            "name": "The New York Times",
            "rss_url": "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml"
        },
        {
            "name": "Bloomberg",
            "rss_url": "https://www.bloomberg.com/feeds/businessweek.rss"
        },
        {
            "name": "CNBC",
            "rss_url": "https://www.cnbc.com/id/10000101/device/rss/rss.html"
        }
    ]
    
    # Create a directory named after today's date
    today = datetime.date.today().isoformat()  # e.g., "2025-03-27"
    os.makedirs(today, exist_ok=True)
    
    # Process each news channel
    for channel in news_channels:
        print(f"Fetching articles from {channel['name']}...")
        articles = get_top_articles(channel['rss_url'])
        
        # Save each article as TXT and PDF
        for i, article in enumerate(articles, 1):
            file_base = os.path.join(today, f"{channel['name'].replace(' ', '_')}_{today}_{i}")
            save_article_as_txt(article, file_base + '.txt')
            save_article_as_pdf(article, file_base + '.pdf')

if __name__ == "__main__":
    main()

# pip install requests beautifulsoup4 selenium weasyprint feedparser 
