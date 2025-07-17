"""
Content processing utilities

Contains functions for processing BookStack content and converting it to markdown.
"""

import re
import shutil
import os
import requests
from urllib.parse import urljoin, urlparse
from pathlib import Path

from ..api.models import ShelfContent
from ..config.navigation import NavigationConfig


def ensure_navigation_directories(website_path: str, nav_config: NavigationConfig) -> None:
    """
    Ensure all navigation directories exist based on the configuration.
    Does not remove existing content.
    """
    website_path = Path(website_path)
    
    # Get all folders that will be created
    folders = nav_config.get_all_folders()
    
    for folder in folders:
        folder_path = website_path / folder
        folder_path.mkdir(parents=True, exist_ok=True)


def clean_resource_directory(resource_path: str) -> None:
    """
    Clean the resource directory by removing all existing content.
    DEPRECATED: Use ensure_navigation_directories instead.
    """
    path = Path(resource_path)
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(exist_ok=True)


def create_content_files_with_navigation(shelf_content: ShelfContent, website_path: str, base_url: str, nav_config: NavigationConfig) -> None:
    """
    Create markdown files and directories from shelf content using navigation configuration.
    """
    website_path = Path(website_path)
    
    for book in shelf_content.books:
        # Get the navigation folder for this book
        nav_folder = nav_config.get_folder_for_book(book.slug)
        nav_path = website_path / nav_folder
        
        # Create book directory within the navigation folder
        # Special handling for books that match their navigation folder name
        if book.slug == nav_folder:
            book_path = nav_path
        else:
            book_path = nav_path / book.slug
            book_path.mkdir(exist_ok=True)
        
        print(f"Processing book '{book.name}' (slug: {book.slug}) -> {nav_folder}/{book.slug if book.slug != nav_folder else ''}")
        
        # Handle standalone pages
        for page in book.pages:
            page_dir = book_path
            page_file = page_dir / f"{page.slug}.md"
            # Convert HTML content and download images to the same directory
            markdown_content = convert_html_to_markdown_with_images(
                page.html,
                page.slug,
                book.slug,
                base_url,
                page_dir
            )
            
            with open(page_file, "w", encoding='utf-8') as f:
                # Write frontmatter
                f.write("---\n")
                f.write(f'title: "{page.name}"\n')
                f.write("---\n\n")
                f.write(markdown_content)

        # Handle chapters and their pages
        for chapter in book.chapters:
            chapter_path = book_path / chapter.slug
            chapter_path.mkdir(exist_ok=True)
            
            # Create chapter pages
            for page in chapter.pages:
                page_dir = chapter_path
                page_file = page_dir / f"{page.slug}.md"
                # Convert HTML content and download images to the same directory
                markdown_content = convert_html_to_markdown_with_images(
                    page.html,
                    page.slug,
                    book.slug,
                    base_url,
                    page_dir
                )
                
                with open(page_file, "w", encoding='utf-8') as f:
                    # Write frontmatter
                    f.write("---\n")
                    f.write(f"title: {page.name}\n")
                    f.write("---\n\n")
                    f.write(markdown_content)


def create_content_files(shelf_content: ShelfContent, resource_path: str, base_url: str) -> None:
    """
    Create markdown files and directories from shelf content.
    DEPRECATED: Use create_content_files_with_navigation instead.
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
            page_dir = book_path
            page_file = page_dir / f"{page.slug}.md"
            # Convert HTML content and download images to the same directory
            markdown_content = convert_html_to_markdown_with_images(
                page.html,
                page.slug,
                book.slug,
                base_url,
                page_dir
            )
            
            with open(page_file, "w", encoding='utf-8') as f:
                # Write frontmatter
                f.write("---\n")
                f.write(f"title: {page.name}\n")
                # f.write("description: The content of this page was written by community members like you!")
                f.write("---\n\n")
                f.write(markdown_content)

        # Handle chapters and their pages
        for chapter in book.chapters:
            chapter_path = book_path / chapter.slug
            chapter_path.mkdir(exist_ok=True)
            
            # Create chapter pages
            for page in chapter.pages:
                page_dir = chapter_path
                page_file = page_dir / f"{page.slug}.md"
                # Convert HTML content and download images to the same directory
                markdown_content = convert_html_to_markdown_with_images(
                    page.html,
                    page.slug,
                    book.slug,
                    base_url,
                    page_dir
                )
                
                with open(page_file, "w", encoding='utf-8') as f:
                    # Write frontmatter
                    f.write("---\n")
                    f.write(f"title: {page.name}\n")
                    f.write("---\n\n")
                    f.write(markdown_content)


def download_image(image_url: str, image_dir: Path, base_url: str) -> str:
    """
    Download an image and return its new local path.
    
    Args:
        image_url: URL of the image to download
        image_dir: Directory to save images
        base_url: Base URL of the BookStack instance
        
    Returns:
        str: Local path to the downloaded image
    """
    try:
        # Handle relative URLs
        if not image_url.startswith(('http://', 'https://')):
            image_url = urljoin(base_url, image_url)
            
        # Get the image filename from the URL
        image_filename = os.path.basename(urlparse(image_url).path)
        local_path = image_dir / image_filename
        
        # Download the image
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        with open(local_path, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
            
        return image_filename
    
    except Exception as e:
        print(f"Failed to download image {image_url}: {str(e)}")
        return None


def convert_html_to_markdown_with_images(html_content: str, page_slug: str, book_slug: str, base_url: str, page_dir: Path) -> str:
    """
    Convert HTML content to markdown, downloading images and updating their paths.
    
    Args:
        html_content: HTML content from BookStack
        page_slug: Slug of the current page
        book_slug: Slug of the current book
        base_url: Base URL of the BookStack instance
        page_dir: Directory where the markdown file will be saved
    """
    # Create directory if it doesn't exist
    page_dir.mkdir(parents=True, exist_ok=True)
    
    # Handle draw.io diagram divs
    def process_drawio_div(match):
        div_content = match.group(0)
        # Extract the image tag
        img_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*>', div_content)
        if img_match:
            image_url = img_match.group(1)
            print(f"Processing draw.io image: {image_url}")
            
            # Download the image
            local_image = download_image(image_url, page_dir, base_url)
            if local_image:
                return f"![]({local_image})"
        return div_content
    
    # Handle regular BookStack images with links
    def process_linked_image(match):
        link_content = match.group(0)
        # Extract image information
        href_match = re.search(r'href="([^"]+)"', link_content)
        img_match = re.search(r'<img[^>]+src="([^"]+)"[^>]*>', link_content)
        alt_match = re.search(r'alt="([^"]+)"', link_content)
        
        if img_match and href_match:
            image_url = href_match.group(1)
            alt_text = alt_match.group(1) if alt_match else ''
            
            print(f"Processing linked image: {image_url}")
            
            # Download the image
            local_image = download_image(image_url, page_dir, base_url)
            if local_image:
                # Just return the image without the external link
                return f"![{alt_text}]({local_image})"
        return link_content
    
    # Replace draw.io divs
    html_content = re.sub(
        r'<div[^>]*drawio-diagram[^>]*>.*?</div>',
        process_drawio_div,
        html_content
    )
    
    # Replace linked images
    html_content = re.sub(
        r'<p[^>]*><a[^>]*>.*?</a></p>',
        process_linked_image,
        html_content
    )
    
    # Clean up any remaining BookStack-specific attributes
    html_content = re.sub(r'id="bkmrk-[^"]*"', '', html_content)
    html_content = re.sub(r'contenteditable="[^"]*"', '', html_content)
    html_content = re.sub(r'target="_blank"', '', html_content)
    html_content = re.sub(r'rel="noopener"', '', html_content)
    
    return html_content
