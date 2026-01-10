IscrapeMDB

The robust, browser-agnostic IMDb data extractor.
No API keys. No rate limits. Just data.

<img width="382" height="73" alt="image" src="https://github.com/user-attachments/assets/3681050d-70e6-43e8-9c7a-de63b8472519" />

What is this?

IScrapeMDB is a Python-based automation tool that scrapes detailed metadata from IMDb. Unlike basic scrapers that just grab a title and a rating, this tool digs deep. It extracts cast lists, full reviews, parental guides, runtime, directors, and recursively scrapes entire series episode lists.

It uses Selenium to handle dynamic content, meaning it captures data that simple requests or BeautifulSoup scripts miss.

Key Features:

Browser Agnostic: Supports Chrome and Firefox.

Deep Extraction: Grabs hidden reviews, cast roles, and parental guidance details.

Series Support: Recursively scrapes every single episode of a TV show.

Portable Data: Saves data locally in structured formats and generates an offline HTML viewer.

<img width="1125" height="819" alt="image" src="https://github.com/user-attachments/assets/a5db1170-ed2d-42a7-8132-00154d2a7ad3" />


Resilient: Skips missing data points without crashing the entire batch.

Installation

Clone the repo:

git clone [https://github.com/YourUsername/IscrapeMDB.git](https://github.com/YourUsername/IscrapeMDB.git)
cd IscrapeMDB


Install dependencies:

pip install -r requirements.txt


Browser Setup:
Ensure you have Chrome or Firefox installed. The script handles the drivers automatically.

How to Use

The main entry point is main.py. It is built to be flexible—whether you need data for one movie or a list of 500.

1. The Basics (Single Scrape)

To scrape a single movie or series and save its data:

python main.py link


What happens?

The tool identifies the media type (Movie vs Series).

It creates a folder: Scraped/Movies/The Shawshank Redemption (1994)/.

Inside data/, it saves main.js (metadata) and review.js (user reviews).

2. Batch Scraping (Text File)

If you have a list of URLs, put them in a text file (one URL per line) and run:

python main.py -f my_links.txt


3. Curated Lists (Organize Your Data)

If you want to group specific scrapes together (e.g., "Horror Marathon"), use the List mode.

Create a new list and scrape to it:

python main.py -l "Horror_Classics"


This creates a dedicated folder structure in Scraped/Lists/Horror_Classics.

Append items to an existing list:

python main.py link1 link2 .... linki -a "Scraped/Lists/Horror_Classics"

<img width="921" height="294" alt="image" src="https://github.com/user-attachments/assets/de1f4b46-c7a3-41a7-8bc1-a5ab051e6e3b" />


Advanced Options

You can tweak how the scraper behaves with these flags:

Flag

Description

--browser

Choose backend: chrome (default) or firefox.

--head

Run in headed mode (browser is visible). Useful for debugging.

--fast

Speed Mode: Skips Reviews and Parental Guides to scrape faster.

-r

Deep Reviews: Scrolls and clicks "Load More" to get maximum reviews.

--no-html

Data Only: Skips generating the index.html viewer.

-portable

Converts a scraped folder into a single, offline-ready HTML file.

Example: Fast scrape using Firefox

python main.py "URL" --browser firefox --fast


Data Structure

The main goal of IscrapeMDB is data gathering. Here is how your data is organized after a scrape:

(Replace with screenshot of your /data folder)

main.js: Contains the core metadata (Title, Rating, Runtime, Cast, Director, etc.).

review.js: Contains an array of user reviews (Title + Content).

index.html: A local viewer to inspect your data visually.

License

Polyform Non-Commercial License 1.0.0

This software is free for personal, educational, and research use.

You can use it to build your personal media library.

You can modify it for your own learning.

You cannot use this tool for commercial purposes (selling the data, selling the software, or using it in a paid service).

See LICENSE for details.

Disclaimer: This tool is for educational purposes. Please respect IMDb's terms of service and do not use this for high-velocity scraping that could affect their servers.
