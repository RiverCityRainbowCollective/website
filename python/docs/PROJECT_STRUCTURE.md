# BookStack Importer Project Structure

This document describes the reorganized project structure for the BookStack importer.

## Directory Layout

```
python/
├── src/bookstack_importer/          # Main package source code
│   ├── __init__.py                  # Package initialization
│   ├── main.py                      # Main import logic and CLI
│   ├── api/                         # BookStack API client
│   │   ├── __init__.py              # API package exports
│   │   ├── client.py                # API client functions
│   │   └── models.py                # Data classes (Page, Book, etc.)
│   ├── config/                      # Configuration management
│   │   ├── __init__.py              # Config package exports
│   │   └── navigation.py            # Navigation configuration
│   └── utils/                       # Utility functions
│       ├── __init__.py              # Utils package exports
│       ├── content_processor.py     # Content processing functions
│       └── env_loader.py            # Environment variable loading
├── scripts/                         # Command-line entry points
│   ├── import.py                    # Main import script
│   └── manage_navigation.py         # Navigation management CLI
├── tests/                           # Test scripts and utilities
│   └── test_navigation.py           # Navigation configuration tests
├── docs/                            # Documentation
│   └── NAVIGATION_README.md         # Navigation system documentation
├── navigation_config.json           # Navigation configuration file
├── .env.example                     # Environment variables template
├── pyproject.toml                   # Poetry configuration (existing)
├── poetry.lock                      # Poetry lock file (existing)
├── README.md                        # Main project documentation
└── PROJECT_STRUCTURE.md             # This file
```

## Package Organization

### `src/bookstack_importer/`
The main package containing all the core functionality, organized into logical modules:

- **`api/`**: BookStack API interaction
  - `client.py`: HTTP client functions for API calls
  - `models.py`: Data classes representing BookStack entities

- **`config/`**: Configuration management
  - `navigation.py`: Navigation folder mapping configuration

- **`utils/`**: Utility functions
  - `content_processor.py`: Content processing and markdown conversion
  - `env_loader.py`: Environment variable loading for development

- **`main.py`**: Main import logic and command-line interface

### `scripts/`
Command-line entry points that import and use the main package:

- **`import.py`**: Main import script (replaces old `bookstack-import.py`)
- **`manage_navigation.py`**: Navigation configuration management

### `tests/`
Test scripts and utilities:

- **`test_navigation.py`**: Tests and demonstrations of navigation configuration

### `docs/`
Documentation files:

- **`NAVIGATION_README.md`**: Comprehensive navigation system documentation

## Migration from Old Structure

### Old Files → New Locations

| Old File | New Location | Notes |
|----------|-------------|-------|
| `bookstack-classes.py` | `src/bookstack_importer/api/models.py` | Data classes |
| `bookstack.py` | `src/bookstack_importer/api/client.py` | API client |
| `navigation_config.py` | `src/bookstack_importer/config/navigation.py` | Navigation config |
| `systemtools.py` | `src/bookstack_importer/utils/content_processor.py` | Content processing |
| `load_env.py` | `src/bookstack_importer/utils/env_loader.py` | Environment loading |
| `bookstack-import.py` | `scripts/import.py` | Main script |
| `manage_navigation.py` | `scripts/manage_navigation.py` | Management script |
| `test_navigation.py` | `tests/test_navigation.py` | Test script |
| `NAVIGATION_README.md` | `docs/NAVIGATION_README.md` | Documentation |

### Deprecated Files

The following files are now deprecated but kept for backward compatibility:

- `bookstack-classes.py`
- `bookstack.py` 
- `navigation_config.py`
- `systemtools.py`
- `load_env.py`
- `bookstack-import.py`
- `manage_navigation.py`
- `test_navigation.py`

## Benefits of New Structure

1. **Clear Separation of Concerns**: API, configuration, and utilities are in separate modules
2. **Proper Python Package Structure**: Follows Python packaging best practices
3. **Better Import Management**: Clean imports with proper `__init__.py` files
4. **Easier Testing**: Test files are separate from source code
5. **Better Documentation**: Documentation is organized in a dedicated directory
6. **Maintainability**: Easier to find and modify specific functionality
7. **Extensibility**: Easy to add new modules and functionality

## Usage

### Running Scripts

```bash
# Main import
python scripts/import.py

# Navigation management
python scripts/manage_navigation.py show

# Testing
python tests/test_navigation.py
```

### Importing as Package

```python
# Import the main function
from bookstack_importer import main

# Import specific components
from bookstack_importer.api import BookStackConfig, create_api_session
from bookstack_importer.config import NavigationConfig
from bookstack_importer.utils import load_env_file
```

## Development

The new structure makes development easier:

1. **Modular Development**: Work on specific components in isolation
2. **Clear Dependencies**: Easy to see what imports what
3. **Testing**: Each module can be tested independently
4. **Documentation**: Each module has its own documentation
5. **IDE Support**: Better autocomplete and navigation in IDEs

## Backward Compatibility

The old script files are maintained for backward compatibility, but users are encouraged to migrate to the new structure:

- Old: `python bookstack-import.py`
- New: `python scripts/import.py`

- Old: `python manage_navigation.py show`
- New: `python scripts/manage_navigation.py show`
