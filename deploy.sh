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

# Determine OS and set packages directory
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    PACKAGES_DIR="$HOME/Library/Application Support/Sublime Text/Packages"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    PACKAGES_DIR="$HOME/.config/sublime-text/Packages"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    PACKAGES_DIR="$APPDATA/Sublime Text/Packages"
else
    echo -e "${RED}Error: Unsupported operating system: $OSTYPE${NC}"
    exit 1
fi

# Check if packages directory exists
if [ ! -d "$PACKAGES_DIR" ]; then
    echo -e "${RED}Error: Sublime Text Packages directory not found at:${NC}"
    echo "  $PACKAGES_DIR"
    echo ""
    echo "Please ensure Sublime Text is installed."
    exit 1
fi

# Create BeancountAutocomplete package directory
TARGET_DIR="$PACKAGES_DIR/BeancountAutocomplete"
mkdir -p "$TARGET_DIR"

# Files to deploy
FILES_TO_DEPLOY=(
    "beancount_autocomplete.py"
    "BeancountAutocomplete.sublime-settings"
    "Main.sublime-menu"
    "README.md"
)

# Check all source files exist
for file in "${FILES_TO_DEPLOY[@]}"; do
    if [ ! -f "$file" ]; then
        echo -e "${RED}Error: Source file not found: $file${NC}"
        echo "Please run this script from the repository root."
        exit 1
    fi
done

# Backup existing package directory if it exists
if [ -d "$TARGET_DIR" ] && [ "$(ls -A $TARGET_DIR)" ]; then
    BACKUP_DIR="$TARGET_DIR.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "${YELLOW}Backing up existing package to:${NC}"
    echo "  $BACKUP_DIR"
    cp -r "$TARGET_DIR" "$BACKUP_DIR"
fi

# Copy all files
echo -e "${GREEN}Deploying plugin to:${NC}"
echo "  $TARGET_DIR"
for file in "${FILES_TO_DEPLOY[@]}"; do
    cp "$file" "$TARGET_DIR/"
    echo "  ✓ $file"
done

echo -e "${GREEN}✓ Deployment successful!${NC}"
echo ""
echo "Next steps:"
echo "  1. Restart Sublime Text or reload the plugin"
echo "  2. Configure beancount_file in Sublime Text settings"
echo "  3. Test autocomplete in a Beancount file"
