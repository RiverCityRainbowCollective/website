"""
BookStack API data models

Contains dataclasses representing BookStack entities.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class BookStackConfig:
    """Configuration class for BookStack API credentials and URL"""
    base_url: str
    token_id: str
    token_secret: str

@dataclass
class Page:
    """Data class to represent a page"""
    id: int
    book_id: int
    chapter_id: int
    name: str
    slug: str
    html: str
    raw_html: str
    markdown: str
    priority: int
    created_at: str
    updated_at: str
    draft: bool
    template: bool

@dataclass
class Chapter:
    """Data class to represent a chapter with its pages"""
    id: int
    name: str
    slug: str
    book_id: int
    url: str
    created_at: str
    updated_at: str
    pages: List[Page]

@dataclass
class Book:
    """Data class to represent a book with its chapters and pages"""
    id: int
    name: str
    slug: str
    description: str
    created_at: str
    updated_at: str
    chapters: List['Chapter']
    pages: List['Page']  # Pages not in chapters

@dataclass
class ShelfContent:
    """Data class to represent a shelf's content"""
    id: int
    name: str
    slug: str
    description: str
    books: List[Dict]
