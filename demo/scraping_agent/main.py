import asyncio
import pprint

from llm_parser import extract
from schemas import SchemaNewsWebsites, ecommerce_schema
from playwright_scraping import ascrape_playwright


if __name__ == "__main__":
    token_limit = 4000

    
    cnn_url = "https://www.cnn.com"
    wsj_url = "https://www.wsj.com"
    nyt_url = "https://www.nytimes.com/ca/"

    ajio_url = "https://www.ajio.com"

    async def scrape_with_playwright(url: str, tags, **kwargs):
        html_content = await ascrape_playwright(url, tags)

        print("Extracting content with LLM")

        html_content_fits_context_window_llm = html_content[:token_limit]

        extracted_content = extract(**kwargs,
                                    content=html_content_fits_context_window_llm)

        pprint.pprint(extracted_content)

    # Scrape and Extract with LLM
    asyncio.run(scrape_with_playwright(
        url=ajio_url,
        tags=["span"],
        schema=ecommerce_schema
    ))