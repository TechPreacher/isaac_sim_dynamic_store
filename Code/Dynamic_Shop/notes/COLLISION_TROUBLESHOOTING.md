# Collision Detection Troubleshooting Guide

## Issue: Tuna Can (or other products) Falling Through Shelf

### Root Cause Analysis:
The problem occurs when either:
1. **Products lack proper collision detection** → Fixed ✅
2. **Shelf surfaces lack collision detection** → Fixed ✅ 
3. **Collision approximation is inadequate** → Enhanced ✅

## Solutions Implemented:

### ✅ Enhanced Shelf Collision Detection
**New Method**: `setup_shelf_collision()`
- Recursively finds all mesh geometry in shelf hierarchy
- Applies `UsdPhysics.CollisionAPI` and `PhysxSchema.PhysxCollisionAPI`
- Uses triangle mesh collision for accurate static surface collision
- Automatically called during scene setup

### ✅ Enhanced Product Collision Detection  
**Improved collision setup** with multiple approaches:
- Applies collision to root product prim AND child meshes
- Configurable collision approximation via `COLLISION_APPROXIMATION`
- Better error handling and collision verification
- Redundant collision setup for reliability

### ✅ Configuration Options
```python
SETUP_SHELF_COLLISION = True        # Enable shelf collision detection
COLLISION_APPROXIMATION = "convexHull"  # Only option for products (PhysX limitation)
FORCE_COLLISION_FOR_PHYSICS = True  # Ensure collision for all physics products
```

## Collision Types Available:

### For Products (moving objects):
- **`"convexHull"`** (Only supported option): Fast collision for dynamic rigid bodies
- ❌ **`"triangleMesh"`**: NOT supported for dynamic objects (PhysX limitation)
- ❌ **`"convexDecomposition"`**: NOT supported for dynamic objects (PhysX limitation)

### For Shelf (static surfaces):  
- **Triangle Mesh**: Most accurate for static geometry (supported)

### ⚠️ **PhysX Limitation:**
Dynamic physics objects (products that can move) can ONLY use convex collision approximations. Triangle mesh collision is only supported for static objects like shelves.

## Testing & Verification:

### Expected Console Output:
```
Setting up shelf collision detection...
  Checking /World/Shelf for collision setup...
    Added triangle mesh collision to /World/Shelf/shelf_surface

Adding physics to _07_tuna_fish_can_61...
  Added convex hull collision to root prim for _07_tuna_fish_can_61
  Added convex hull collision to mesh 1 for _07_tuna_fish_can_61
```

### Test Procedure:
1. Run the script in Isaac Sim
2. Press Play to start physics simulation
3. Use the Transform tool to lift a tuna can
4. Drop it back onto the shelf
5. **Expected**: Can should collide with shelf and stay on surface
6. **Previous**: Can would fall through shelf

## Quick Fixes if Still Having Issues:

### ⚠️ **Common Error Fixed:**
```
PhysX error: attachShape: non-SDF triangle mesh... are not supported for non-kinematic PxRigidDynamic instances.
```
**Solution**: ✅ Fixed! Products now automatically use convex hull collision only.

### Option 1: Verify Collision Setup
The script now automatically handles proper collision types:
- **Products**: Always use convex hull (PhysX requirement)
- **Shelf**: Uses triangle mesh (static objects only)

### Option 2: Disable Shelf Collision (for debugging)
```python  
SETUP_SHELF_COLLISION = False  # Test if shelf collision causes conflicts
```

### Option 3: Check for Conflicting Physics
- Some assets might have conflicting physics settings
- The enhanced collision setup should override these

## Physics Simulation Notes:
- **Convex Hull**: Fast approximation, good for real-time simulation
- **Triangle Mesh**: Exact geometry, better for precise collision but slower
- **Static vs Dynamic**: Shelves are static (don't move), products are dynamic (physics-enabled)

The collision system is now much more robust and should handle lifting/dropping products correctly! 🎯