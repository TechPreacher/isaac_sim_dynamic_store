# Physics Configuration Guide

## Issue: Products Falling Through Scenery

The problem occurs when physics-enabled products don't have proper collision detection set up, causing them to fall through the shelf surfaces.

## Solutions Implemented:

### 1. Enhanced Collision Detection
- Added `UsdPhysics.CollisionAPI` to all physics-enabled products
- Added `PhysxSchema.PhysxCollisionAPI` for better PhysX integration  
- Attempts to add convex hull collision for realistic physics behavior
- Falls back to mesh collision if convex hull fails

### 2. Configuration Options (Top of script)
```python
ENABLE_PHYSICS_FOR_ALL = True   # Set to False to make ALL products static
FORCE_COLLISION_FOR_PHYSICS = True  # Ensures collision for physics products
```

### 3. Quick Fixes:

**Option A: Disable All Physics (Safest)**
Set `ENABLE_PHYSICS_FOR_ALL = False` at the top of the script.
- All products become static (no falling)
- Products stay exactly where placed
- No physics simulation

**Option B: Enable Physics with Collision (Realistic)**  
Keep `ENABLE_PHYSICS_FOR_ALL = True` and `FORCE_COLLISION_FOR_PHYSICS = True`
- Products with physics will have collision detection
- Should prevent fall-through issues
- Maintains realistic physics simulation

## How to Test:
1. Try Option B first (current settings) - run the script
2. If products still fall through, try Option A as backup
3. Check console output for collision setup messages

## Console Output to Look For:
```
Adding physics to _10_potted_meat_can_24...
  Added convex hull collision for _10_potted_meat_can_24
```

## Products by Physics Status:
- **Static (no physics)**: Mustard bottles, Cracker boxes, Tomato soup cans
- **Physics enabled**: Spam cans, Tuna cans, Cleaner bottles, Mugs, Mac-n-cheese boxes