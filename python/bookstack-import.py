import os
from typing import Dict
from bookstack import BookStackConfig, create_api_session, get_shelf_contents, BookStackAPIError
from systemtools import clean_resource_directory, create_content_files
def main(base_url: str, token_id: str, token_secret: str, shelf_slug: str) -> Dict:
    """
    Main function to demonstrate usage of the shelf content retrieval.
    
    Args:
        base_url (str): Base URL of the BookStack instance
        token_id (str): API Token ID
        token_secret (str): API Token Secret
        shelf_slug (str): Slug identifier of the shelf to retrieve
        
    Returns:
        Dict: Dictionary containing the shelf contents
        
    Raises:
        BookStackAPIError: If any API operation fails
    """
    config = BookStackConfig(base_url, token_id, token_secret)
    session = create_api_session(config)
    shelf_contents = get_shelf_contents(session, base_url, shelf_slug)

     # Setup paths
    repo_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    print(f"repo_path: {repo_path}")
    resource_path = os.path.join(repo_path, "website", "resources")
    print(f"resource_path: {resource_path}")
    
    # Clean resource directory
    print("Cleaning resource directory...")
    clean_resource_directory(resource_path)

     # Create new content
    print("Creating content files...")
    create_content_files(shelf_contents, resource_path, base_url)

    return {
        'shelf_id': shelf_contents.id,
        'name': shelf_contents.name,
        'slug': shelf_contents.slug,
        'description': shelf_contents.description,
        'books': shelf_contents.books
    }

if __name__ == "__main__":
    # Example usage (replace with actual values)
    BASE_URL = "https://wiki.rcrc.fyi"
    TOKEN_ID = "gqxXA89C12JCf94cqWZdXXLLWIKW9Khi"
    TOKEN_SECRET = "72EanBq999XnavBmox1NP6nus7KU5BV6"
    SHELF_SLUG = "rainbow-collective-website"
    
    try:
        result = main(BASE_URL, TOKEN_ID, TOKEN_SECRET, SHELF_SLUG)
        # print(f"Retrieved shelf contents: {result}")
    except (BookStackAPIError, ValueError) as e:
        print(f"Error: {str(e)}")
