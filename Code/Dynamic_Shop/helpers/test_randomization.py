#!/usr/bin/env python3
"""
Test script to verify the randomization functionality
"""

import random
import math

# Simulate the randomization logic without Isaac Sim dependencies
def test_randomization():
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
    
    print("Original data:")
    for pid, pdata in test_data.items():
        print(f"  {pid}: {pdata}")
    
    print("\nAfter randomization:")
    result = randomize_product_rotations(test_data, 2)
    for pid, pdata in result.items():
        print(f"  {pid}: {pdata}")

if __name__ == "__main__":
    test_randomization()