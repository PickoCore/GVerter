#!/usr/bin/env python3
"""
Minecraft Resource Pack Converter - Inisialisasi Project
Membuat struktur folder dan dependencies yang diperlukan
"""

import os
import sys
import subprocess
from pathlib import Path

def create_folder_structure():
    """Membuat struktur folder project"""
    base_dir = Path("/vercel/share/v0-project")
    
    folders = [
        "input",
        "output",
        "converter/core",
        "converter/utils",
        "converter/mappers",
        "converter/ui",
        "temp",
        "logs",
    ]
    
    for folder in folders:
        folder_path = base_dir / folder
        folder_path.mkdir(parents=True, exist_ok=True)
        print(f"✓ Created: {folder}")
    
    return base_dir

def initialize_uv_project():
    """Inisialisasi project dengan uv"""
    try:
        subprocess.run(
            ["uv", "init", "--bare", "."],
            cwd="/vercel/share/v0-project",
            check=True
        )
        print("✓ UV project initialized")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to initialize UV: {e}")
        sys.exit(1)

def add_dependencies():
    """Menambahkan dependencies yang diperlukan"""
    dependencies = [
        "click>=8.1.0",  # CLI framework
        "rich>=13.0.0",  # Terminal UI
        "pillow>=10.0.0",  # Image processing
        "pydantic>=2.0.0",  # Data validation
        "pyyaml>=6.0",  # YAML parsing
        "jsonschema>=4.0",  # JSON validation
        "python-dotenv>=1.0.0",  # Environment variables
        "tqdm>=4.66.0",  # Progress bars
    ]
    
    for dep in dependencies:
        try:
            subprocess.run(
                ["uv", "add", dep],
                cwd="/vercel/share/v0-project",
                check=True,
                capture_output=True
            )
            print(f"✓ Added: {dep}")
        except subprocess.CalledProcessError as e:
            print(f"✗ Failed to add {dep}: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("Minecraft Resource Pack Converter - Project Setup")
    print("=" * 60)
    
    # Create folder structure
    print("\n📁 Creating folder structure...")
    create_folder_structure()
    
    # Initialize UV
    print("\n📦 Initializing UV project...")
    initialize_uv_project()
    
    # Add dependencies
    print("\n⬇️  Adding dependencies...")
    add_dependencies()
    
    print("\n" + "=" * 60)
    print("✓ Project setup completed!")
    print("=" * 60)
