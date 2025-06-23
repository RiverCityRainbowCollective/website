"""
BookStack API module

Contains classes and functions for interacting with the BookStack API.
"""

from .client import BookStackConfig, create_api_session, get_shelf_contents, BookStackAPIError
from .models import Page, Chapter, Book, ShelfContent

__all__ = [
    "BookStackConfig",
    "create_api_session", 
    "get_shelf_contents",
    "BookStackAPIError",
    "Page",
    "Chapter", 
    "Book",
    "ShelfContent"
]
