#!/usr/bin/env python3
"""
Quick product count verification script - now reads from JSON data
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to access main project files
sys.path.append(str(Path(__file__).parent.parent))

# Base path is now the parent directory
BASE_PATH = Path(__file__).parent.parent

def load_product_data():
    """Load product data from JSON file."""
    json_file_path = BASE_PATH / "assets" / "product_data.json"
    try:
        with open(json_file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"ERROR: Failed to load product data: {e}")
        return {}

def count_products_in_file():
    """Count products in the JSON data."""
    product_data = load_product_data()
    
    if not product_data:
        print("❌ Failed to load product data")
        return
    
    products = list(product_data.keys())
    
    print(f"Total products found: {len(products)}")
    print("\nAll products:")
    for i, product in enumerate(products, 1):
        print(f"{i:2d}. {product}")
    
    # Count new products (mugs and mac-n-cheese)
    new_products = [p for p in products if '_25_mug' in p or 'mac_n_cheese' in p]
    print(f"\nNew products added ({len(new_products)}):")
    for product in new_products:
        print(f"- {product}")

if __name__ == "__main__":
    count_products_in_file()