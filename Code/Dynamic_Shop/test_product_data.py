"""
Test script to verify the product data JSON loading functionality
without Isaac Sim dependencies.
"""

import json
from pathlib import Path

BASE_PATH = "C:/Users/sascha/Code/Hackathon/Code/Dynamic_Shop/"

def load_product_data():
    """Load product data from JSON file."""
    json_file_path = Path(BASE_PATH) / "assets" / "product_data.json"
    try:
        with open(json_file_path, 'r') as f:
            product_data = json.load(f)
        print(f"Loaded product data from: {json_file_path}")
        return product_data
    except FileNotFoundError:
        print(f"ERROR: Product data file not found at: {json_file_path}")
        return {}
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in product data file: {e}")
        return {}
    except Exception as e:
        print(f"ERROR: Failed to load product data: {e}")
        return {}

def test_product_data():
    """Test the product data loading and structure."""
    print("Testing product data loading...")
    
    data = load_product_data()
    
    if not data:
        print("❌ Failed to load product data")
        return False
    
    print(f"✅ Successfully loaded {len(data)} products")
    
    # Test data structure
    sample_product = list(data.keys())[0]
    sample_data = data[sample_product]
    
    print(f"\n🔍 Sample product: {sample_product}")
    print(f"  Asset: {sample_data.get('asset', 'N/A')}")
    print(f"  Translate: {sample_data.get('translate', 'N/A')}")
    print(f"  Scale: {sample_data.get('scale', 'N/A')}")
    print(f"  Physics enabled: {sample_data.get('physics_enabled', 'N/A')}")
    
    # Check if rotation or orient is present
    if 'rotate' in sample_data:
        print(f"  Rotation: {sample_data['rotate']}")
    elif 'orient' in sample_data:
        print(f"  Orientation: {sample_data['orient']}")
    
    # Verify all required fields are present for all products
    required_fields = ['asset', 'translate', 'scale', 'physics_enabled']
    missing_fields = []
    
    for product_id, product_data in data.items():
        for field in required_fields:
            if field not in product_data:
                missing_fields.append(f"{product_id}.{field}")
    
    if missing_fields:
        print(f"❌ Missing required fields: {missing_fields}")
        return False
    else:
        print("✅ All products have required fields")
    
    # Count products by type
    categories = {}
    for product_id in data.keys():
        if product_id.startswith('_06_mustard_bottle'):
            categories['Mustard Bottles'] = categories.get('Mustard Bottles', 0) + 1
        elif product_id.startswith('_10_potted_meat_can'):
            categories['Spam Cans'] = categories.get('Spam Cans', 0) + 1
        elif product_id.startswith('_07_tuna_fish_can'):
            categories['Tuna Cans'] = categories.get('Tuna Cans', 0) + 1
        elif product_id.startswith('_21_bleach_cleanser'):
            categories['Bleach Cleanser'] = categories.get('Bleach Cleanser', 0) + 1
        elif product_id.startswith('_03_cracker_box'):
            categories['Cracker Boxes'] = categories.get('Cracker Boxes', 0) + 1
        elif product_id.startswith('_05_tomato_soup_can'):
            categories['Tomato Soup Cans'] = categories.get('Tomato Soup Cans', 0) + 1
        elif product_id.startswith('_25_mug'):
            categories['Mugs'] = categories.get('Mugs', 0) + 1
        elif product_id.startswith('mac_n_cheese'):
            categories['Mac n Cheese'] = categories.get('Mac n Cheese', 0) + 1
    
    print(f"\n📊 Product categories:")
    for category, count in categories.items():
        print(f"  {category}: {count}")
    
    print(f"\n✅ Product data structure test completed successfully!")
    return True

if __name__ == "__main__":
    test_product_data()