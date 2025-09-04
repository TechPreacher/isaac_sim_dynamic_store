## Randomization Feature Summary

### What was added:

1. **New import**: Added `random` and `math` modules for randomization functionality

2. **`randomize_product_rotations()` method**:
   - Randomly selects 3 products from the 25 available products
   - For products with Euler rotations: generates random angles between -180° and +180°
   - For products with quaternion orientations: generates random unit quaternions using Marsaglia method
   - Handles both rotation types properly and avoids conflicts
   - Provides console output showing which products were randomized

3. **Updated `place_all_products()` method**:
   - Now calls randomization before product placement
   - Uses the randomized product data instead of original data
   - Maintains the same placement logic and error handling

4. **Enhanced documentation**:
   - Updated README.md to mention the randomization feature
   - Updated script docstring to describe the new functionality
   - Updated product count from 19 to 25 products

### How it works:
- When `place_all_products()` is called, it first creates a copy of the product data
- Randomly selects 3 products and modifies their rotation/orientation properties
- Places all products using the modified data (3 randomized, 22 original)
- The randomization is different each time the script runs

### Valid rotation ranges:
- **Euler angles**: Random values between -180° and +180° for X, Y, Z rotations
- **Quaternions**: Mathematically valid unit quaternions ensuring proper 3D orientations

### Example console output:
```
Randomizing rotations for products: ['_25_mug_01', '_03_cracker_box_04', 'mac_n_cheese_centered']
  _25_mug_01: New rotation = [-89.64, 168.33, 97.74]
  _03_cracker_box_04: New orientation = [0.707, 0.345, -0.123, 0.601]
  mac_n_cheese_centered: New orientation = [0.891, -0.234, 0.156, 0.356]
```

The feature adds variety to the simulation while maintaining the original precise positioning and physics properties.