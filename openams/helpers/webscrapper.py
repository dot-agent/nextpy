from typing import Type, Optional
from pydantic import BaseModel, Field
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import requests
import random


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    #... Rest of the user agents...
]

class WebScraperSchema(BaseModel):
    website_url: str = Field(
        ...,
        description="Valid website url without any quotes.",
    )

class WebScraperTool(BaseTool):
    """
    Web Scraper tool

    Attributes:
        name : The name.
        description : The description.
        args_schema : The args schema.
    """
    name = "WebScraperTool"
    description = (
        "Used to scrape website urls and extract text content"
    )
    args_schema: Type[WebScraperSchema] = WebScraperSchema

    def run(self, tool_input: str, **kwargs: Any) -> Any:
        """
        Execute the Web Scraper tool.

        Args:
            tool_input : The website url to scrape.

        Returns:
            The text content of the website.
        """
        content = self.extract_with_bs4(tool_input)
        max_length = len(' '.join(content.split(" ")[:600]))
        return content[:max_length]

    def extract_with_bs4(self, url):
        headers = {
            "User-Agent": random.choice(USER_AGENTS)
        }
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                for tag in soup(['script', 'style', 'nav', 'footer', 'head', 'link', 'meta', 'noscript']):
                    tag.decompose()

                main_content_areas = soup.find_all(['main', 'article', 'section', 'div'])
                if main_content_areas:
                    main_content = max(main_content_areas, key=lambda x: len(x.text))
                    content_tags = ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']
                    content = ' '.join([tag.text.strip() for tag in main_content.find_all(content_tags)])
                else:
                    content = ' '.join([tag.text.strip() for tag in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'])])

                content = re.sub(r'\t', ' ', content)
                content = re.sub(r'\s+', ' ', content)
                return content
            elif response.status_code == 404:
                return f"Error: 404. Url is invalid or does not exist. Try with valid url..."
            else:
                logger.error(f"Error while extracting text from HTML (bs4): {response.status_code}")
                return f"Error while extracting text from HTML (bs4): {response.status_code}"

        except Exception as e:
            logger.error(f"Unknown error while extracting text from HTML (bs4): {str(e)}")
            return ""
