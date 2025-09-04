"""
Dynamic Shop Product Placer for IsaacSim

This script loads the empty shop environment and dynamically places products
at their original positions extracted from the populated shop USD file.

Features:
- Places 25 products from 8 categories across upper and lower shelves
- Automatically randomizes rotation of 3 random products for variety
- Supports both Euler angles and quaternion rotations
- Enables physics simulation for realistic behavior

Usage:
- Run this script in IsaacSim
- It will load the empty shop and populate it with products programmatically
"""

import omni.usd
from pxr import Usd, UsdGeom, Gf, UsdPhysics, PhysxSchema
import asyncio
import numpy as np
import random
import math
import json
from pathlib import Path

BASE_PATH = "C:/Users/sascha/Code/Hackathon/Code/Dynamic_Shop/"

# Configuration
ENABLE_PHYSICS_FOR_ALL = True  # Set to False to make all products static (no physics)
FORCE_COLLISION_FOR_PHYSICS = True  # Ensure collision detection for physics-enabled products

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

# Load product data from JSON file
PRODUCT_DATA = load_product_data()


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
            "_05_tomato_soup_can": ("Items_Upper", "TomatoCans"),
            "_25_mug": ("Items_Upper", "Mugs"),
            "mac_n_cheese": ("Items_Upper", "Mac_n_Cheese")
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
            # Convert [w,x,y,z] to Gf.Quatf(w, Gf.Vec3f(x,y,z))
            rotation_op.Set(Gf.Quatf(quat_data[0], Gf.Vec3f(quat_data[1], quat_data[2], quat_data[3])))
            
        # Set transform order with the operations we have
        if rotation_op:
            xform.SetXformOpOrder([translate_op, rotation_op, scale_op])
        else:
            xform.SetXformOpOrder([translate_op, scale_op])
        
        # Add physics if enabled (with global override option)
        physics_enabled = product_data.get("physics_enabled", False) and ENABLE_PHYSICS_FOR_ALL
        
        if physics_enabled:
            print(f"  Adding physics to {product_id}...")
            # Add RigidBody API
            rigid_body_api = UsdPhysics.RigidBodyAPI.Apply(product_prim)
            rigid_body_api.CreateRigidBodyEnabledAttr(True)
            rigid_body_api.CreateKinematicEnabledAttr(False)
            
            # Add Physx RigidBody API  
            physx_rb_api = PhysxSchema.PhysxRigidBodyAPI.Apply(product_prim)
            
            # Add collision APIs - this is crucial for preventing fall-through
            if FORCE_COLLISION_FOR_PHYSICS:
                collision_api = UsdPhysics.CollisionAPI.Apply(product_prim)
                collision_api.CreateCollisionEnabledAttr(True)
                
                # Add Physx collision APIs for better collision detection
                physx_collision_api = PhysxSchema.PhysxCollisionAPI.Apply(product_prim)
                
                # Use convex hull approximation for realistic collision
                # Try to find the mesh geometry in the loaded asset to apply collision to
                stage = product_prim.GetStage()
                for child_prim in product_prim.GetAllChildren():
                    # Look for mesh geometry in the loaded asset
                    if child_prim.GetTypeName() == "Mesh":
                        mesh_collision_api = UsdPhysics.CollisionAPI.Apply(child_prim)
                        mesh_collision_api.CreateCollisionEnabledAttr(True)
                        physx_mesh_collision = PhysxSchema.PhysxCollisionAPI.Apply(child_prim)
                        # Try to add convex hull collision
                        try:
                            convex_hull_api = PhysxSchema.PhysxConvexHullCollisionAPI.Apply(child_prim)
                            print(f"    Added convex hull collision for {product_id}")
                        except Exception as e:
                            # Fallback to mesh collision if convex hull fails
                            try:
                                mesh_collision = PhysxSchema.PhysxMeshCollisionAPI.Apply(child_prim)
                                print(f"    Added mesh collision for {product_id}")
                            except Exception as e2:
                                print(f"    Warning: Could not add collision to {product_id}: {e2}")
            
            # Set initial velocities if provided
            if "velocity" in product_data:
                rigid_body_api.CreateVelocityAttr(Gf.Vec3f(*product_data["velocity"]))
            if "angular_velocity" in product_data:
                rigid_body_api.CreateAngularVelocityAttr(Gf.Vec3f(*product_data["angular_velocity"]))
        else:
            print(f"  {product_id} set as static (no physics)")
                
        print(f"Placed product: {product_id} at {product_data['translate']}")
        return True
        
    def randomize_product_rotations(self, product_data_dict, num_products=3):
        """
        Randomly select and randomize rotation properties of specified number of products.
        
        Args:
            product_data_dict (dict): The product data dictionary to modify
            num_products (int): Number of products to randomize (default: 3)
        """
        # Create a copy to avoid modifying the original
        randomized_data = product_data_dict.copy()
        
        # Get list of product IDs
        product_ids = list(randomized_data.keys())
        
        # Randomly select products to randomize
        selected_products = random.sample(product_ids, min(num_products, len(product_ids)))
        
        print(f"Randomizing rotations for products: {selected_products}")
        
        for product_id in selected_products:
            product_data = randomized_data[product_id].copy()
            
            # Generate random rotation values
            if "rotate" in product_data or "orient" not in product_data:
                # Use Euler angles (ZYX order) - generate random rotations in degrees
                random_rotation = [
                    random.uniform(-180, 180),  # X rotation
                    random.uniform(-180, 180),  # Y rotation  
                    random.uniform(-180, 180)   # Z rotation
                ]
                product_data["rotate"] = random_rotation
                # Remove orient if it exists to avoid conflicts
                if "orient" in product_data:
                    del product_data["orient"]
                print(f"  {product_id}: New rotation = {random_rotation}")
            else:
                # Generate random quaternion orientation
                # Create random unit quaternion using Marsaglia method
                u1, u2, u3 = random.random(), random.random(), random.random()
                q1 = math.sqrt(1 - u1) * math.sin(2 * math.pi * u2)
                q2 = math.sqrt(1 - u1) * math.cos(2 * math.pi * u2)
                q3 = math.sqrt(u1) * math.sin(2 * math.pi * u3)
                q0 = math.sqrt(u1) * math.cos(2 * math.pi * u3)
                random_quat = [float(q0), float(q1), float(q2), float(q3)]  # (w, x, y, z)
                
                product_data["orient"] = random_quat
                # Remove rotate if it exists to avoid conflicts
                if "rotate" in product_data:
                    del product_data["rotate"]
                print(f"  {product_id}: New orientation = {random_quat}")
            
            # Update the data
            randomized_data[product_id] = product_data
            
        return randomized_data
        
    def place_all_products(self):
        """Place all products from the product data."""
        print("Placing all products...")
        
        # Randomize 3 products before placing
        randomized_product_data = self.randomize_product_rotations(PRODUCT_DATA, num_products=3)
        success_count = 0
        
        for product_id, product_data in randomized_product_data.items():
            try:
                if self.place_product(product_id, product_data):
                    success_count += 1
                else:
                    print(f"Failed to place product: {product_id}")
            except Exception as e:
                print(f"Error placing product {product_id}: {str(e)}")
                
        print(f"Successfully placed {success_count} out of {len(randomized_product_data)} products")
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