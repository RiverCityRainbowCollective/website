"""
Navigation configuration

Contains classes for managing navigation folder mappings.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional
import json
import os


@dataclass
class NavigationConfig:
    """Configuration for mapping books to navigation folders"""
    default_folder: str = "resources"
    book_mappings: Dict[str, str] = None
    
    def __post_init__(self):
        if self.book_mappings is None:
            self.book_mappings = {}
    
    def get_folder_for_book(self, book_slug: str) -> str:
        """Get the navigation folder for a given book slug"""
        return self.book_mappings.get(book_slug, self.default_folder)
    
    def add_book_mapping(self, book_slug: str, folder_name: str):
        """Add or update a book to folder mapping"""
        self.book_mappings[book_slug] = folder_name
    
    def remove_book_mapping(self, book_slug: str):
        """Remove a book mapping (will fall back to default)"""
        if book_slug in self.book_mappings:
            del self.book_mappings[book_slug]
    
    def get_all_folders(self) -> List[str]:
        """Get all unique folder names that will be created"""
        folders = set([self.default_folder])
        folders.update(self.book_mappings.values())
        return sorted(list(folders))
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization"""
        return {
            "default_folder": self.default_folder,
            "book_mappings": self.book_mappings
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'NavigationConfig':
        """Create from dictionary"""
        return cls(
            default_folder=data.get("default_folder", "resources"),
            book_mappings=data.get("book_mappings", {})
        )
    
    def save_to_file(self, filepath: str):
        """Save configuration to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load_from_file(cls, filepath: str) -> 'NavigationConfig':
        """Load configuration from JSON file"""
        if not os.path.exists(filepath):
            # Create default config if file doesn't exist
            config = cls()
            config.save_to_file(filepath)
            return config
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)


def create_default_config() -> NavigationConfig:
    """Create a default navigation configuration"""
    config = NavigationConfig(default_folder="resources")
    
    # Add example mappings based on the user's requirements
    config.add_book_mapping("events", "events")
    
    return config
