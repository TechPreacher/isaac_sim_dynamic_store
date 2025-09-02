"""
Test Runner and Usage Instructions for Dynamic Shop Placer

This script provides instructions and test functionality for the dynamic shop placer.
"""

# Usage Instructions:
"""
HOW TO USE THE DYNAMIC SHOP PLACER IN ISAAC SIM:

1. SETUP:
   - Make sure IsaacSim is installed and running
   - Ensure the USD files are in the ./assets/ directory:
     * Shop Minimal Empty.usda (empty shop environment)
     * Shop Minimal.usda (populated shop - for reference)

2. RUNNING THE SCRIPT:
   - Open IsaacSim
   - Load the dynamic_shop_placer.py script
   - Execute the script in IsaacSim's Script Editor or Python console
   
   OR
   
   - Run from command line: python dynamic_shop_placer.py (if IsaacSim Python environment is configured)

3. WHAT THE SCRIPT DOES:
   - Loads the empty shop USD file (Shop Minimal Empty.usda)
   - Creates the product hierarchy (Items_Lower/Items_Upper with categories)
   - Places 18 products with exact transforms from the original shop:
     * 3 Mustard Bottles (lower shelf)
     * 3 Spam Cans (lower shelf, with physics)
     * 4 Tuna Cans (lower shelf, with physics)
     * 3 Bleach Cleanser bottles (lower shelf, with physics + velocities)
     * 3 Cracker Boxes (upper shelf)
     * 3 Tomato Soup Cans (upper shelf)

4. PRODUCT CATEGORIES AND LOCATIONS:
   - Lower Shelf (/World/Shelf/Items_Lower/):
     * MustardBottles/ - 3 mustard bottles
     * Spam/ - 3 spam cans with physics
     * TunaCans/ - 4 tuna cans with physics
     * Cleaner/ - 3 bleach bottles with physics and motion
   
   - Upper Shelf (/World/Shelf/Items_Upper/):
     * Crackers/ - 3 cracker boxes
     * TomatoCans/ - 3 tomato soup cans

5. PHYSICS PROPERTIES:
   - Some products have rigid body physics enabled
   - Physics-enabled products have collision detection
   - Some products have initial velocities and angular velocities
   - Physics approximation set to "convexHull" for realistic behavior

6. ASSET SOURCES:
   - All products use YCB (Yale-CMU-Berkeley) dataset assets
   - Assets are loaded from Omniverse content servers
   - URLs point to official Isaac Sim asset library

7. COORDINATE SYSTEM:
   - Uses original USD coordinate system
   - Products placed at exact positions from populated shop
   - Shelf coordinate system: X=-25 (shelf front), Y=44-48 (shelf length), Z=0.8-2.1 (shelf height)

8. TROUBLESHOOTING:
   - If assets don't load, check internet connection (external URLs)
   - If shop doesn't load, verify ./assets/Shop Minimal Empty.usda exists
   - If products appear in wrong locations, check coordinate system alignment
   - If physics doesn't work, ensure IsaacSim physics is enabled

9. CUSTOMIZATION:
   - Modify PRODUCT_DATA dictionary to add/remove/move products
   - Change asset URLs to use different products
   - Adjust physics properties per product
   - Modify hierarchy structure in create_product_hierarchy()

10. EXPECTED OUTPUT:
    - Console messages showing loading progress
    - Empty shop environment loaded as base
    - Products appearing at shelf locations with proper orientations
    - Physics-enabled products responding to gravity and collisions
"""

# Test function to verify script components
def test_product_data_integrity():
    """Test function to verify product data is properly structured."""
    from dynamic_shop_placer import PRODUCT_DATA
    
    print("Testing product data integrity...")
    
    required_fields = ["asset", "translate", "scale"]
    physics_fields = ["physics_enabled"]
    rotation_fields = ["rotate", "orient"]  # One of these must be present
    
    issues = []
    
    for product_id, data in PRODUCT_DATA.items():
        # Check required fields
        for field in required_fields:
            if field not in data:
                issues.append(f"{product_id}: Missing required field '{field}'")
                
        # Check rotation field (either rotate or orient)
        has_rotation = any(field in data for field in rotation_fields)
        if not has_rotation:
            issues.append(f"{product_id}: Missing rotation information (rotate or orient)")
            
        # Validate transform data types
        if "translate" in data and len(data["translate"]) != 3:
            issues.append(f"{product_id}: translate must have 3 values")
            
        if "scale" in data and len(data["scale"]) != 3:
            issues.append(f"{product_id}: scale must have 3 values")
            
        if "rotate" in data and len(data["rotate"]) != 3:
            issues.append(f"{product_id}: rotate must have 3 values (ZYX)")
            
        if "orient" in data and len(data["orient"]) != 4:
            issues.append(f"{product_id}: orient must have 4 values (quaternion)")
    
    if issues:
        print("❌ Product data integrity test FAILED:")
        for issue in issues:
            print(f"  - {issue}")
        return False
    else:
        print(f"✅ Product data integrity test PASSED - {len(PRODUCT_DATA)} products validated")
        return True

def print_product_summary():
    """Print a summary of all products that will be placed."""
    from dynamic_shop_placer import PRODUCT_DATA
    
    print("\n=== PRODUCT PLACEMENT SUMMARY ===")
    
    # Categorize products
    categories = {}
    for product_id, data in PRODUCT_DATA.items():
        # Determine category from product ID
        if "_06_mustard_bottle" in product_id:
            category = "Mustard Bottles (Lower)"
        elif "_10_potted_meat_can" in product_id:
            category = "Spam Cans (Lower)"
        elif "_07_tuna_fish_can" in product_id:
            category = "Tuna Cans (Lower)"
        elif "_21_bleach_cleanser" in product_id:
            category = "Bleach Cleanser (Lower)"
        elif "_03_cracker_box" in product_id:
            category = "Cracker Boxes (Upper)"
        elif "_05_tomato_soup_can" in product_id:
            category = "Tomato Soup Cans (Upper)"
        else:
            category = "Other"
            
        if category not in categories:
            categories[category] = []
        categories[category].append((product_id, data))
    
    # Print category summaries
    total_products = 0
    physics_enabled = 0
    
    for category, products in categories.items():
        print(f"\n{category}: {len(products)} items")
        for product_id, data in products:
            physics_status = "🔵 Physics" if data.get("physics_enabled", False) else "⚪ Static"
            position = f"({data['translate'][0]:.1f}, {data['translate'][1]:.1f}, {data['translate'][2]:.1f})"
            print(f"  - {product_id}: {position} {physics_status}")
            
            total_products += 1
            if data.get("physics_enabled", False):
                physics_enabled += 1
    
    print(f"\n📊 TOTALS:")
    print(f"  Total Products: {total_products}")
    print(f"  Physics-Enabled: {physics_enabled}")
    print(f"  Static Objects: {total_products - physics_enabled}")

def check_file_structure():
    """Check if required files exist."""
    import os
    
    print("\n=== FILE STRUCTURE CHECK ===")
    
    required_files = [
        "./assets/Shop Minimal Empty.usda",
        "dynamic_shop_placer.py"
    ]
    
    optional_files = [
        "./assets/Shop Minimal.usda",
        "./assets/product_data.txt"
    ]
    
    all_good = True
    
    print("Required files:")
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ {file_path} - MISSING!")
            all_good = False
    
    print("\nOptional files (for reference):")
    for file_path in optional_files:
        if os.path.exists(file_path):
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❓ {file_path} - not found")
    
    return all_good

# Main test runner
if __name__ == "__main__":
    print("🧪 DYNAMIC SHOP PLACER - TEST & VERIFICATION")
    print("=" * 50)
    
    # Run tests
    file_check = check_file_structure()
    data_check = test_product_data_integrity()
    
    # Print summary
    print_product_summary()
    
    print("\n" + "=" * 50)
    if file_check and data_check:
        print("🎉 ALL TESTS PASSED - Ready to run in IsaacSim!")
        print("\nTo run the placer:")
        print("1. Open IsaacSim")
        print("2. Load and execute dynamic_shop_placer.py")
        print("3. Watch as products are placed dynamically!")
    else:
        print("⚠️  SOME TESTS FAILED - Please fix issues before running")
    
    print("\nFor detailed usage instructions, see the docstring at the top of this file.")