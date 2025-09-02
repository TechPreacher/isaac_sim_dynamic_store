#!/usr/bin/env python3
"""
Check the actual physics settings for all products
"""

import re
import os

def analyze_physics_settings():
    # Find the dynamic_shop_placer.py file relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    placer_file = os.path.join(parent_dir, 'dynamic_shop_placer.py')
    
    try:
        with open(placer_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: Could not find dynamic_shop_placer.py at {placer_file}")
        print("Make sure this script is in the helpers/ subdirectory of the project")
        return
    
    # Extract all product entries with their physics settings
    pattern = r'"([^"]+)":\s*{[^}]*"physics_enabled":\s*(True|False)[^}]*}'
    matches = re.findall(pattern, content, re.DOTALL)
    
    physics_enabled = []
    physics_disabled = []
    
    for product_name, setting in matches:
        if setting == 'True':
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