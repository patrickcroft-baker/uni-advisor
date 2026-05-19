#!/usr/bin/env bash
# Setup script for uni-advisor skill
# Installs Python dependency and downloads fonts for PDF generation.
# Run once after installing the skill files.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FONTS_DIR="$SCRIPT_DIR/fonts"

echo "=== uni-advisor setup ==="

# ── 1. Python dependency ──────────────────────────────────────────────────────
echo ""
echo "Checking fpdf2..."
if python3 -c "import fpdf" 2>/dev/null; then
    echo "  fpdf2 already installed."
else
    echo "  Installing fpdf2..."
    pip3 install fpdf2
    echo "  Done."
fi

# ── 2. DejaVu fonts ───────────────────────────────────────────────────────────
echo ""
echo "Checking fonts..."

mkdir -p "$FONTS_DIR"

FONTS=(
    "DejaVuSans.ttf"
    "DejaVuSans-Bold.ttf"
    "DejaVuSans-Oblique.ttf"
)

BASE_URL="https://github.com/dejavu-fonts/dejavu-fonts/raw/main/ttf"

all_present=true
for font in "${FONTS[@]}"; do
    if [ ! -f "$FONTS_DIR/$font" ]; then
        all_present=false
        break
    fi
done

if $all_present; then
    echo "  Fonts already present."
else
    # Try system fonts first (Linux/WSL)
    SYSTEM_FONT_DIR="/usr/share/fonts/truetype/dejavu"
    if [ -d "$SYSTEM_FONT_DIR" ] && [ -f "$SYSTEM_FONT_DIR/DejaVuSans.ttf" ]; then
        echo "  Copying from system fonts ($SYSTEM_FONT_DIR)..."
        for font in "${FONTS[@]}"; do
            cp "$SYSTEM_FONT_DIR/$font" "$FONTS_DIR/$font"
        done
        echo "  Done."
    else
        echo "  Downloading DejaVu fonts..."
        for font in "${FONTS[@]}"; do
            if [ ! -f "$FONTS_DIR/$font" ]; then
                curl -fsSL "$BASE_URL/$font" -o "$FONTS_DIR/$font"
                echo "    Downloaded $font"
            fi
        done
        echo "  Done."
    fi
fi

echo ""
echo "=== Setup complete ==="
echo ""
echo "PDF generator is ready. Usage:"
echo "  python3 $SCRIPT_DIR/generate-uni-pdf.py input.json output.pdf"
