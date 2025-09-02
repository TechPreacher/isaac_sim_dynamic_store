#!/usr/bin/env python3
"""
Simple test to verify JSON loading functionality
"""

import json
import os

def test_json_loading():
    """Test the JSON loading functionality."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)  # Go up one level from helpers/
    json_file = os.path.join(parent_dir, "product_data.json")
    
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            product_data = json.load(f)
        
        print(f"✅ Successfully loaded {len(product_data)} products from product_data.json")
        
        # Test a few sample products
        sample_products = list(product_data.keys())[:3]
        print(f"\nSample products:")
        for i, product_id in enumerate(sample_products, 1):
            data = product_data[product_id]
            print(f"  {i}. {product_id}")
            print(f"     Asset: {data['asset'].split('/')[-1]}")
            print(f"     Position: {data['translate']}")
            print(f"     Physics: {data['physics_enabled']}")
            if 'description' in data:
                print(f"     Description: {data['description']}")
            print()
        
        # Verify data types
        sample_data = product_data[sample_products[0]]
        print("✅ Data type validation:")
        print(f"  translate: {type(sample_data['translate'])} -> {sample_data['translate']}")
        print(f"  scale: {type(sample_data['scale'])} -> {sample_data['scale']}")
        print(f"  physics_enabled: {type(sample_data['physics_enabled'])} -> {sample_data['physics_enabled']}")
        
        # Test coordinate unpacking (this is what the main script does)
        translate = sample_data['translate']
        scale = sample_data['scale']
        print(f"✅ Unpacking test: translate(*{translate}) = {translate[0]}, {translate[1]}, {translate[2]}")
        print(f"✅ Unpacking test: scale(*{scale}) = {scale[0]}, {scale[1]}, {scale[2]}")
        
        return True
        
    except FileNotFoundError:
        print(f"❌ Error: Could not find product_data.json at {json_file}")
        return False
    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON in product_data.json: {e}")
        return False
    except Exception as e:
        print(f"❌ Error loading product data: {e}")
        return False

if __name__ == "__main__":
    success = test_json_loading()
    if success:
        print("\n🎯 JSON loading test PASSED - Ready for use in Isaac Sim!")
    else:
        print("\n❌ JSON loading test FAILED")