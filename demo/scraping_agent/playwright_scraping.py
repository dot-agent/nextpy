import asyncio
import pprint

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright


def remove_unwanted_tags(html_content, unwanted_tags=["script", "style"])->str:
    """
    This removes unwanted HTML tags from the given HTML content.
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    for tag in unwanted_tags:
        for element in soup.find_all(tag):
            element.decompose()

    return str(soup)


def extract_tags(html_content, tags: list[str]):
    """
    This takes in HTML content and a list of tags, and returns a string
    containing the text content of all elements with those tags, along with their href attribute if the
    tag is an "a" tag.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    text_parts = []

    for tag in tags:
        elements = soup.find_all(tag)
        for element in elements:
            # If the tag is a link (a tag), append its href as well
            if tag == "a":
                href = element.get('href')
                if href:
                    text_parts.append(f"{element.get_text()} ({href})")
            else:
                text_parts.append(element.get_text())

    return ' '.join(text_parts)


def remove_unessesary_lines(content):
    
    lines = content.split("\n")

    
    stripped_lines = [line.strip() for line in lines]

    non_empty_lines = [line for line in stripped_lines if line]
    duplicate = set()
    deduped_lines = [line for line in non_empty_lines if not (
        line in duplicate or duplicate.add(line))]

    # Join the cleaned lines without any separators (remove newlines)
    cleaned_content = "".join(deduped_lines)

    return cleaned_content


async def ascrape_playwright(url, tags: list[str] = ["h1", "h2", "h3", "span"]) -> str:
    print("Started scraping...")
    results = ""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(url)

            page_source = await page.content()

            results = remove_unessesary_lines(extract_tags(remove_unwanted_tags(
                page_source), tags))
            print("Content scraped")
        except Exception as e:
            results = f"Error: {e}"
        await browser.close()
    return results


# TESTING
if __name__ == "__main__":
    url = "https://www.ajio.com/?gclid=CjwKCAjwyY6pBhA9EiwAMzmfwS1IKhxyxf03c67YvfdPiTzVgaNklXmSzWHS2ZO_gpMOtGH0cAIuCBoCDOAQAvD_BwE"

    async def scrape_playwright():
        results = await ascrape_playwright(url)
        print(results)

    pprint.pprint(asyncio.run(scrape_playwright()))