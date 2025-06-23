#!/usr/bin/env python3
"""
Navigation Configuration Management Tool

This script helps manage the navigation configuration for the BookStack import tool.
It allows you to view, add, remove, and modify book-to-folder mappings.
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from bookstack_importer.config import NavigationConfig


def main():
    parser = argparse.ArgumentParser(description='Manage navigation configuration for BookStack import')
    parser.add_argument('--config', '-c', default='navigation_config.json', 
                       help='Path to navigation config file (default: navigation_config.json)')
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Show command
    show_parser = subparsers.add_parser('show', help='Show current configuration')
    
    # Set default command
    set_default_parser = subparsers.add_parser('set-default', help='Set default folder')
    set_default_parser.add_argument('folder', help='Default folder name')
    
    # Add mapping command
    add_parser = subparsers.add_parser('add', help='Add book to folder mapping')
    add_parser.add_argument('book_slug', help='Book slug')
    add_parser.add_argument('folder', help='Folder name')
    
    # Remove mapping command
    remove_parser = subparsers.add_parser('remove', help='Remove book mapping')
    remove_parser.add_argument('book_slug', help='Book slug to remove')
    
    # List folders command
    list_parser = subparsers.add_parser('folders', help='List all folders that will be created')
    
    # Reset command
    reset_parser = subparsers.add_parser('reset', help='Reset to default configuration')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Load configuration
    config_path = args.config
    if not os.path.isabs(config_path):
        # Look for config file in the python directory
        python_dir = Path(__file__).parent.parent
        config_path = python_dir / config_path
    
    nav_config = NavigationConfig.load_from_file(str(config_path))
    
    if args.command == 'show':
        print("Current Navigation Configuration:")
        print(f"  Config file: {config_path}")
        print(f"  Default folder: {nav_config.default_folder}")
        print(f"  Book mappings:")
        if nav_config.book_mappings:
            for book_slug, folder in nav_config.book_mappings.items():
                print(f"    {book_slug} -> {folder}")
        else:
            print("    (none)")
    
    elif args.command == 'set-default':
        nav_config.default_folder = args.folder
        nav_config.save_to_file(str(config_path))
        print(f"Default folder set to: {args.folder}")
    
    elif args.command == 'add':
        nav_config.add_book_mapping(args.book_slug, args.folder)
        nav_config.save_to_file(str(config_path))
        print(f"Added mapping: {args.book_slug} -> {args.folder}")
    
    elif args.command == 'remove':
        if args.book_slug in nav_config.book_mappings:
            nav_config.remove_book_mapping(args.book_slug)
            nav_config.save_to_file(str(config_path))
            print(f"Removed mapping for: {args.book_slug}")
        else:
            print(f"No mapping found for: {args.book_slug}")
    
    elif args.command == 'folders':
        folders = nav_config.get_all_folders()
        print("Folders that will be created:")
        for folder in folders:
            print(f"  {folder}")
    
    elif args.command == 'reset':
        # Create default configuration
        default_config = NavigationConfig(default_folder="resources")
        default_config.add_book_mapping("events", "events")
        default_config.save_to_file(str(config_path))
        print("Configuration reset to defaults")
        print(f"  Default folder: {default_config.default_folder}")
        print(f"  Book mappings: {default_config.book_mappings}")


if __name__ == "__main__":
    main()
