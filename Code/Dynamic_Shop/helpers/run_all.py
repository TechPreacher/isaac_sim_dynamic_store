#!/usr/bin/env python3
"""
Run all helper scripts for Dynamic Shop Placer

This script runs all available helper scripts in sequence to provide
a comprehensive overview of the project status.
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description):
    """Run a helper script and display its output."""
    print(f"\n{'='*60}")
    print(f"[HELPER] {description}")
    print(f"   Running: {script_name}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print(result.stdout)
            if result.stderr:
                print("WARNINGS:")
                print(result.stderr)
        else:
            print(f"[ERROR] ERROR running {script_name}:")
            print(result.stderr)
            if result.stdout:
                print("OUTPUT:")
                print(result.stdout)
    except Exception as e:
        print(f"[ERROR] EXCEPTION running {script_name}: {e}")

def main():
    """Run all helper scripts."""
    print("[HELPERS] DYNAMIC SHOP PLACER - COMPLETE HELPER SUITE")
    print("Running all helper scripts to verify project status...")
    
    # List of scripts to run in order
    scripts = [
        ("test_product_data.py", "Product Data JSON Loading Test"),
        ("count_products.py", "Product Count Verification"),
        ("analyze_physics.py", "Physics Settings Analysis"),
        ("verify_data.py", "Comprehensive Data Verification"),
        ("test_randomization.py", "Randomization Functionality Test"),
        ("verify_readme.py", "README Documentation Check"),
        ("test_and_usage.py", "Complete Test Suite & Usage Instructions")
    ]
    
    # Run each script
    for script_name, description in scripts:
        run_script(script_name, description)
    
    print(f"\n{'='*60}")
    print("[SUCCESS] COMPLETE HELPER SUITE FINISHED")
    print("All helper scripts have been executed.")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()