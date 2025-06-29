"""
Quick Test Script for Waterjet Design Agent Components
"""
import sys
import os

def test_imports():
    """Test if all modules can be imported"""
    print("Testing imports...")
    
    try:
        import streamlit as st
        print("✓ Streamlit: OK")
    except ImportError as e:
        print(f"✗ Streamlit: FAILED ({e})")
    
    try:
        from src.catalogue_matcher import load_catalogue, match_design
        print("✓ Catalogue Matcher: OK")
    except ImportError as e:
        print(f"✗ Catalogue Matcher: FAILED ({e})")
    
    try:
        from src.prompt_processor import parse_prompt
        print("✓ Prompt Processor: OK")
    except ImportError as e:
        print(f"✗ Prompt Processor: FAILED ({e})")
    
    try:
        import json
        with open("data/catalogue.json", "r") as f:
            catalog = json.load(f)
        print(f"✓ Catalog loaded: {len(catalog)} designs")
    except Exception as e:
        print(f"✗ Catalog loading: FAILED ({e})")

def test_catalog_matching():
    """Test catalog matching functionality"""
    print("\nTesting catalog matching...")
    
    try:
        from src.catalogue_matcher import match_design
        from src.prompt_processor import parse_prompt
        
        # Test cases
        test_prompts = [
            "Create a steel circle 100mm diameter",
            "Make a marble star with ornamental style",
            "Design a functional washer for M12 bolt"
        ]
        
        for prompt in test_prompts:
            tags = parse_prompt(prompt)
            design = match_design(tags)
            if design:
                print(f"✓ '{prompt}' -> {design['id']} ({design['shape']})")
            else:
                print(f"✗ '{prompt}' -> No match found")
                
    except Exception as e:
        print(f"✗ Catalog matching test failed: {e}")

def test_file_structure():
    """Test if required files and directories exist"""
    print("\nTesting file structure...")
    
    required_files = [
        "app.py",
        "requirements.txt",
        "data/catalogue.json",
        "src/catalogue_matcher.py",
        "src/prompt_processor.py",
        "src/design_browser.py"
    ]
    
    required_dirs = [
        "data",
        "data/outputs",
        "src"
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}: EXISTS")
        else:
            print(f"✗ {file_path}: MISSING")
    
    for dir_path in required_dirs:
        if os.path.isdir(dir_path):
            print(f"✓ {dir_path}/: EXISTS")
        else:
            print(f"✗ {dir_path}/: MISSING")

def main():
    print("WATERJET DESIGN AGENT - SYSTEM CHECK")
    print("=" * 50)
    
    test_file_structure()
    test_imports()
    test_catalog_matching()
    
    print("\n" + "=" * 50)
    print("Test complete! If all items show ✓, you're ready to run:")
    print("streamlit run app.py")

if __name__ == "__main__":
    main()
