#!/usr/bin/env python3
"""
README verification script
"""

with open('README.md', 'r', encoding='utf-8') as f:
    content = f.read()

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