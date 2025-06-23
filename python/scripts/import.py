#!/usr/bin/env python3
"""
BookStack Import Script

Main entry point for importing content from BookStack.
"""

import sys
import os
from pathlib import Path

# Add the src directory to the Python path
src_path = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_path))

from bookstack_importer.main import cli_main

if __name__ == "__main__":
    cli_main()
