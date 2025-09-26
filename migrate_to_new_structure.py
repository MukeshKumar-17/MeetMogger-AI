#!/usr/bin/env python3
"""
Migration script to help transition from old structure to new modular architecture.

This script helps migrate data and configurations from the old structure
to the new production-ready structure.
"""

import os
import shutil
import json
from pathlib import Path


def migrate_data():
    """Migrate data files to new structure."""
    print("🔄 Migrating data files...")
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Migrate transcript.json if it exists
    old_transcript = Path("data/transcript.json")
    if old_transcript.exists():
        print("✅ Found existing transcript.json")
        
        # Load and validate the old transcript
        try:
            with open(old_transcript, 'r') as f:
                data = json.load(f)
            
            # Create new format with metadata
            new_data = {
                "text": data.get("text", ""),
                "metadata": {
                    "migrated_from": "old_structure",
                    "migration_timestamp": "2024-01-01T00:00:00Z",
                    "original_format": "legacy"
                }
            }
            
            # Save in new format
            with open(old_transcript, 'w') as f:
                json.dump(new_data, f, indent=2)
            
            print("✅ Updated transcript.json with new format")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not migrate transcript.json: {e}")


def migrate_scripts():
    """Migrate old scripts to new structure."""
    print("🔄 Migrating scripts...")
    
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        print("✅ Found scripts directory")
        
        # Create backup
        backup_dir = Path("scripts_backup")
        if not backup_dir.exists():
            shutil.copytree(scripts_dir, backup_dir)
            print("✅ Created backup of scripts directory")
        
        print("ℹ️  Old scripts are preserved in scripts_backup/")
        print("ℹ️  New functionality is available in src/meetmogger/")


def create_directories():
    """Create necessary directories for new structure."""
    print("🔄 Creating new directory structure...")
    
    directories = [
        "uploads",
        "outputs", 
        "logs",
        "src/meetmogger",
        "src/meetmogger/core",
        "src/meetmogger/utils", 
        "src/meetmogger/ui",
        "tests"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created {directory}/")


def update_gitignore():
    """Update .gitignore for new structure."""
    print("🔄 Updating .gitignore...")
    
    gitignore_content = """
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
env/
ENV/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
uploads/
outputs/
logs/
*.log
scripts_backup/

# Testing
.coverage
htmlcov/
.pytest_cache/
.tox/

# Docker
.dockerignore
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content.strip())
    
    print("✅ Updated .gitignore")


def main():
    """Main migration function."""
    print("🚀 MeetMogger AI Migration Script")
    print("=" * 40)
    
    try:
        create_directories()
        migrate_data()
        migrate_scripts()
        update_gitignore()
        
        print("\n✅ Migration completed successfully!")
        print("\n📋 Next steps:")
        print("1. Install new dependencies: pip install -r requirements.txt")
        print("2. Run the new application: streamlit run app_new.py")
        print("3. Test the functionality with your existing data")
        print("4. Remove old files when satisfied with the new structure")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("Please check the error and try again.")


if __name__ == "__main__":
    main()
