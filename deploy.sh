#!/bin/bash
#
# Deploy script for local development of BeancountAutocomplete plugin
#
# This script copies the plugin file to Sublime Text's User packages directory
# for testing and development purposes.
#

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Determine OS and set target directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    TARGET_DIR="$HOME/Library/Application Support/Sublime Text/Packages/User"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    TARGET_DIR="$HOME/.config/sublime-text/Packages/User"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    TARGET_DIR="$APPDATA/Sublime Text/Packages/User"
else
    echo -e "${RED}Error: Unsupported operating system: $OSTYPE${NC}"
    exit 1
fi

# Check if target directory exists
if [ ! -d "$TARGET_DIR" ]; then
    echo -e "${RED}Error: Sublime Text User packages directory not found at:${NC}"
    echo "  $TARGET_DIR"
    echo ""
    echo "Please ensure Sublime Text is installed."
    exit 1
fi

# Source file
SOURCE_FILE="beancount_autocomplete.py"

if [ ! -f "$SOURCE_FILE" ]; then
    echo -e "${RED}Error: Source file not found: $SOURCE_FILE${NC}"
    echo "Please run this script from the repository root."
    exit 1
fi

# Target file
TARGET_FILE="$TARGET_DIR/$SOURCE_FILE"

# Backup existing file if it exists
if [ -f "$TARGET_FILE" ]; then
    BACKUP_FILE="$TARGET_FILE.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}Backing up existing file to:${NC}"
    echo "  $BACKUP_FILE"
    cp "$TARGET_FILE" "$BACKUP_FILE"
fi

# Copy the file
echo -e "${GREEN}Deploying plugin to:${NC}"
echo "  $TARGET_FILE"
cp "$SOURCE_FILE" "$TARGET_FILE"

echo -e "${GREEN}✓ Deployment successful!${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart Sublime Text or reload the plugin"
echo "  2. Configure beancount_file in Sublime Text settings"
echo "  3. Test autocomplete in a Beancount file"
