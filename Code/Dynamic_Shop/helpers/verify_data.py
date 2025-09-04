"""
Standalone Test and Verification for Dynamic Shop Placer

This version can run outside of IsaacSim to verify the product data and file structure.
Updated to use JSON product data.
"""

import json
import math
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

def verify_product_data_structure():
    """Verify the structure and content of product data."""
    print("=== PRODUCT DATA VERIFICATION ===")
    
    product_data = load_product_data()
    
    if not product_data:
        print("❌ Failed to load product data")
        return False
    
    print(f"✅ Loaded {len(product_data)} products from JSON")
    
    # Test each product entry
    issues = []
    physics_count = 0
    static_count = 0
    
    for product_id, data in product_data.items():
        # Required fields check
        required_fields = ["asset", "translate", "scale", "physics_enabled"]
        for field in required_fields:
            if field not in data:
                issues.append(f"{product_id}: Missing '{field}' field")
        
        # Rotation check (must have either rotate or orient)
        if "rotate" not in data and "orient" not in data:
            issues.append(f"{product_id}: Missing rotation data (neither 'rotate' nor 'orient')")
        
        # Data type checks
        if "translate" in data:
            if not isinstance(data["translate"], list) or len(data["translate"]) != 3:
                issues.append(f"{product_id}: 'translate' must be a list of 3 numbers")
        
        if "scale" in data:
            if not isinstance(data["scale"], list) or len(data["scale"]) != 3:
                issues.append(f"{product_id}: 'scale' must be a list of 3 numbers")
        
        if "rotate" in data:
            if not isinstance(data["rotate"], list) or len(data["rotate"]) != 3:
                issues.append(f"{product_id}: 'rotate' must be a list of 3 numbers")
        
        if "orient" in data:
            if not isinstance(data["orient"], list) or len(data["orient"]) != 4:
                issues.append(f"{product_id}: 'orient' must be a list of 4 numbers (quaternion)")
        
        # Count physics vs static
        if data.get("physics_enabled", False):
            physics_count += 1
        else:
            static_count += 1
    
    # Report issues
    if issues:
        print(f"❌ Found {len(issues)} data structure issues:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print("✅ All product data structure checks passed")
        print(f"  - Physics enabled: {physics_count} products")
        print(f"  - Static objects: {static_count} products")
        return True

def categorize_products():
    """Categorize products by type and location."""
    print("\n=== PRODUCT CATEGORIZATION ===")
    
    product_data = load_product_data()
    
    if not product_data:
        print("❌ Cannot categorize - failed to load product data")
        return
    
    # Category definitions
    categories = {
        'Mustard Bottles': [],
        'Spam Cans': [],
        'Tuna Cans': [],
        'Bleach Cleanser': [],
        'Cracker Boxes': [],
        'Tomato Soup Cans': [],
        'Mugs': [],
        'Mac-n-Cheese': []
    }
    
    # Categorize each product
    for product_id, data in product_data.items():
        if '_06_mustard_bottle' in product_id:
            categories['Mustard Bottles'].append(product_id)
        elif '_10_potted_meat_can' in product_id:
            categories['Spam Cans'].append(product_id)
        elif '_07_tuna_fish_can' in product_id:
            categories['Tuna Cans'].append(product_id)
        elif '_21_bleach_cleanser' in product_id:
            categories['Bleach Cleanser'].append(product_id)
        elif '_03_cracker_box' in product_id:
            categories['Cracker Boxes'].append(product_id)
        elif '_05_tomato_soup_can' in product_id:
            categories['Tomato Soup Cans'].append(product_id)
        elif '_25_mug' in product_id:
            categories['Mugs'].append(product_id)
        elif 'mac_n_cheese' in product_id:
            categories['Mac-n-Cheese'].append(product_id)
    
    # Print categorization
    total_categorized = 0
    for category, products in categories.items():
        if products:
            # Check shelf level based on Z coordinate (height)
            sample_product = products[0]
            z_coord = product_data[sample_product]['translate'][2]
            shelf_level = "Upper" if z_coord > 1.5 else "Lower"
            
            # Check physics
            sample_data = product_data[sample_product]
            physics_status = "Physics" if sample_data.get('physics_enabled', False) else "Static"
            
            print(f"{category:20s}: {len(products)} items - {shelf_level} shelf - {physics_status}")
            total_categorized += len(products)
    
    print(f"\nTotal products categorized: {total_categorized}")

def validate_positions():
    """Validate product positions are reasonable for the shop environment."""
    print("\n=== POSITION VALIDATION ===")
    
    product_data = load_product_data()
    
    if not product_data:
        print("❌ Cannot validate positions - failed to load product data")
        return
    
    # Expected shop bounds (based on shop model)
    expected_bounds = {
        'x': (-26, -24),  # Shelf depth (front to back)
        'y': (44, 48),    # Shelf length (side to side)
        'z': (0.8, 2.2)   # Shelf height (bottom to top)
    }
    
    out_of_bounds = []
    lower_shelf_items = []
    upper_shelf_items = []
    
    for product_id, data in product_data.items():
        x, y, z = data['translate']
        
        # Check bounds
        if not (expected_bounds['x'][0] <= x <= expected_bounds['x'][1]):
            out_of_bounds.append(f"{product_id}: X={x:.2f} out of range {expected_bounds['x']}")
        if not (expected_bounds['y'][0] <= y <= expected_bounds['y'][1]):
            out_of_bounds.append(f"{product_id}: Y={y:.2f} out of range {expected_bounds['y']}")
        if not (expected_bounds['z'][0] <= z <= expected_bounds['z'][1]):
            out_of_bounds.append(f"{product_id}: Z={z:.2f} out of range {expected_bounds['z']}")
        
        # Categorize by shelf level
        if z < 1.5:  # Lower shelf threshold
            lower_shelf_items.append(product_id)
        else:
            upper_shelf_items.append(product_id)
    
    if out_of_bounds:
        print(f"❌ Found {len(out_of_bounds)} position issues:")
        for issue in out_of_bounds:
            print(f"  - {issue}")
    else:
        print("✅ All product positions are within expected shop bounds")
    
    print(f"  - Lower shelf items: {len(lower_shelf_items)}")
    print(f"  - Upper shelf items: {len(upper_shelf_items)}")

def check_assets():
    """Check asset URL validity (basic format check)."""
    print("\n=== ASSET URL VALIDATION ===")
    
    product_data = load_product_data()
    
    if not product_data:
        print("❌ Cannot validate assets - failed to load product data")
        return
    
    valid_base_url = "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/"
    invalid_assets = []
    asset_types = {}
    
    for product_id, data in product_data.items():
        asset_url = data.get('asset', '')
        
        # Check URL format
        if not asset_url.startswith(valid_base_url):
            invalid_assets.append(f"{product_id}: Invalid base URL")
        elif not asset_url.endswith('.usd'):
            invalid_assets.append(f"{product_id}: Not a USD file")
        
        # Count asset types
        if 'YCB' in asset_url:
            if 'Physics' in asset_url:
                asset_type = 'YCB Physics'
            else:
                asset_type = 'YCB Standard'
        elif 'Food' in asset_url:
            asset_type = 'Food'
        else:
            asset_type = 'Other'
        
        asset_types[asset_type] = asset_types.get(asset_type, 0) + 1
    
    if invalid_assets:
        print(f"❌ Found {len(invalid_assets)} asset issues:")
        for issue in invalid_assets:
            print(f"  - {issue}")
    else:
        print("✅ All asset URLs have valid format")
    
    print("Asset type distribution:")
    for asset_type, count in asset_types.items():
        print(f"  - {asset_type}: {count} products")

def run_all_verifications():
    """Run all verification tests."""
    print("🔍 DYNAMIC SHOP PLACER - DATA VERIFICATION")
    print("=" * 50)
    
    # Run all verification functions
    structure_ok = verify_product_data_structure()
    categorize_products()
    validate_positions()
    check_assets()
    
    print("\n" + "=" * 50)
    if structure_ok:
        print("🎉 VERIFICATION COMPLETED - Data structure is valid!")
        print("\nThe product data is ready for use with the Dynamic Shop Placer.")
    else:
        print("⚠️  VERIFICATION ISSUES FOUND - Please fix data structure problems")
    
    print(f"\nTotal products verified: {len(load_product_data())}")

if __name__ == "__main__":
    run_all_verifications()