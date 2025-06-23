"""
BookStack API client

Contains functions for interacting with the BookStack API.
"""

import requests
from typing import Dict, List, Optional
from urllib.parse import urljoin

from .models import BookStackConfig, Page, Chapter, Book, ShelfContent


class BookStackAPIError(Exception):
    """Custom exception for BookStack API errors"""
    pass


def create_api_session(config: BookStackConfig) -> requests.Session:
    """Create a requests session configured for BookStack API access."""
    if not all([config.base_url, config.token_id, config.token_secret]):
        raise ValueError("All BookStack configuration parameters must be provided")
    
    session = requests.Session()
    session.headers.update({
        'Authorization': f'Token {config.token_id}:{config.token_secret}',
        'Content-Type': 'application/json'
    })
    return session


def get_shelf_id_by_slug(session: requests.Session, base_url: str, shelf_slug: str) -> Optional[int]:
    """Get shelf ID by its slug."""
    endpoint = urljoin(base_url, '/api/shelves')
    
    try:
        # Get first page of results
        response = session.get(endpoint)
        response.raise_for_status()
        data = response.json()
        
        # Search current page
        for shelf in data.get('data', []):
            if shelf.get('slug') == shelf_slug:
                return shelf['id']
         
        # Check if there are more pages
        while 'next' in data.get('links', {}):
            response = session.get(data['links']['next'])
            response.raise_for_status()
            data = response.json()
            
            for shelf in data.get('data', []):
                if shelf.get('slug') == shelf_slug:
                    return shelf['id']
        
        return None
        
    except requests.exceptions.RequestException as e:
        raise BookStackAPIError(f"Failed to fetch shelves: {str(e)}") from e


def get_shelf_by_slug(session: requests.Session, base_url: str, shelf_slug: str) -> Optional[Dict]:
    """Get shelf data by its slug."""
    shelf_id = get_shelf_id_by_slug(session, base_url, shelf_slug)
    if shelf_id is None:
        return None
        
    endpoint = urljoin(base_url, f'/api/shelves/{shelf_id}')
    print(f'Getting shelf contents with: {endpoint}')
    
    try:
        response = session.get(endpoint)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        if response.status_code == 404:
            return None
        raise BookStackAPIError(f"Failed to fetch shelf: {str(e)}") from e


def get_shelf_contents(session: requests.Session, base_url: str, shelf_slug: str) -> ShelfContent:
    """Get complete shelf contents including all books, chapters, and pages."""
    shelf = get_shelf_by_slug(session, base_url, shelf_slug)
    if not shelf:
        raise BookStackAPIError(f"Shelf with slug '{shelf_slug}' not found")
    
    try:
        # Get books in the shelf
        books_endpoint = urljoin(base_url, f'/api/shelves/{shelf["id"]}')
        response = session.get(books_endpoint)
        response.raise_for_status()
        books_data = response.json()
        
        # Get detailed contents for each book
        books = [
            get_book_contents(session, base_url, book['id'])
            for book in books_data.get('books', [])
        ]
        
        return ShelfContent(
            id=shelf['id'],
            name=shelf['name'],
            slug=shelf['slug'],
            description=shelf.get('description', ''),
            books=books
        )
    except requests.exceptions.RequestException as e:
        raise BookStackAPIError(f"Failed to fetch shelf contents: {str(e)}") from e


def get_book_contents(session: requests.Session, base_url: str, book_id: int) -> Book:
    """Get all contents of a book including its chapters and pages with their content."""
    try:
        # Get book details with all contents in a single call
        book_endpoint = urljoin(base_url, f'/api/books/{book_id}')
        response = session.get(book_endpoint)
        response.raise_for_status()
        book_data = response.json()

        chapters = []
        standalone_pages = []

        # Process contents array to separate chapters and pages
        for content in book_data.get('contents', []):
            if content.get('type') == 'chapter':
                # Create Chapter object with its pages
                chapter_pages = []
                for page in content.get('pages', []):
                    # Get full page content for each page in the chapter
                    full_page = get_page_content(session, base_url, page['id'])
                    chapter_pages.append(full_page)

                chapters.append(Chapter(
                    id=content['id'],
                    name=content['name'],
                    slug=content['slug'],
                    book_id=content['book_id'],
                    url=content['url'],
                    created_at=content['created_at'],
                    updated_at=content['updated_at'],
                    pages=chapter_pages
                ))
            elif content.get('type') == 'page':
                # Get full page content for standalone page
                full_page = get_page_content(session, base_url, content['id'])
                standalone_pages.append(full_page)
                
        # Create and return Book object
        return Book(
            id=book_data['id'],
            name=book_data['name'],
            slug=book_data['slug'],
            description=book_data.get('description', ''),
            created_at=book_data['created_at'],
            updated_at=book_data['updated_at'],
            chapters=chapters,
            pages=standalone_pages
        )

    except requests.exceptions.RequestException as e:
        raise BookStackAPIError(f"Failed to fetch book contents: {str(e)}") from e


def get_page_content(session: requests.Session, base_url: str, page_id: int) -> Page:
    """Get full content of a specific page."""
    try:
        page_endpoint = urljoin(base_url, f'/api/pages/{page_id}')
        response = session.get(page_endpoint)
        response.raise_for_status()
        page_data = response.json()
        print(f"getting page_data for page: {page_data['name']}")

        return Page(
            id=page_data['id'],
            book_id=page_data['book_id'],
            chapter_id=page_data['chapter_id'],
            name=page_data['name'],
            slug=page_data['slug'],
            html=page_data['html'],
            raw_html=page_data['raw_html'],
            markdown=page_data['markdown'],
            priority=page_data.get('priority', 0),
            created_at=page_data['created_at'],
            updated_at=page_data['updated_at'],
            draft=page_data.get('draft', False),
            template=page_data.get('template', False)
        )

    except requests.exceptions.RequestException as e:
        raise BookStackAPIError(f"Failed to fetch page content: {str(e)}") from e
