# Bookstack Import Script

This program will scrape the BookStack wiki and populate pieces of the website with pages from the wiki in a format that will translate to MkDocs.

## New Navigation Configuration System

The import script now supports customizable navigation folders! Instead of putting everything under a single "resources" folder, you can now:

- Set a default folder for books that don't have specific mappings
- Map specific books to their own navigation folders  
- Create multiple navigation sections in your website

### Quick Start

1. **View current configuration:**
   ```bash
   python scripts/manage_navigation.py show
   ```

2. **Add a book mapping:**
   ```bash
   python scripts/manage_navigation.py add events events
   python scripts/manage_navigation.py add policies governance
   ```

3. **Run the import:**
   ```bash
   python scripts/import.py
   ```

### Configuration File

The navigation is controlled by `navigation_config.json`:

```json
{
  "default_folder": "resources",
  "book_mappings": {
    "events": "events",
    "policies": "governance"
  }
}
```

### Management Commands

- `python scripts/manage_navigation.py show` - Show current configuration
- `python scripts/manage_navigation.py add <book-slug> <folder>` - Add book mapping
- `python scripts/manage_navigation.py remove <book-slug>` - Remove book mapping
- `python scripts/manage_navigation.py set-default <folder>` - Set default folder
- `python scripts/manage_navigation.py folders` - List all folders that will be created
- `python scripts/manage_navigation.py reset` - Reset to default configuration

## Project Structure

```
python/
├── src/bookstack_importer/          # Main package
│   ├── api/                         # BookStack API client
│   │   ├── client.py               # API functions
│   │   └── models.py               # Data classes
│   ├── config/                     # Configuration management
│   │   └── navigation.py           # Navigation config classes
│   ├── utils/                      # Utility functions
│   │   ├── content_processor.py    # Content processing
│   │   └── env_loader.py           # Environment loading
│   └── main.py                     # Main import logic
├── scripts/                        # Command-line scripts
│   ├── import.py                   # Main import script
│   └── manage_navigation.py        # Navigation management
├── tests/                          # Test scripts
│   └── test_navigation.py          # Navigation testing
├── docs/                           # Documentation
│   └── NAVIGATION_README.md        # Navigation docs
├── navigation_config.json          # Navigation configuration
└── .env.example                    # Environment template
```

## Usage

### Automated with GitHub Actions (Recommended)

The easiest way to use this script is with the automated GitHub Actions workflow:

1. **Set up GitHub secrets** with your BookStack credentials
2. **Configure the workflow** to run on your desired schedule
3. **Let it run automatically** - it will update your website content daily

See [GITHUB_ACTIONS_SETUP.md](../GITHUB_ACTIONS_SETUP.md) for detailed setup instructions.

### Manual/Local Usage

For local development or manual runs:

1. **Set up environment variables:**
   ```bash
   # Copy the example file and edit with your values
   cp .env.example .env
   # Edit .env with your BookStack credentials
   ```

2. **Run the import:**
   ```bash
   python scripts/import.py
   ```

3. **Test your environment setup:**
   ```bash
   python -m src.bookstack_importer.utils.env_loader
   ```

### Environment Variables

The script requires these environment variables:

- `BOOKSTACK_BASE_URL` - Base URL of your BookStack instance
- `BOOKSTACK_TOKEN_ID` - API Token ID from BookStack  
- `BOOKSTACK_TOKEN_SECRET` - API Token Secret from BookStack
- `BOOKSTACK_SHELF_SLUG` - Slug of the shelf to import

For detailed documentation on the navigation system, see [NAVIGATION_README.md](NAVIGATION_README.md).
