"""
Dynamic Shop Product Placer for IsaacSim

This script loads the empty shop environment and dynamically places products
at their original positions extracted from the populated shop USD file.

Usage:
- Run this script in IsaacSim
- It will load the empty shop and populate it with products programmatically
"""

import omni.usd
from pxr import Usd, UsdGeom, Gf, UsdPhysics, PhysxSchema
import asyncio
import numpy as np
from pathlib import Path

BASE_PATH = "C:/Users/sascha/Code/Hackathon/Code/Dynamic_Shop/"

# Product data extracted from Shop Minimal.usda
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


class DynamicShopPlacer:
    """Main class for loading empty shop and placing products dynamically."""
    
    def __init__(self):
        self.stage = omni.usd.get_context().get_stage()
        base_file = Path(BASE_PATH) / "assets" / "Shop Minimal Empty.usda"
        self.empty_shop_path = str(base_file)
        
    def load_empty_shop_sync(self):
        """Synchronous version of load_empty_shop for easier testing."""
        print("Loading empty shop environment...")
        
        # Open the empty shop USD file
        success = omni.usd.get_context().open_stage(str(self.empty_shop_path))
        if not success:
            print(f"Failed to load empty shop from: {self.empty_shop_path}")
            return False
            
        self.stage = omni.usd.get_context().get_stage()
        print(f"Successfully loaded empty shop: {self.empty_shop_path}")
        return True
        
    async def load_empty_shop(self):
        """Load the empty shop USD file as the base environment."""
        print("Loading empty shop environment...")
        
        # Open the empty shop USD file
        success = await omni.usd.get_context().open_stage_async(str(self.empty_shop_path))
        if not success:
            print(f"Failed to load empty shop from: {self.empty_shop_path}")
            return False
            
        self.stage = omni.usd.get_context().get_stage()
        print(f"Successfully loaded empty shop: {self.empty_shop_path}")
        return True
        
    def create_product_hierarchy(self):
        """Create the product hierarchy structure in the stage."""
        # Create the main product containers
        shelf_prim = self.stage.GetPrimAtPath("/World/Shelf")
        if not shelf_prim:
            print("Warning: Could not find /World/Shelf in the loaded stage")
            return False
            
        # Create Items_Lower scope
        items_lower_path = "/World/Shelf/Items_Lower"
        items_lower = UsdGeom.Scope.Define(self.stage, items_lower_path)
        
        # Create product category scopes
        categories = {
            "MustardBottles": ["_06_mustard_bottle_05", "_06_mustard_bottle_06", "_06_mustard_bottle_08"],
            "Spam": ["_10_potted_meat_can_24", "_10_potted_meat_can_26", "_10_potted_meat_can_27"],
            "TunaCans": ["_07_tuna_fish_can_61", "_07_tuna_fish_can_62", "_07_tuna_fish_can_63", "_07_tuna_fish_can_64"],
            "Cleaner": ["_21_bleach_cleanser_03", "_21_bleach_cleanser_04", "_21_bleach_cleanser_06"]
        }
        
        # Create Items_Upper scope
        items_upper_path = "/World/Shelf/Items_Upper"
        items_upper = UsdGeom.Scope.Define(self.stage, items_upper_path)
        
        # Upper shelf categories
        upper_categories = {
            "Crackers": ["_03_cracker_box_03", "_03_cracker_box_04", "_03_cracker_box_05"],
            "TomatoCans": ["_05_tomato_soup_can_12", "_05_tomato_soup_can_13", "_05_tomato_soup_can_14"]
        }
        
        # Create category scopes for lower shelf
        for category, products in categories.items():
            category_path = f"{items_lower_path}/{category}"
            UsdGeom.Scope.Define(self.stage, category_path)
            
        # Create category scopes for upper shelf  
        for category, products in upper_categories.items():
            category_path = f"{items_upper_path}/{category}"
            UsdGeom.Scope.Define(self.stage, category_path)
            
        print("Created product hierarchy structure")
        return True
        
    def place_product(self, product_id, product_data):
        """Place a single product in the scene with proper transforms and physics."""
        # Determine the category and shelf level
        category_map = {
            "_06_mustard_bottle": ("Items_Lower", "MustardBottles"),
            "_10_potted_meat_can": ("Items_Lower", "Spam"),
            "_07_tuna_fish_can": ("Items_Lower", "TunaCans"),
            "_21_bleach_cleanser": ("Items_Lower", "Cleaner"),
            "_03_cracker_box": ("Items_Upper", "Crackers"),
            "_05_tomato_soup_can": ("Items_Upper", "TomatoCans")
        }
        
        # Find the category for this product
        product_category = None
        for prefix, (shelf_level, category) in category_map.items():
            if product_id.startswith(prefix):
                product_category = (shelf_level, category)
                break
                
        if not product_category:
            print(f"Warning: Could not determine category for product {product_id}")
            return False
            
        shelf_level, category = product_category
        product_path = f"/World/Shelf/{shelf_level}/{category}/{product_id}"
        
        # Create the product prim with payload reference
        product_prim = self.stage.DefinePrim(product_path)
        product_prim.GetPayloads().AddPayload(product_data["asset"])
        
        # Create Xform for transforms
        xform = UsdGeom.Xform(product_prim)
        
        # Clear any existing transform operations to avoid conflicts
        xform.ClearXformOpOrder()
        
        # Set transform operations - simply add them (since we cleared existing ops)
        translate_op = xform.AddTranslateOp()
        translate_op.Set(Gf.Vec3d(*product_data["translate"]))
        
        scale_op = xform.AddScaleOp()
        scale_op.Set(Gf.Vec3f(*product_data["scale"]))
        
        # Handle rotation - some products use rotateZYX, others use orient (quaternion)
        if "rotate" in product_data:
            # Use Euler rotation (ZYX order)
            rotation_op = xform.AddRotateZYXOp()
            rotation_op.Set(Gf.Vec3f(*product_data["rotate"]))
        elif "orient" in product_data:
            # Use quaternion orientation
            rotation_op = xform.AddOrientOp()
            quat_data = product_data["orient"]
            # Convert (w,x,y,z) to Gf.Quatf(w, Gf.Vec3f(x,y,z))
            rotation_op.Set(Gf.Quatf(quat_data[0], Gf.Vec3f(quat_data[1], quat_data[2], quat_data[3])))
            
        # Set transform order with the operations we have
        if rotation_op:
            xform.SetXformOpOrder([translate_op, rotation_op, scale_op])
        else:
            xform.SetXformOpOrder([translate_op, scale_op])
        
        # Add physics if enabled
        if product_data.get("physics_enabled", False):
            # Add RigidBody API
            rigid_body_api = UsdPhysics.RigidBodyAPI.Apply(product_prim)
            rigid_body_api.CreateRigidBodyEnabledAttr(True)
            rigid_body_api.CreateKinematicEnabledAttr(False)
            
            # Add Physx RigidBody API  
            physx_rb_api = PhysxSchema.PhysxRigidBodyAPI.Apply(product_prim)
            
            # Set initial velocities if provided
            if "velocity" in product_data:
                rigid_body_api.CreateVelocityAttr(Gf.Vec3f(*product_data["velocity"]))
            if "angular_velocity" in product_data:
                rigid_body_api.CreateAngularVelocityAttr(Gf.Vec3f(*product_data["angular_velocity"]))
                
        print(f"Placed product: {product_id} at {product_data['translate']}")
        return True
        
    def place_all_products(self):
        """Place all products from the product data."""
        print("Placing all products...")
        success_count = 0
        
        for product_id, product_data in PRODUCT_DATA.items():
            try:
                if self.place_product(product_id, product_data):
                    success_count += 1
                else:
                    print(f"Failed to place product: {product_id}")
            except Exception as e:
                print(f"Error placing product {product_id}: {str(e)}")
                
        print(f"Successfully placed {success_count} out of {len(PRODUCT_DATA)} products")
        return success_count > 0
        
    def setup_scene_sync(self):
        """Synchronous version of setup_scene for easier execution in Isaac Sim."""
        print("Starting dynamic shop setup...")
        
        # Load empty shop
        if not self.load_empty_shop_sync():
            print("Failed to load empty shop!")
            return False
            
        # Create product hierarchy
        if not self.create_product_hierarchy():
            print("Failed to create product hierarchy!")
            return False
            
        # Place all products
        if not self.place_all_products():
            print("Failed to place products!")
            return False
            
        print("Dynamic shop setup completed successfully!")
        return True
        
    async def setup_scene(self):
        """Main method to set up the complete scene."""
        print("Starting dynamic shop setup...")
        
        # Load empty shop
        if not await self.load_empty_shop():
            return False
            
        # Create product hierarchy
        if not self.create_product_hierarchy():
            return False
            
        # Place all products
        if not self.place_all_products():
            return False
            
        print("Dynamic shop setup completed successfully!")
        return True


# Main execution function
async def main():
    """Main function to run the dynamic shop placer."""
    placer = DynamicShopPlacer()
    await placer.setup_scene()


# Entry point for IsaacSim
if __name__ == "__main__":
    print("Dynamic Shop Product Placer")
    print("Loading empty shop and placing products dynamically...")
    
    # Create and run the placer synchronously (works better in Isaac Sim Script Editor)
    placer = DynamicShopPlacer()
    
    try:
        result = placer.setup_scene_sync()
        if result:
            print("✅ SUCCESS: Dynamic shop setup completed!")
            print("Check the viewport - products should now be visible on the shelves.")
        else:
            print("❌ FAILED: Dynamic shop setup encountered errors.")
            print("Check the console output above for details.")
    except Exception as e:
        print(f"❌ ERROR: Script execution failed: {str(e)}")
        print("This might be due to missing files or Isaac Sim API issues.")
        
    print("\nScript execution finished.")