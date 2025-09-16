from typing import Optional, List
from pydantic import BaseModel, Field
from agents import Agent, Runner
from config import config


class ProductInfo(BaseModel):
    name: str                           # Text
    price: float                        # Decimal number
    in_stock: bool                      # True/False
    categories: List[str]               # List of text items
    #discount_percent: Optional[int] = Field(default=0) # Optional number, default 0
    reviews_count: int                  # Whole number

# Create product info extractor
agent = Agent(
    name="ProductExtractor",
    instructions="Extract product information from product descriptions.",
    output_type=ProductInfo
)

# Test with product description
result = Runner.run_sync(
    agent,
    "The iPhone 15 Pro costs $999.99, it's available in electronics and smartphones categories, currently in stock with 1,247 reviews .",
    run_config=config
)
print(ProductInfo.model_json_schema())
print("\n=== Product Info ===")
print("Product:", result.final_output.name)         # "iPhone 15 Pro"
print("Price:", result.final_output.price)          # 999.99
print("In Stock:", result.final_output.in_stock)    # True
print("Categories:", result.final_output.categories) # ["electronics", "smartphones"]
print("Reviews:", result.final_output.reviews_count) # 1247