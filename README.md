# CodeToAGI — Episode 52 Challenge

## 🎯 Challenge: Scrape Author Bios

**Task**: Collect every author from [quotes.toscrape.com](https://quotes.toscrape.com/), visit their individual pages, extract their biography, and save everything to a clean CSV.

### Features Implemented
- Multi-page scraping
- Deduplication (each author only once)
- Proper headers (User-Agent)
- Rate limiting (`time.sleep`)
- Clean bio extraction
- CSV export with UTF-8 support

### How to Run

```bash
# 1. Activate environment
myenv\Scripts\activate

# 2. Run the challenge
python challenge_solution.py
