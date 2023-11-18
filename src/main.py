import asyncio
import json
from datetime import datetime
import sys
import logging
import argparse
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Crawling")

# Command-line arguments
parser = argparse.ArgumentParser(description="Asynchronous web crawler")
parser.add_argument("url", help="The starting URL for the crawl")
parser.add_argument("--output", default="data.json", help="Output file for crawled data")
parser.add_argument("--stats", default="crawl_stats.csv", help="Output file for crawl statistics")
parser.add_argument("--selectors", default=None,  nargs='+', help="List of CSS selectors to extract text")
parser.add_argument("--max-links", type=int, help="Maximum number of visited links to allow")
parser.add_argument("--annotate-size", type=int, help="Chunk data.json to this file size in MB")
args = parser.parse_args()

# Global constants
STATIC_FILE_EXTENSIONS = (
    '.webp', '.pdf', '.jpg', '.jpeg', '.png', '.gif', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.zip',
    '.rar', '.mp3', '.mp4', '.avi', '.flv', '.wmv', '.mov', '.wav', '.mid', '.midi', '.ogg', '.mkv',
    '.webm', '.m4a', '.m4v', '.3gp', '.m3u8', '.ts', '.m3u', '.apk', '.exe', '.dmg', '.iso', '.img',
    '.css', '.js', '.json', '.xml', '.svg', '.ico', '.ttf', '.otf', '.woff', '.woff2', '.eot', '.psd',
    '.ai', '.eps', '.ps', '.txt', '.rtf', '.wps', '.csv', '.dat', '.sav', '.sql', '.mdb', '.db', '.accdb'
)


async def fetch(session, url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        async with session.get(url, headers=headers, ssl=False) as response:
            response.raise_for_status()
            return await response.text()
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}")
        return None


async def extract_text(soup, selectors):
    if not selectors:
        return soup.get_text()
    elements = soup.select(', '.join(selectors))
    extracted_text = "\n".join([e.get_text() for e in elements])
    return extracted_text


async def crawl(start_url, domain):
    visited = []
    queue = set([start_url])

    async with aiohttp.ClientSession() as session:
        with open(args.stats, 'w') as f:
            f.write('Time,Links in Queue,Visited Links\n')

        while queue and (not args.max_links or len(visited) < args.max_links):
            url = queue.pop()
            logger.info(url)

            if any(v['url'] == url for v in visited):
                continue

            html_resp = await fetch(session, url)
            if html_resp is None:
                continue

            soup = BeautifulSoup(html_resp, 'html.parser')

            # Extract text based on CSS selectors
            extracted_text = await extract_text(soup, args.selectors)

            # Store URL, text, and other data
            visited.append({"url": url, "text": extracted_text})

            for link in soup.find_all('a', href=True):
                full_link = urljoin(url, link['href']).split('#')[0].split('?')[0]
                if urlparse(full_link).netloc == domain and full_link not in [k['url'] for k in visited] \
                        and not full_link.endswith(STATIC_FILE_EXTENSIONS):
                    queue.add(full_link)

            # Statistics and writing to file
            with open('crawl_stats.csv', 'a') as f:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                f.write(f'{now},{len(queue)},{len(visited)}\n')

    return visited


def chunk_json_data(data, chunk_size):
    chunks = []
    current_chunk = []
    current_chunk_size = 0

    for item in data:
        item_size = len(json.dumps(item))
        if current_chunk_size + item_size > chunk_size:
            chunks.append(current_chunk)
            current_chunk = []
            current_chunk_size = 0

        current_chunk.append(item)
        current_chunk_size += item_size

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def start_crawl(url):
    domain = urlparse(url).netloc
    visited_links = asyncio.run(crawl(url, domain))

    # Annotate data.json with file size in MB
    if args.annotate_size:
        chunk_size = args.annotate_size * 1024 * 1024  # Convert MB to bytes
        chunks = chunk_json_data(visited_links, chunk_size)
        for i, chunk in enumerate(chunks):
            chunk_filename = f'{i}_{args.output}'
            with open(chunk_filename, 'w') as file:
                json.dump(chunk, file, indent=4)

    visited_links = json.loads(json.dumps(visited_links, default=str))
    with open(args.output, 'w') as file:
        json.dump(visited_links, file, indent=4)


if __name__ == "__main__":
    start_crawl(args.url)
