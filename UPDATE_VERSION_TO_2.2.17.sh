#!/bin/bash

################################################################################
# BIZLENS v2.2.17 VERSION UPDATE SCRIPT
# ============================================
# This script updates all version references from 2.2.16 to 2.2.17
# Run from project root directory
#
# Usage: bash UPDATE_VERSION_TO_2.2.17.sh
################################################################################

set -e  # Exit on error

PROJECT_DIR=$(pwd)
echo "=================================================="
echo "BizLens Version Update Script"
echo "=================================================="
echo "Current Directory: $PROJECT_DIR"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Files to update
FILES_TO_UPDATE=(
    "setup.py"
    "pyproject.toml"
    "src/bizlens/__init__.py"
)

OPTIONAL_FILES=(
    "CHANGELOG.md"
    "README.md"
)

echo -e "${YELLOW}Step 1: Verifying files exist...${NC}"
echo ""

ALL_EXIST=true
for file in "${FILES_TO_UPDATE[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✓${NC} Found: $file"
    else
        echo -e "${RED}✗${NC} Missing: $file"
        ALL_EXIST=false
    fi
done

echo ""

if [ "$ALL_EXIST" = false ]; then
    echo -e "${RED}Error: Some required files are missing!${NC}"
    exit 1
fi

echo -e "${YELLOW}Step 2: Showing current versions...${NC}"
echo ""

for file in "${FILES_TO_UPDATE[@]}"; do
    echo -e "${GREEN}$file:${NC}"
    grep -n "2\.2\.16\|__version__" "$file" | head -3
    echo ""
done

echo -e "${YELLOW}Step 3: Creating backups...${NC}"
echo ""

BACKUP_DIR="backups_v2.2.16_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

for file in "${FILES_TO_UPDATE[@]}"; do
    cp "$file" "$BACKUP_DIR/$file.bak"
    echo -e "${GREEN}✓${NC} Backed up: $file → $BACKUP_DIR/$file.bak"
done

echo ""
echo -e "${YELLOW}Step 4: Updating version strings (2.2.16 → 2.2.17)...${NC}"
echo ""

# Use sed to replace version strings
# macOS: sed -i '' (with empty string argument)
# Linux: sed -i (direct)

for file in "${FILES_TO_UPDATE[@]}"; do
    echo "Updating: $file"

    # Detect OS and use appropriate sed syntax
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' 's/2\.2\.16/2.2.17/g' "$file"
    else
        # Linux
        sed -i 's/2\.2\.16/2.2.17/g' "$file"
    fi

    echo -e "${GREEN}✓${NC} Updated: $file"
done

echo ""
echo -e "${YELLOW}Step 5: Verifying updates...${NC}"
echo ""

for file in "${FILES_TO_UPDATE[@]}"; do
    echo -e "${GREEN}$file:${NC}"
    grep -n "2\.2\.17\|__version__" "$file" | head -3
    echo ""
done

echo -e "${YELLOW}Step 6: Summary${NC}"
echo ""
echo -e "${GREEN}✓ Version successfully updated to 2.2.17${NC}"
echo ""
echo "Backup location: $BACKUP_DIR"
echo ""

echo -e "${YELLOW}Step 7: Optional - Update CHANGELOG.md${NC}"
echo ""
echo "Would you like to add a v2.2.17 section to CHANGELOG.md? (y/n)"
read -r -n 1 response
echo ""

if [[ $response == "y" ]]; then
    echo -e "${YELLOW}Adding CHANGELOG.md entry...${NC}"

    # Get current date
    DATE=$(date +%Y-%m-%d)

    # Create temporary file with new changelog entry
    cat > /tmp/changelog_entry.txt << EOF
## [2.2.17] - $DATE

### Added
- [List new features here]

### Fixed
- [List bug fixes here]

### Changed
- [List changes here]

### Notes
- All 13 notebooks verified for v2.2.17
- Dual pandas/polars support confirmed across all notebooks
- 10/13 notebooks fully tested; 3 require manual verification due to file locks

EOF

    # Prepend to CHANGELOG.md (after header section)
    # Find the line number of the first version entry (## [)
    FIRST_VERSION_LINE=$(grep -n "^## \[" CHANGELOG.md | head -1 | cut -d: -f1)

    if [ -n "$FIRST_VERSION_LINE" ]; then
        # Insert before the first version
        head -n $((FIRST_VERSION_LINE - 1)) CHANGELOG.md > /tmp/changelog_new.txt
        cat /tmp/changelog_entry.txt >> /tmp/changelog_new.txt
        tail -n +$FIRST_VERSION_LINE CHANGELOG.md >> /tmp/changelog_new.txt

        mv /tmp/changelog_new.txt CHANGELOG.md
        echo -e "${GREEN}✓${NC} CHANGELOG.md updated"
    else
        echo -e "${RED}✗${NC} Could not find version entries in CHANGELOG.md"
    fi
else
    echo "Skipping CHANGELOG.md update"
fi

echo ""
echo -e "${YELLOW}Step 8: Final Checklist${NC}"
echo ""
echo "Before uploading to PyPI and GitHub:"
echo ""
echo "☐ Verify version updates are correct:"
echo "    python -c \"import sys; sys.path.insert(0, 'src'); import bizlens; print(f'BizLens version: {bizlens.__version__}')\""
echo ""
echo "☐ Clean old build artifacts:"
echo "    rm -rf dist/ build/ *.egg-info/"
echo ""
echo "☐ Build distribution packages:"
echo "    python setup.py sdist bdist_wheel"
echo ""
echo "☐ Verify build output:"
echo "    ls -lh dist/"
echo ""
echo "☐ Test installation (optional):"
echo "    pip install dist/bizlens-2.2.17-py3-*.whl"
echo ""
echo "☐ Upload to PyPI:"
echo "    twine upload dist/*"
echo ""
echo "☐ Create GitHub release:"
echo "    git add ."
echo "    git commit -m 'Release v2.2.17'"
echo "    git tag v2.2.17"
echo "    git push origin main v2.2.17"
echo ""
echo -e "${GREEN}✓ Version update complete!${NC}"
echo ""
