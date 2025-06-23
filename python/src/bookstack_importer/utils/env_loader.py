"""
Environment variable loader for local development.

This module loads environment variables from a .env file if it exists.
"""

import os
from pathlib import Path


def load_env_file(env_file_path: str = None):
    """
    Load environment variables from a .env file.
    
    Args:
        env_file_path (str): Path to the .env file. If None, looks for .env in the project root.
    """
    if env_file_path is None:
        # Look for .env file in the project root (python directory)
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent.parent.parent  # Go up to python directory
        env_file_path = project_root / '.env'
    
    env_path = Path(env_file_path)
    
    if not env_path.exists():
        print(f"No .env file found at {env_path}")
        print("For local development, copy .env.example to .env and fill in your values.")
        return False
    
    print(f"Loading environment variables from {env_path}")
    
    with open(env_path, 'r') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith('#'):
                continue
            
            # Parse KEY=VALUE format
            if '=' in line:
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                # Remove quotes if present
                if value.startswith('"') and value.endswith('"'):
                    value = value[1:-1]
                elif value.startswith("'") and value.endswith("'"):
                    value = value[1:-1]
                
                # Set environment variable
                os.environ[key] = value
                print(f"  {key}={'*' * len(value) if 'SECRET' in key or 'TOKEN' in key else value}")
            else:
                print(f"Warning: Invalid format on line {line_num}: {line}")
    
    return True


def check_required_env_vars():
    """
    Check if all required environment variables are set.
    
    Returns:
        bool: True if all required variables are set, False otherwise.
    """
    required_vars = [
        "BOOKSTACK_BASE_URL",
        "BOOKSTACK_TOKEN_ID", 
        "BOOKSTACK_TOKEN_SECRET",
        "BOOKSTACK_SHELF_SLUG"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print("Missing required environment variables:")
        for var in missing_vars:
            print(f"  - {var}")
        return False
    
    return True


if __name__ == "__main__":
    # Load .env file if it exists
    load_env_file()
    
    # Check if all required variables are set
    if check_required_env_vars():
        print("All required environment variables are set!")
    else:
        print("\nPlease set the missing environment variables.")
        print("For local development, copy .env.example to .env and fill in your values.")
