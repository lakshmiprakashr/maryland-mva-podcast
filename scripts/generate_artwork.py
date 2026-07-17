#!/usr/bin/env python3
"""
Generate podcast artwork icon for Maryland MVA Study Podcast - Clean Design.
"""

from PIL import Image, ImageDraw, ImageFont
import math


def create_podcast_artwork():
    """Create a professional podcast artwork icon."""
    
    # Dimensions (Apple Podcasts requirement: 1400x1400 minimum)
    size = 3000
    img = Image.new('RGB', (size, size), '#1a365d')
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background - dark blue to teal
    for y in range(size):
        r = int(26 + (y / size) * 20)
        g = int(54 + (y / size) * 60)
        b = int(93 + (y / size) * 40)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # Draw large circle accent
    center_x, center_y = size // 2, size // 2 - 200
    radius = 700
    draw.ellipse(
        [center_x - radius, center_y - radius, 
         center_x + radius, center_y + radius],
        fill='#2b6cb0',
        outline='#4299e1',
        width=12
    )
    
    # Draw inner circle
    inner_radius = 550
    draw.ellipse(
        [center_x - inner_radius, center_y - inner_radius,
         center_x + inner_radius, center_y + inner_radius],
        fill='#2c5282',
        outline='#3182ce',
        width=6
    )
    
    # Draw steering wheel icon (large, centered)
    sw_center_x = center_x
    sw_center_y = center_y
    sw_radius = 350
    
    # Outer ring
    draw.ellipse(
        [sw_center_x - sw_radius, sw_center_y - sw_radius,
         sw_center_x + sw_radius, sw_center_y + sw_radius],
        outline='#f6e05e',
        width=40
    )
    
    # Inner hub
    hub_radius = 80
    draw.ellipse(
        [sw_center_x - hub_radius, sw_center_y - hub_radius,
         sw_center_x + hub_radius, sw_center_y + hub_radius],
        fill='#f6e05e'
    )
    
    # Spokes (3 spokes like a real steering wheel)
    for angle in [90, 210, 330]:
        rad = math.radians(angle)
        x1 = sw_center_x + int(hub_radius * math.cos(rad))
        y1 = sw_center_y + int(hub_radius * math.sin(rad))
        x2 = sw_center_x + int((sw_radius - 30) * math.cos(rad))
        y2 = sw_center_y + int((sw_radius - 30) * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill='#f6e05e', width=35)
    
    # Draw headphones at top
    hp_y = center_y - 500
    hp_width = 500
    hp_height = 200
    
    # Headband arc
    draw.arc(
        [center_x - hp_width // 2, hp_y - hp_height,
         center_x + hp_width // 2, hp_y + hp_height],
        180, 0,
        fill='#f6e05e',
        width=30
    )
    
    # Left earpiece
    draw.rounded_rectangle(
        [center_x - hp_width // 2 - 60, hp_y - 50,
         center_x - hp_width // 2 + 60, hp_y + 120],
        radius=25,
        fill='#f6e05e'
    )
    
    # Right earpiece
    draw.rounded_rectangle(
        [center_x + hp_width // 2 - 60, hp_y - 50,
         center_x + hp_width // 2 + 60, hp_y + 120],
        radius=25,
        fill='#f6e05e'
    )
    
    # Load fonts
    try:
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        ]
        title_font = None
        subtitle_font = None
        small_font = None
        
        for fp in font_paths:
            try:
                title_font = ImageFont.truetype(fp, 220)
                subtitle_font = ImageFont.truetype(fp, 140)
                small_font = ImageFont.truetype(fp, 100)
                break
            except:
                continue
        
        if title_font is None:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        small_font = ImageFont.load_default()
    
    # Draw text at bottom
    texts = [
        ("MARYLAND", 'white', subtitle_font, size - 550),
        ("MVA", '#f6e05e', title_font, size - 400),
        ("STUDY PODCAST", 'white', small_font, size - 200),
    ]
    
    for text, color, font, y_pos in texts:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        x_pos = (size - text_width) // 2
        draw.text((x_pos, y_pos), text, fill=color, font=font)
    
    # Save
    output_path = 'podcast/artwork.jpg'
    img.save(output_path, 'JPEG', quality=95, dpi=(72, 72))
    print(f"Generated: {output_path}")
    print(f"Size: {size}x{size} pixels")
    
    # Also save as PNG
    img.save('podcast/artwork.png', 'PNG', dpi=(72, 72))
    print(f"Generated: podcast/artwork.png")


if __name__ == "__main__":
    create_podcast_artwork()
