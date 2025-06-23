"""
Main BookStack importer module

Contains the main function for importing content from BookStack.
"""

import os
from typing import Dict
from pathlib import Path

from .api import BookStackConfig, create_api_session, get_shelf_contents, BookStackAPIError
from .utils import ensure_navigation_directories, create_content_files_with_navigation
from .config import NavigationConfig

# Try to load environment variables from .env file for local development
try:
    from .utils.env_loader import load_env_file
    load_env_file()
except ImportError:
    # env_loader not available, continue without it
    pass


def main(base_url: str, token_id: str, token_secret: str, shelf_slug: str, config_file: str = None) -> Dict:
    """
    Main function for importing BookStack content.
    
    Args:
        base_url (str): Base URL of the BookStack instance
        token_id (str): API Token ID
        token_secret (str): API Token Secret
        shelf_slug (str): Slug identifier of the shelf to retrieve
        config_file (str): Path to navigation configuration file (optional)
        
    Returns:
        Dict: Dictionary containing the shelf contents
        
    Raises:
        BookStackAPIError: If any API operation fails
    """
    config = BookStackConfig(base_url, token_id, token_secret)
    session = create_api_session(config)
    shelf_contents = get_shelf_contents(session, base_url, shelf_slug)

    # Setup paths
    repo_path = Path(__file__).parent.parent.parent.parent  # Go up to repo root
    print(f"repo_path: {repo_path}")
    website_path = repo_path / "website"
    print(f"website_path: {website_path}")
    
    # Load navigation configuration
    if config_file is None:
        config_file = repo_path / "python" / "navigation_config.json"
    
    print(f"Loading navigation config from: {config_file}")
    nav_config = NavigationConfig.load_from_file(str(config_file))
    
    print(f"Navigation configuration:")
    print(f"  Default folder: {nav_config.default_folder}")
    print(f"  Book mappings: {nav_config.book_mappings}")
    print(f"  All folders to be created: {nav_config.get_all_folders()}")
    
    # Ensure navigation directories exist
    print("Ensuring navigation directories exist...")
    ensure_navigation_directories(str(website_path), nav_config)

    # Create new content
    print("Creating content files with navigation...")
    create_content_files_with_navigation(shelf_contents, str(website_path), base_url, nav_config)

    return {
        'shelf_id': shelf_contents.id,
        'name': shelf_contents.name,
        'slug': shelf_contents.slug,
        'description': shelf_contents.description,
        'books': shelf_contents.books
    }


def cli_main():
    """Command-line interface for the BookStack importer."""
    # Get configuration from environment variables
    BASE_URL = os.getenv("BOOKSTACK_BASE_URL")
    TOKEN_ID = os.getenv("BOOKSTACK_TOKEN_ID")
    TOKEN_SECRET = os.getenv("BOOKSTACK_TOKEN_SECRET")
    SHELF_SLUG = os.getenv("BOOKSTACK_SHELF_SLUG")
    
    # Validate that all required environment variables are set
    required_vars = {
        "BOOKSTACK_BASE_URL": BASE_URL,
        "BOOKSTACK_TOKEN_ID": TOKEN_ID,
        "BOOKSTACK_TOKEN_SECRET": TOKEN_SECRET,
        "BOOKSTACK_SHELF_SLUG": SHELF_SLUG
    }
    
    missing_vars = [var for var, value in required_vars.items() if not value]
    
    if missing_vars:
        print("Error: Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        print("\nPlease set these environment variables before running the script.")
        print("Example:")
        print("  export BOOKSTACK_BASE_URL='https://your-bookstack.com'")
        print("  export BOOKSTACK_TOKEN_ID='your-token-id'")
        print("  export BOOKSTACK_TOKEN_SECRET='your-token-secret'")
        print("  export BOOKSTACK_SHELF_SLUG='your-shelf-slug'")
        exit(1)
    
    try:
        print(f"Connecting to BookStack at: {BASE_URL}")
        print(f"Importing shelf: {SHELF_SLUG}")
        result = main(BASE_URL, TOKEN_ID, TOKEN_SECRET, SHELF_SLUG)
        print("Import completed successfully!")
    except (BookStackAPIError, ValueError) as e:
        print(f"Error: {str(e)}")
        exit(1)


if __name__ == "__main__":
    cli_main()
