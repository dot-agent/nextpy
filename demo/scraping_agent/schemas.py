from pydantic import BaseModel

ecommerce_schema={
    "properties": {
        "product_title": {"type": "string"},
        "product_price": {
            "anyOf": [
                {"type": "number"},
                {"type": "string"}
            ]
        },
        "product_extra_info": {"type": "string"}
    },
    "required": ["product_title", "product_price", "product_extra_info"]
}



class SchemaNewsWebsites(BaseModel):
    news_headline: str
    news_short_summary: str