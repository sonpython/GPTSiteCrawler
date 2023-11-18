# GPT Query

Craw content from a website an all its subpages and store it in a database. Then use GPT create your own custom GPT and generate new content based on the crawled content.

screenshots:

![image](https://raw.githubusercontent.com/sonpython/GPTSiteCrawler/main/screenshot.png)

## Demo Link
https://chat.openai.com/g/g-RskOOlLFp-sumato-assistant

## How to use
### Prerequisites
- Python 3.11

### Setup
- Clone this repo
`git clone https://github.com/sonpython/GPTSiteCrawler`
- craete a virtual environment: `python3 -m venv venv`
- activate the virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`
- Run the crawler: `python src/main.py https://example.com --selectors .main --annotate-size 2`

### Usage

```bash
> python src/main.py -h
usage: main.py [-h] [--output OUTPUT] [--stats STATS] [--selectors SELECTORS [SELECTORS ...]] [--max-links MAX_LINKS] [--annotate-size ANNOTATE_SIZE] url

Asynchronous web crawler

positional arguments:
  url                   The starting URL for the crawl

options:
  -h, --help            show this help message and exit
  --output OUTPUT       Output file for crawled data
  --stats STATS         Output file for crawl statistics
  --selectors SELECTORS [SELECTORS ...]
                        List of CSS selectors to extract text
  --max-links MAX_LINKS
                        Maximum number of visited links to allow
  --annotate-size ANNOTATE_SIZE
                        Chunk data.json to this file size in MB

```

## Docker
env vars
```env
CRAWLER_URL=https://example.com 
CRAWLER_SELECTOR=.main 
CRAWLER_CHUNK_SIZE=2 # in MB
```

### Build
`docker build -t gpt-site-crawler .`
### Run
`docker run -it --rm gpt-site-crawler`

(I borrow the bellows docs from @BuilderIO)
### Upload your data to OpenAI 

The crawl will generate a file called `output.json` at the root of this project. Upload that [to OpenAI](https://platform.openai.com/docs/assistants/overview) to create your custom assistant or custom GPT.

#### Create a custom GPT

Use this option for UI access to your generated knowledge that you can easily share with others

> Note: you may need a paid ChatGPT plan to create and use custom GPTs right now

1. Go to [https://chat.openai.com/](https://chat.openai.com/)
2. Click your name in the bottom left corner
3. Choose "My GPTs" in the menu
4. Choose "Create a GPT"
5. Choose "Configure"
6. Under "Knowledge" choose "Upload a file" and upload the file you generated

![Gif of how to upload a custom GPT](https://github.com/BuilderIO/gpt-crawler/assets/844291/22f27fb5-6ca5-4748-9edd-6bcf00b408cf)


#### Create a custom assistant

Use this option for API access to your generated knowledge that you can integrate into your product.

1. Go to [https://platform.openai.com/assistants](https://platform.openai.com/assistants)
2. Click "+ Create"
3. Choose "upload" and upload the file you generated

![Gif of how to upload to an assistant](https://github.com/BuilderIO/gpt-crawler/assets/844291/06e6ad36-e2ba-4c6e-8d5a-bf329140de49)