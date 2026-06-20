#!/usr/bin/env python3
"""
Generate downloadable Kartoza desktop wallpapers — expanded version
of the homepage hero (Rewrite theme): solid charcoal canvas with
the map motif clipped to a slanted polygon on the right edge and
an amber slant rule along the polygon's leading edge.

Output: PNG files under /static/img/brand/wallpapers/, one per
target resolution.

Run: nix develop --command python3 scripts/generate-wallpapers.py
"""
import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT       = Path(__file__).resolve().parent.parent
MOTIF      = ROOT / "static" / "img" / "brand" / "kartoza-background.png"
LOGO       = ROOT / "static" / "img" / "kartoza-logo.png"
OUT_DIR    = ROOT / "static" / "img" / "brand" / "wallpapers"

# Kartoza Brand Pack v1.0.1 palette
CHARCOAL   = (56, 57, 57)        # #383939
AMBER      = (238, 179, 72)      # #EEB348
WHITE      = (255, 255, 255)
RULE       = (209, 209, 209)     # #D1D1D1

# Geometry — mirrors the homepage hero CSS variables
MOTIF_WIDTH_PCT  = 0.55     # motif occupies right 55% of canvas
MOTIF_SKEW_PCT   = 0.10     # top-left of motif polygon, relative to motif width
AMBER_RULE_PX    = 6        # amber stripe thickness

# Output sizes (label, width, height)
SIZES = [
    ("1080p",            1920, 1080),
    ("1440p",            2560, 1440),
    ("4k",               3840, 2160),
    ("ultrawide-1440p",  3440, 1440),
    ("super-ultrawide",  5120, 1440),
    ("macbook-13",       2560, 1600),
    ("macbook-16",       3072, 1920),
    ("mobile-portrait",  1440, 2960),
]

VISION_TITLE   = "Kartoza"
VISION_EYEBROW = "OPEN SOURCE GEOSPATIAL EXPERTS"
VISION_LABEL   = "OUR VISION"
VISION_TEXT    = (
    "Enable a world where spatial decision making "
    "tools are universal, accessible and affordable "
    "for everyone."
)
URL_TEXT       = "kartoza.com"


def find_font(weight: str = "Regular", points: int = 48) -> ImageFont.FreeTypeFont:
    """Locate a usable system font, preferring project-bundled Lato."""
    candidates = [
        ROOT / "static" / "webfonts" / f"Lato-{weight}.ttf",
        Path("/run/current-system/sw/share/fonts/lato/Lato-{weight}.ttf"),
        Path(f"/usr/share/fonts/truetype/lato/Lato-{weight}.ttf"),
        Path(f"/usr/share/fonts/lato/Lato-{weight}.ttf"),
    ]
    for p in candidates:
        if p.exists():
            return ImageFont.truetype(str(p), points)
    # System fallback — DejaVu is present on most Linux/Nix systems
    fallback = "DejaVuSans-Bold.ttf" if weight in ("Bold", "Black") else "DejaVuSans.ttf"
    return ImageFont.truetype(fallback, points)


def wrap_text(draw, text, font, max_width):
    """Greedy word-wrap to fit within max_width pixels."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        candidate = (cur + " " + w).strip()
        bbox = draw.textbbox((0, 0), candidate, font=font)
        if bbox[2] - bbox[0] <= max_width:
            cur = candidate
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def generate(width: int, height: int, label: str) -> Path:
    """Compose one wallpaper at the requested resolution."""
    canvas = Image.new("RGB", (width, height), CHARCOAL)

    # ---- Motif on the right column ---------------------------
    motif_w_px = int(width * MOTIF_WIDTH_PCT)
    skew_px    = int(motif_w_px * MOTIF_SKEW_PCT)

    motif = Image.open(MOTIF).convert("RGB")
    # Cover-fit the motif into a (motif_w_px × height) box
    mw, mh = motif.size
    scale  = max(motif_w_px / mw, height / mh)
    motif = motif.resize((int(mw * scale), int(mh * scale)), Image.LANCZOS)
    # Center-crop
    mw, mh = motif.size
    left   = (mw - motif_w_px) // 2
    top    = (mh - height) // 2
    motif  = motif.crop((left, top, left + motif_w_px, top + height))

    # Slanted polygon mask: motif visible from (skew_px, 0) at top to (0, height) at bottom
    mask = Image.new("L", (motif_w_px, height), 0)
    md   = ImageDraw.Draw(mask)
    md.polygon([
        (skew_px, 0),
        (motif_w_px, 0),
        (motif_w_px, height),
        (0, height),
    ], fill=255)
    canvas.paste(motif, (width - motif_w_px, 0), mask)

    # ---- Amber slant rule ------------------------------------
    rule_x_top    = width - motif_w_px + skew_px
    rule_x_bottom = width - motif_w_px
    half          = AMBER_RULE_PX // 2
    cd = ImageDraw.Draw(canvas)
    cd.polygon([
        (rule_x_top - half,    0),
        (rule_x_top + half,    0),
        (rule_x_bottom + half, height),
        (rule_x_bottom - half, height),
    ], fill=AMBER)

    # ---- Left-column text ------------------------------------
    text_max_width = int((width - motif_w_px) * 0.82)   # leave breathing room
    text_left      = int(width * 0.06)
    text_top       = int(height * 0.18)

    # Scale type to the SHORTER edge of the canvas — using max() made text
    # absurdly large on wide-and-short canvases like 5120×1440 (text overflowed
    # the bottom).  base ≈ "one line of body text height", and the whole stack
    # is built off it.
    base = min(width, height) / 28    # ~39px on 1080h, ~51px on 1440h, ~106px on 2960h
    font_title    = find_font("Black",   int(base * 2.2))
    font_eyebrow  = find_font("Bold",    int(base * 0.55))
    font_label    = find_font("Bold",    int(base * 0.55))
    font_quote    = find_font("Regular", int(base * 0.95))

    # Kartoza logo + wordmark
    logo = Image.open(LOGO).convert("RGBA")
    logo_h = int(base * 2.6)
    lw, lh = logo.size
    logo_w = int(lw * logo_h / lh)
    logo   = logo.resize((logo_w, logo_h), Image.LANCZOS)
    canvas.paste(logo, (text_left, text_top), logo)

    cursor_y = text_top + logo_h + int(base * 0.6)

    # Eyebrow
    cd.text((text_left, cursor_y), VISION_EYEBROW, font=font_eyebrow, fill=RULE)
    cursor_y += int(base * 1.4)

    # Title
    cd.text((text_left, cursor_y), VISION_TITLE, font=font_title, fill=WHITE)
    cursor_y += int(base * 3.1)

    # "OUR VISION" label
    cd.text((text_left, cursor_y), VISION_LABEL, font=font_label, fill=AMBER)
    cursor_y += int(base * 1.2)

    # Vision quote, with amber left border
    quote_lines = wrap_text(cd, f"“{VISION_TEXT}”", font_quote, text_max_width - int(base * 0.6))
    quote_top   = cursor_y
    line_h      = int(base * 1.3)
    quote_h     = line_h * len(quote_lines)
    # Amber border bar
    cd.rectangle([
        text_left, quote_top,
        text_left + int(base * 0.18), quote_top + quote_h
    ], fill=AMBER)
    for i, line in enumerate(quote_lines):
        cd.text(
            (text_left + int(base * 0.6), quote_top + i * line_h),
            line, font=font_quote, fill=WHITE,
        )
    cursor_y = quote_top + quote_h + int(base * 2.2)

    # URL — instead of the homepage's CTA buttons
    font_url = find_font("Bold", int(base * 0.95))
    cd.text((text_left, cursor_y), URL_TEXT, font=font_url, fill=AMBER)

    # Save
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path = OUT_DIR / f"kartoza-wallpaper-{label}-{width}x{height}.png"
    canvas.save(out_path, "PNG", optimize=True)
    return out_path


def main():
    if not MOTIF.exists():
        sys.exit(f"motif not found: {MOTIF}")
    if not LOGO.exists():
        sys.exit(f"logo not found: {LOGO}")
    print(f"Output dir: {OUT_DIR}")
    for label, w, h in SIZES:
        path = generate(w, h, label)
        size_kb = path.stat().st_size // 1024
        print(f"  {label:<18} {w}x{h:<5}  →  {path.name} ({size_kb} KB)")


if __name__ == "__main__":
    main()
