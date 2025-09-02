#!/usr/bin/env python3
"""
Quick product count verification script
"""

import re

def count_products_in_file():
    with open('dynamic_shop_placer.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all product entries in PRODUCT_DATA
    product_pattern = r'"([^"]+)":\s*{'
    matches = re.findall(product_pattern, content)
    
    # Filter to only get the actual product IDs (not other dictionary keys)
    products = [m for m in matches if not m.startswith('asset') and not m.startswith('translate') and not m.startswith('orient') and not m.startswith('rotate') and not m.startswith('scale') and not m.startswith('physics')]
    
    print(f"Total products found: {len(products)}")
    print("\nAll products:")
    for i, product in enumerate(products, 1):
        print(f"{i:2d}. {product}")
    
    # Count new products
    new_products = [p for p in products if '_25_mug' in p or 'mac_n_cheese' in p]
    print(f"\nNew products added ({len(new_products)}):")
    for product in new_products:
        print(f"- {product}")

if __name__ == "__main__":
    count_products_in_file()