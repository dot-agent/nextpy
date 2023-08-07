from serpapi import GoogleSearch
from .config import Config
import logging

serpapi_key = Config.get_serpapi_key()

def get_product(product_keyword):
    params = {
        "api_key": serpapi_key,
        "engine": "google_shopping",
        "google_domain": "google.com",
        "q": product_keyword,
        "hl": "en",
        "gl": "us",
        "location": "United States",
        "tbs": "mr:1,price:1,ppr_max:150,merchagg:g113872638|m114193152|m7388148",
        "num": "2"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    logging.info(results)

    # Return the shopping results for this product
    out = results.get('shopping_results', [])
    logging.info(out)

    return out

