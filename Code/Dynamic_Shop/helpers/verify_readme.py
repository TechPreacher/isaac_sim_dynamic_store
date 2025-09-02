#!/usr/bin/env python3
"""
README verification script
"""

import os

# Find the README.md file relative to this script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)
readme_file = os.path.join(parent_dir, 'README.md')

try:
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()
except FileNotFoundError:
    print(f"Error: Could not find README.md at {readme_file}")
    print("Make sure this script is in the helpers/ subdirectory of the project")
    exit(1)

print('=== README VERIFICATION ===')
print(f'Mentions of "25 products": {content.count("25 products")}')
print(f'Mentions of "8 categories": {content.count("8 categories")}') 
print(f'Mentions of "16 products have physics": {content.count("16 products have physics")}')
print(f'Mentions of "9 are static": {content.count("9 are static")}')

print(f'Mentions of "Mugs": {content.count("Mugs")}')
print(f'Mentions of "Mac": {content.count("Mac")}')
print(f'Mentions of randomization: {content.count("Random") + content.count("random")}')
print(f'Mentions of configuration: {content.count("Configuration") + content.count("configuration")}')

print(f'Latest version mentioned: v1.2' if 'v1.2' in content else 'Version needs update')

# Check if all categories are mentioned
categories = ['MustardBottles', 'Spam', 'TunaCans', 'Cleaner', 'Crackers', 'TomatoCans', 'Mugs', 'Mac_n_Cheese']
for cat in categories:
    if cat in content:
        print(f'✓ {cat} category found')
    else:
        print(f'✗ {cat} category missing')

print('\n✓ README verification complete')