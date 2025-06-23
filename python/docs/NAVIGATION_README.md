# BookStack Navigation Configuration

This document explains how to use the new navigation configuration system for the BookStack import tool.

## Overview

The navigation configuration system allows you to customize how BookStack books are organized into different navigation folders (menu sections) in your website. Instead of putting everything under a single "resources" folder, you can now:

- Set a default folder for books that don't have specific mappings
- Map specific books to their own navigation folders
- Create multiple navigation sections in your website

## Configuration File

The navigation configuration is stored in `navigation_config.json`. Here's the default configuration:

```json
{
  "default_folder": "resources",
  "book_mappings": {
    "events": "events"
  }
}
```

### Configuration Options

- **`default_folder`**: The folder where books will be placed by default if they don't have a specific mapping
- **`book_mappings`**: A dictionary mapping book slugs to folder names

## How It Works

1. When the import script runs, it loads the navigation configuration
2. For each book in the BookStack shelf:
   - If the book slug has a mapping in `book_mappings`, it goes to that folder
   - Otherwise, it goes to the `default_folder`
3. The script creates the necessary folder structure in the `website/` directory

## Managing Configuration

### Using the Management Script

The `scripts/manage_navigation.py` script provides a command-line interface for managing your configuration:

```bash
# Show current configuration
python scripts/manage_navigation.py show

# Set the default folder
python scripts/manage_navigation.py set-default resources

# Add a book mapping
python scripts/manage_navigation.py add my-book-slug my-folder

# Remove a book mapping
python scripts/manage_navigation.py remove my-book-slug

# List all folders that will be created
python scripts/manage_navigation.py folders

# Reset to default configuration
python scripts/manage_navigation.py reset
```

### Manual Configuration

You can also edit the `navigation_config.json` file directly:

```json
{
  "default_folder": "resources",
  "book_mappings": {
    "events": "events",
    "guides": "guides",
    "policies": "governance",
    "meeting-notes": "governance"
  }
}
```

## Examples

### Example 1: Basic Setup

If you have books with slugs `resources`, `events`, and `policies`, and you want:
- `resources` book → `resources` folder (default)
- `events` book → `events` folder
- `policies` book → `resources` folder (default)

Configuration:
```json
{
  "default_folder": "resources",
  "book_mappings": {
    "events": "events"
  }
}
```

### Example 2: Multiple Navigation Sections

For a more complex setup with multiple navigation sections:

Configuration:
```json
{
  "default_folder": "resources",
  "book_mappings": {
    "events": "events",
    "meeting-minutes": "governance",
    "policies": "governance",
    "guides": "guides",
    "tutorials": "guides"
  }
}
```

This creates four navigation sections:
- `resources` (default)
- `events`
- `governance`
- `guides`

### Example 3: Everything in One Section

If you want everything to go under a single section:

Configuration:
```json
{
  "default_folder": "community",
  "book_mappings": {}
}
```

## Folder Structure

The script creates folders under `website/` based on your configuration. For example, with the default configuration, you might see:

```
website/
├── resources/
│   ├── resources/          # Content from "resources" book
│   └── other-book/         # Content from other books (default)
└── events/
    └── events/             # Content from "events" book
```

## Special Handling

### Books Matching Folder Names

When a book slug matches its target folder name (e.g., `events` book → `events` folder), the content is placed directly in the folder without creating a subfolder.

### Backward Compatibility

The old `create_content_files` function is still available but marked as deprecated. The new system uses `create_content_files_with_navigation`.

## Running the Import

The main import script now uses the navigation configuration automatically:

```bash
python scripts/import.py
```

You can also specify a custom configuration file:

```python
from bookstack_importer import main

result = main(
    base_url="https://your-bookstack.com",
    token_id="your-token-id",
    token_secret="your-token-secret",
    shelf_slug="your-shelf-slug",
    config_file="custom_navigation_config.json"
)
```

## Troubleshooting

### Configuration File Not Found

If the configuration file doesn't exist, the script will create a default one automatically.

### Invalid Configuration

The script will show detailed error messages if there are issues with the configuration file. Common issues:
- Invalid JSON syntax
- Missing required fields

### Debugging

The script provides detailed output showing:
- Which configuration file is being used
- The loaded configuration
- How each book is being mapped to folders

Look for output like:
```
Loading navigation config from: /path/to/navigation_config.json
Navigation configuration:
  Default folder: resources
  Book mappings: {'events': 'events'}
  All folders to be created: ['events', 'resources']
Processing book 'Events' (slug: events) -> events/
Processing book 'Resources' (slug: resources) -> resources/resources
