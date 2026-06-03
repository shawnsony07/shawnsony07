"""
Convert a profile picture to ASCII art and update both SVG files.
Usage: python generate_ascii.py [image_path]
Default: downloads GitHub profile picture for shawnsony07
"""
import sys
import os
import re
import requests
from io import BytesIO

try:
    from PIL import Image, ImageEnhance
except ImportError:
    os.system(sys.executable + " -m pip install Pillow")
    from PIL import Image, ImageEnhance

# Character ramp from lightest to darkest visual density (20 levels)
ASCII_CHARS = " .',:;clodxkO0KXNWM@"

WIDTH = 40   # characters wide
HEIGHT = 25  # lines tall
CHAR_ASPECT = 0.55  # width/height ratio of monospace characters


def load_image(source):
    """Load image from file path or URL."""
    if source.startswith('http'):
        response = requests.get(source, timeout=15)
        response.raise_for_status()
        return Image.open(BytesIO(response.content))
    return Image.open(source)


def image_to_ascii(img, width=WIDTH, height=HEIGHT, invert=False):
    """Convert PIL Image to list of ASCII art lines."""
    img = img.convert('L')

    # Calculate the pixel-equivalent aspect of the character grid
    target_pixel_aspect = (width / height) * (1 / CHAR_ASPECT)
    img_aspect = img.width / img.height

    if img_aspect > target_pixel_aspect:
        # Image wider than needed -> crop sides
        new_w = int(img.height * target_pixel_aspect)
        left = (img.width - new_w) // 2
        img = img.crop((left, 0, left + new_w, img.height))
    else:
        # Image taller than needed -> crop top/bottom (bias toward face area)
        new_h = int(img.width / target_pixel_aspect)
        top = (img.height - new_h) // 5  # keep upper portion for face
        img = img.crop((0, top, img.width, top + new_h))

    img = img.resize((width, height), Image.LANCZOS)

    # Boost contrast for punchier ASCII art
    img = ImageEnhance.Contrast(img).enhance(1.4)
    img = ImageEnhance.Brightness(img).enhance(1.1)

    pixels = list(img.getdata())
    num_chars = len(ASCII_CHARS)

    lines = []
    for row in range(height):
        line = ""
        for col in range(width):
            pixel = pixels[row * width + col]
            idx = int(pixel / 256 * num_chars)
            idx = min(idx, num_chars - 1)
            if invert:
                line += ASCII_CHARS[num_chars - 1 - idx]
            else:
                line += ASCII_CHARS[idx]
        lines.append(line)
    return lines


def xml_escape(text):
    """Escape XML special characters in text content."""
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def build_tspans(lines):
    """Build SVG tspan elements from ASCII art lines."""
    tspans = []
    y = 30
    for line in lines:
        escaped = xml_escape(line)
        tspans.append(f'<tspan x="15" y="{y}">{escaped}</tspan>')
        y += 20
    return '\n'.join(tspans)


def update_svg(svg_path, new_tspans):
    """Replace the ASCII art section in an SVG file."""
    with open(svg_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find the first <text> block (ASCII art) and replace its tspan children
    pattern = r'(<text x="15" y="30"[^>]*>\s*\n)(.*?)(</text>)'
    replacement = r'\g<1>' + new_tspans + '\n' + r'\g<3>'
    new_content = re.sub(pattern, replacement, content, count=1, flags=re.DOTALL)

    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(new_content)


def main():
    if len(sys.argv) > 1:
        source = sys.argv[1]
    else:
        source = 'https://github.com/shawnsony07.png?size=460'
        print(f"Downloading GitHub avatar from {source} ...")

    img = load_image(source)
    print(f"Image loaded: {img.size[0]}x{img.size[1]}")

    # --- Dark mode: brightness -> character density ---
    print("Generating dark-mode ASCII art ...")
    dark_lines = image_to_ascii(img, invert=False)
    dark_tspans = build_tspans(dark_lines)
    update_svg('dark_mode.svg', dark_tspans)
    print("  -> dark_mode.svg updated")

    # --- Light mode: inverted (dark pixels -> dense chars) ---
    print("Generating light-mode ASCII art ...")
    light_lines = image_to_ascii(img, invert=True)
    light_tspans = build_tspans(light_lines)
    update_svg('light_mode.svg', light_tspans)
    print("  -> light_mode.svg updated")

    # Preview
    print("\n=== DARK MODE PREVIEW ===")
    for l in dark_lines:
        print(l)
    print("\n=== LIGHT MODE PREVIEW ===")
    for l in light_lines:
        print(l)
    print("\nDone!")


if __name__ == '__main__':
    main()
