#!/usr/bin/env python3
"""
Debug script for testing the waterjet design agent pipeline
"""

from src.pipeline_controller import run_pipeline
import os

def main():
    print("🔧 Waterjet Design Agent - Debug Mode")
    print("=" * 50)
    
    # Check if data/outputs directory exists
    output_dir = "data/outputs"
    if not os.path.exists(output_dir):
        print(f"❌ Output directory '{output_dir}' not found!")
        os.makedirs(output_dir, exist_ok=True)
        print(f"✅ Created output directory: {output_dir}")
    
    # List files in output directory
    try:
        files = os.listdir(output_dir)
        png_files = [f for f in files if f.lower().endswith('.png')]
        
        print(f"\n📁 Files in {output_dir}:")
        if files:
            for file in files:
                print(f"  - {file}")
        else:
            print("  (empty)")
        
        print(f"\n🖼️  PNG files found: {len(png_files)}")
        for png in png_files:
            print(f"  - {png}")
    
    except Exception as e:
        print(f"❌ Error listing files: {e}")
        return
    
    # Test pipeline
    print("\n🚀 Testing Pipeline...")
    print("-" * 30)
    
    if png_files:
        print("Testing batch conversion...")
        try:
            results = run_pipeline(batch=True)
            print(f"✅ Batch conversion results:")
            if isinstance(results, list):
                for i, result in enumerate(results, 1):
                    print(f"  {i}. {result}")
            else:
                print(f"  {results}")
        except Exception as e:
            print(f"❌ Batch conversion failed: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("No PNG files found. Testing with sample file...")
        try:
            result = run_pipeline(image_filename="sample.png")
            print(f"✅ Single file test result: {result}")
        except Exception as e:
            print(f"❌ Single file test failed: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
