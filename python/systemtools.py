import shutil
import os
import subprocess
import importlib
from pathlib import Path

bookstack_classes = importlib.import_module('bookstack-classes')
ShelfContent = bookstack_classes.ShelfContent

def clean_resource_directory(resource_path: str) -> None:
    """
    Clean the resource directory by removing all existing content.
    """
    path = Path(resource_path)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(exist_ok=True)

def create_content_files(shelf_content: ShelfContent, resource_path: str) -> None:
    """
    Create markdown files and directories from shelf content.
    
    Args:
        shelf_content: ShelfContent object containing the wiki structure
        resource_path: Path to the resource directory
    """
    base_path = Path(resource_path)
    
    for book in shelf_content.books:
        # Create book directory
        # skip resources book since the site category is already named resources
        if book.slug != 'resources':
            book_path = base_path / book.slug
            book_path.mkdir(exist_ok=True)
        else:
            book_path = base_path
        
        # Handle standalone pages
        for page in book.pages:
            page_file = book_path / f"{page.slug}.md"
            with open(page_file, "w", encoding='utf-8') as f:
                # Write frontmatter
                f.write("---\n")
                f.write(f"title: {page.name}\n")
                f.write("---\n\n")
                f.write(page.html)

        # Handle chapters and their pages
        for chapter in book.chapters:
            chapter_path = book_path / chapter.slug
            chapter_path.mkdir(exist_ok=True)
            
            # Create chapter pages
            for page in chapter.pages:
                page_file = chapter_path / f"{page.slug}.md"
                with open(page_file, "w", encoding='utf-8') as f:
                    # Write frontmatter
                    f.write("---\n")
                    f.write(f"title: {page.name}\n")
                    f.write("---\n\n")
                    f.write(page.html)