"""
CodeToAGI — Episode 52 Challenge
Scrape author bios from quotes.toscrape.com
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
from urllib.parse import urljoin
import re

BASE_URL = "https://quotes.toscrape.com"

def scrape_author_bios():
    print("🚀 Starting author bio scraper...")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
    }
    
    authors = {}  # name -> bio (deduplication)
    
    # Step 1: Get all quote pages (there are multiple pages)
    page = 1
    while True:
        url = f"{BASE_URL}/page/{page}/"
        print(f"📄 Scraping page {page}...")
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"  Stopped at page {page} (status: {response.status_code})")
            break
            
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find all quote cards
        quote_cards = soup.select("div.quote")
        
        if not quote_cards:
            break
            
        for card in quote_cards:
            # Get author name and link
            author_tag = card.select_one("small.author")
            author_name = author_tag.get_text(strip=True) if author_tag else None
            
            about_link = card.select_one("a[href^='/author/']")
            
            if author_name and about_link:
                author_url = urljoin(BASE_URL, about_link['href'])
                
                # Step 2: Visit author page if not already scraped
                if author_name not in authors:
                    print(f"   👤 Fetching bio for: {author_name}")
                    try:
                        author_resp = requests.get(author_url, headers=headers)
                        if author_resp.status_code == 200:
                            author_soup = BeautifulSoup(author_resp.text, "html.parser")
                            
                            # Extract bio (the long description paragraph)
                            bio_tag = author_soup.select_one("div.author-description")
                            bio = bio_tag.get_text(strip=True) if bio_tag else "No bio available"
                            
                            # Clean bio a bit
                            bio = re.sub(r'\s+', ' ', bio).strip()
                            
                            authors[author_name] = bio
                            
                    except Exception as e:
                        print(f"   ⚠️  Error fetching {author_name}: {e}")
                    
                    time.sleep(0.8)  # Be polite
        
        page += 1
        time.sleep(1.0)  # Rate limiting between pages
    
    # Step 3: Save to CSV
    output_file = "author_bios.csv"
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Author", "Bio"])  # Header
        
        for name, bio in sorted(authors.items()):
            writer.writerow([name, bio])
    
    print(f"\n✅ Done! Scraped {len(authors)} unique authors.")
    print(f"📁 File saved as: {output_file}")
    print(f"   Total rows: {len(authors) + 1} (including header)")
    
    return len(authors)

if __name__ == "__main__":
    scrape_author_bios()
