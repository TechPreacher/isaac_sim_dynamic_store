#!/usr/bin/env python3
"""
Test script to verify the randomization functionality
"""

import random
import math
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

def randomize_product_rotations(product_data_dict, num_products=3):
    """Test version of the randomization function."""
    randomized_data = product_data_dict.copy()
    product_ids = list(randomized_data.keys())
    selected_products = random.sample(product_ids, min(num_products, len(product_ids)))
    
    print(f"Randomizing rotations for products: {selected_products}")
    
    for product_id in selected_products:
        product_data = randomized_data[product_id].copy()
        
        if "rotate" in product_data or "orient" not in product_data:
            # Use Euler angles
            random_rotation = [
                random.uniform(-180, 180),
                random.uniform(-180, 180),
                random.uniform(-180, 180)
            ]
            product_data["rotate"] = random_rotation
            if "orient" in product_data:
                del product_data["orient"]
            print(f"  {product_id}: New rotation = {random_rotation}")
        else:
            # Generate random quaternion
            u1, u2, u3 = random.random(), random.random(), random.random()
            q1 = math.sqrt(1 - u1) * math.sin(2 * math.pi * u2)
            q2 = math.sqrt(1 - u1) * math.cos(2 * math.pi * u2)
            q3 = math.sqrt(u1) * math.sin(2 * math.pi * u3)
            q0 = math.sqrt(u1) * math.cos(2 * math.pi * u3)
            random_quat = [float(q0), float(q1), float(q2), float(q3)]
            
            product_data["orient"] = random_quat
            if "rotate" in product_data:
                del product_data["rotate"]
            print(f"  {product_id}: New orientation = {random_quat}")
        
        randomized_data[product_id] = product_data
        
    return randomized_data

def test_randomization_with_real_data():
    """Test randomization with real product data."""
    print("=== Testing randomization with real product data ===")
    
    product_data = load_product_data()
    if not product_data:
        print("❌ Failed to load product data")
        return
    
    print(f"Loaded {len(product_data)} products")
    
    # Show original rotations for first 3 products
    product_ids = list(product_data.keys())[:3]
    print("\nOriginal rotations for first 3 products:")
    for pid in product_ids:
        pdata = product_data[pid]
        if 'rotate' in pdata:
            print(f"  {pid}: rotate = {pdata['rotate']}")
        elif 'orient' in pdata:
            print(f"  {pid}: orient = {pdata['orient']}")
    
    # Apply randomization
    randomized_data = randomize_product_rotations(product_data, 3)
    
    print("\nAfter randomization:")
    for pid in product_ids:
        pdata = randomized_data[pid]
        if 'rotate' in pdata:
            print(f"  {pid}: rotate = {pdata['rotate']}")
        elif 'orient' in pdata:
            print(f"  {pid}: orient = {pdata['orient']}")

def test_randomization_simple():
    """Test randomization with simple sample data."""
    print("=== Testing randomization with sample data ===")
    
    # Sample product data
    test_data = {
        "product_1": {
            "asset": "test.usd",
            "translate": [1, 2, 3],
            "rotate": [90, 0, 0],
            "scale": [1, 1, 1]
        },
        "product_2": {
            "asset": "test2.usd", 
            "translate": [4, 5, 6],
            "orient": [1, 0, 0, 0],
            "scale": [1, 1, 1]
        },
        "product_3": {
            "asset": "test3.usd",
            "translate": [7, 8, 9],
            "rotate": [0, 90, 0],
            "scale": [1, 1, 1]
        }
    }
    
    print("Original data:")
    for pid, pdata in test_data.items():
        print(f"  {pid}: {pdata}")
    
    print("\nAfter randomization:")
    result = randomize_product_rotations(test_data, 2)
    for pid, pdata in result.items():
        print(f"  {pid}: {pdata}")

if __name__ == "__main__":
    test_randomization_simple()
    print("\n" + "="*60 + "\n")
    test_randomization_with_real_data()