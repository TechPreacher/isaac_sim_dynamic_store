#!/usr/bin/env python3
"""
Check the actual physics settings for all products by reading from JSON data
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

def analyze_physics_settings():
    """Analyze physics settings from the product data."""
    product_data = load_product_data()
    
    if not product_data:
        print("❌ Failed to load product data")
        return
    
    physics_enabled = []
    physics_disabled = []
    
    for product_name, data in product_data.items():
        if data.get("physics_enabled", False):
            physics_enabled.append(product_name)
        else:
            physics_disabled.append(product_name)
    
    print("=== PHYSICS ANALYSIS ===")
    print(f"\nPHYSICS ENABLED ({len(physics_enabled)} products):")
    for i, product in enumerate(physics_enabled, 1):
        print(f"{i:2d}. {product}")
    
    print(f"\nPHYSICS DISABLED - STATIC ({len(physics_disabled)} products):")
    for i, product in enumerate(physics_disabled, 1):
        print(f"{i:2d}. {product}")
    
    print(f"\nTOTAL: {len(physics_enabled)} physics + {len(physics_disabled)} static = {len(physics_enabled) + len(physics_disabled)} products")
    
    # Categorize by product type
    print("\n=== BY CATEGORY ===")
    categories = {
        'Mustard Bottles': [p for p in physics_disabled + physics_enabled if '_06_mustard_bottle' in p],
        'Spam Cans': [p for p in physics_disabled + physics_enabled if '_10_potted_meat_can' in p],
        'Tuna Cans': [p for p in physics_disabled + physics_enabled if '_07_tuna_fish_can' in p],
        'Cleaner': [p for p in physics_disabled + physics_enabled if '_21_bleach_cleanser' in p],
        'Cracker Boxes': [p for p in physics_disabled + physics_enabled if '_03_cracker_box' in p],
        'Tomato Soup Cans': [p for p in physics_disabled + physics_enabled if '_05_tomato_soup_can' in p],
        'Mugs': [p for p in physics_disabled + physics_enabled if '_25_mug' in p],
        'Mac-n-Cheese': [p for p in physics_disabled + physics_enabled if 'mac_n_cheese' in p]
    }
    
    for category, products in categories.items():
        if products:
            # Check if first product in category has physics
            first_product = products[0]
            has_physics = first_product in physics_enabled
            status = "Physics enabled" if has_physics else "Static (no physics)"
            print(f"{category:17s} ({len(products)} items): {status}")

if __name__ == "__main__":
    analyze_physics_settings()