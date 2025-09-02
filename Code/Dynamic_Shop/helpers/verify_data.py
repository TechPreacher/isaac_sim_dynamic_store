"""
Standalone Test and Verification for Dynamic Shop Placer

This version can run outside of IsaacSim to verify the product data and file structure.
"""

# Product data extracted from Shop Minimal.usda (copy from main script for testing)
PRODUCT_DATA = {
    # Mustard Bottles
    "_06_mustard_bottle_05": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/006_mustard_bottle.usd",
        "translate": (-25.086469880134647, 46.04343291587653, 0.9831003337342358),
        "rotate": (-90, 90, 0),  # rotateZYX
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False  # No physics properties in original
    },
    "_06_mustard_bottle_06": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/006_mustard_bottle.usd",
        "translate": (-25.097005175579373, 46.236204296072046, 0.9831003337342274),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    },
    "_06_mustard_bottle_08": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/006_mustard_bottle.usd",
        "translate": (-25.108974151148644, 46.43321083479538, 0.9831003337342358),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    },
    
    # Spam Cans
    "_10_potted_meat_can_24": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/010_potted_meat_can.usd",
        "translate": (-25.049380299928515, 44.521806528176384, 0.9167479613211755),
        "orient": (0.5, -0.5, 0.5, -0.5),  # quaternion
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True
    },
    "_10_potted_meat_can_26": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/010_potted_meat_can.usd",
        "translate": (-25.04938029992852, 44.341230940568934, 0.9167479613212102),
        "orient": (0.5, -0.5, 0.5, -0.5),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True
    },
    "_10_potted_meat_can_27": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/010_potted_meat_can.usd",
        "translate": (-25.04938029992852, 44.700208761938356, 0.9167479613211815),
        "orient": (0.5, -0.5, 0.5, -0.5),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True
    },
    
    # Tuna Cans
    "_07_tuna_fish_can_61": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/007_tuna_fish_can.usd",
        "translate": (-25.10408201181237, 45.12872643158456, 0.8812623099010872),
        "orient": (0.5, -0.5, 0.5, -0.5),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True
    },
    "_07_tuna_fish_can_62": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/007_tuna_fish_can.usd",
        "translate": (-25.108974151148644, 45.28407841269332, 0.8812623033304866),
        "orient": (0.5, -0.5, 0.5, -0.5),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True
    },
    "_07_tuna_fish_can_63": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/007_tuna_fish_can.usd",
        "translate": (-25.10408201181237, 45.428384443723154, 0.8812623099011412),
        "orient": (0.5, -0.5, 0.5, -0.5),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True
    },
    "_07_tuna_fish_can_64": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/007_tuna_fish_can.usd",
        "translate": (-25.108974151148644, 45.57446350380658, 0.8812623033304906),
        "orient": (0.5, -0.5, 0.5, -0.5),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True
    },
    
    # Bleach Cleanser
    "_21_bleach_cleanser_03": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/021_bleach_cleanser.usd",
        "translate": (-25.0994007709961, 47.132883414317945, 1.0243693192799825),
        "orient": (0.49827352, -0.50172055, 0.49827352, -0.50172055),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True,
        "angular_velocity": (1.8195142, -1.942818, 0.1757693),
        "velocity": (-0.004141945, -0.0037015579, -0.0014265937)
    },
    "_21_bleach_cleanser_04": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/021_bleach_cleanser.usd",
        "translate": (-25.102817119518022, 46.940442813463704, 1.0243617693582936),
        "orient": (0.49721286, -0.5027717, 0.49721286, -0.5027717),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True,
        "angular_velocity": (-2.702913, -3.8973846, 0.16748588),
        "velocity": (-0.007810059, 0.004482531, -0.0011357713)
    },
    "_21_bleach_cleanser_06": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned/021_bleach_cleanser.usd",
        "translate": (-25.10048221339459, 47.33321083479538, 1.024369557698539),
        "orient": (0.49827352, -0.50172055, 0.49827352, -0.50172055),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": True,
        "angular_velocity": (1.8075716, -1.9553645, 0.17668894),
        "velocity": (-0.004166908, -0.0036812094, -0.0014256913)
    },
    
    # Cracker Boxes (Upper shelf items)
    "_03_cracker_box_03": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/003_cracker_box.usd",
        "translate": (-25.089131422445735, 44.480783161966876, 2.061636572559885),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    },
    "_03_cracker_box_04": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/003_cracker_box.usd",
        "translate": (-25.089131422445707, 44.73967814589616, 2.061636572559931),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    },
    "_03_cracker_box_05": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/003_cracker_box.usd",
        "translate": (-25.08913142244565, 44.999162018393456, 2.061636572559899),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    },
    
    # Tomato Soup Cans
    "_05_tomato_soup_can_12": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/005_tomato_soup_can.usd",
        "translate": (-25.13039479318357, 45.496833812098515, 1.9914948821441776),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    },
    "_05_tomato_soup_can_13": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/005_tomato_soup_can.usd",
        "translate": (-25.137969118012506, 45.659482863260706, 1.9878743145899174),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    },
    "_05_tomato_soup_can_14": {
        "asset": "https://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.5/Isaac/Props/YCB/Axis_Aligned_Physics/005_tomato_soup_can.usd",
        "translate": (-25.145552442841443, 45.82212915452936, 1.9842537470356572),
        "rotate": (-90, 90, 0),
        "scale": (1.3333334, 1.3333334, 1.3333334),
        "physics_enabled": False
    }
}


# Test function to verify script components
def test_product_data_integrity():
    """Test function to verify product data is properly structured."""
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
    print("🧪 DYNAMIC SHOP PLACER - STANDALONE VERIFICATION")
    print("=" * 55)
    
    # Run tests
    file_check = check_file_structure()
    data_check = test_product_data_integrity()
    
    # Print summary
    print_product_summary()
    
    print("\n" + "=" * 55)
    if file_check and data_check:
        print("🎉 ALL TESTS PASSED - Ready to run in IsaacSim!")
        print("\nTo run the placer in IsaacSim:")
        print("1. Open IsaacSim")
        print("2. Load and execute 'dynamic_shop_placer.py'")
        print("3. Watch as products are placed dynamically!")
        print("\nThe script will:")
        print("- Load the empty shop environment")
        print("- Create organized product hierarchy")
        print("- Place 18 products with exact transforms")
        print("- Enable physics for 10 products")
        print("- Set initial velocities for moving objects")
    else:
        print("⚠️  SOME TESTS FAILED - Please fix issues before running")
    
    print(f"\nFor detailed usage instructions, see 'test_and_usage.py'")