#!/usr/bin/env python3
"""
Test script to demonstrate the navigation configuration system.
This script shows how the navigation configuration affects book placement.
"""

import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from bookstack_importer.config import NavigationConfig


def test_navigation_config():
    """Test the navigation configuration with sample data."""
    
    print("=== Navigation Configuration Test ===\n")
    
    # Load the current configuration
    config_file = Path(__file__).parent.parent / "navigation_config.json"
    config = NavigationConfig.load_from_file(str(config_file))
    
    print("Current Configuration:")
    print(f"  Default folder: {config.default_folder}")
    print(f"  Book mappings: {config.book_mappings}")
    print(f"  All folders: {config.get_all_folders()}")
    print()
    
    # Test with sample book slugs
    sample_books = [
        "resources",
        "events", 
        "policies",
        "meeting-minutes",
        "guides",
        "unknown-book"
    ]
    
    print("Book Placement Test:")
    print("Book Slug → Navigation Folder")
    print("-" * 35)
    
    for book_slug in sample_books:
        folder = config.get_folder_for_book(book_slug)
        print(f"{book_slug:20} → {folder}")
    
    print()
    
    # Show what the folder structure would look like
    print("Resulting Website Structure:")
    print("website/")
    
    folders = config.get_all_folders()
    for folder in sorted(folders):
        print(f"├── {folder}/")
        
        # Show which books would go in this folder
        books_in_folder = []
        for book_slug in sample_books:
            if config.get_folder_for_book(book_slug) == folder:
                books_in_folder.append(book_slug)
        
        for i, book_slug in enumerate(books_in_folder):
            is_last = i == len(books_in_folder) - 1
            prefix = "└──" if is_last else "├──"
            
            # Special handling for books that match folder names
            if book_slug == folder:
                print(f"│   {prefix} (content from '{book_slug}' book)")
            else:
                print(f"│   {prefix} {book_slug}/")
        
        if not books_in_folder:
            print("│   └── (no books mapped to this folder)")
    
    print()


if __name__ == "__main__":
    test_navigation_config()
