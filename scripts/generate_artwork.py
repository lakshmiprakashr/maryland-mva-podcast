#!/usr/bin/env python3
"""
Generate podcast artwork icon for Maryland MVA Study Podcast.
"""

from PIL import Image, ImageDraw, ImageFont
import math


def create_podcast_artwork():
    """Create a professional podcast artwork icon."""
    
    # Dimensions (Apple Podcasts requirement: 1400x1400 minimum)
    size = 3000
    img = Image.new('RGB', (size, size), '#1a365d')  # Dark blue background
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    for y in range(size):
        # Gradient from dark blue to lighter blue
        r = int(26 + (y / size) * 30)
        g = int(54 + (y / size) * 40)
        b = int(93 + (y / size) * 50)
        draw.line([(0, y), (size, y)], fill=(r, g, b))
    
    # Draw circular accent
    center_x, center_y = size // 2, size // 2 - 100
    radius = 600
    draw.ellipse(
        [center_x - radius, center_y - radius, 
         center_x + radius, center_y + radius],
        fill='#2b6cb0',
        outline='#4299e1',
        width=8
    )
    
    # Draw car icon (simplified)
    car_width = 400
    car_height = 180
    car_x = center_x - car_width // 2
    car_y = center_y - car_height // 2
    
    # Car body
    draw.rounded_rectangle(
        [car_x, car_y + 50, car_x + car_width, car_y + car_height],
        radius=30,
        fill='#e2e8f0'
    )
    
    # Car roof
    draw.rounded_rectangle(
        [car_x + 80, car_y, car_x + car_width - 80, car_y + 80],
        radius=20,
        fill='#e2e8f0'
    )
    
    # Wheels
    wheel_radius = 50
    wheel_y = car_y + car_height - 20
    draw.ellipse(
        [car_x + 60 - wheel_radius, wheel_y - wheel_radius,
         car_x + 60 + wheel_radius, wheel_y + wheel_radius],
        fill='#2d3748'
    )
    draw.ellipse(
        [car_x + car_width - 60 - wheel_radius, wheel_y - wheel_radius,
         car_x + car_width - 60 + wheel_radius, wheel_y + wheel_radius],
        fill='#2d3748'
    )
    
    # Inner wheels
    inner_radius = 25
    draw.ellipse(
        [car_x + 60 - inner_radius, wheel_y - inner_radius,
         car_x + 60 + inner_radius, wheel_y + inner_radius],
        fill='#718096'
    )
    draw.ellipse(
        [car_x + car_width - 60 - inner_radius, wheel_y - inner_radius,
         car_x + car_width - 60 + inner_radius, wheel_y + inner_radius],
        fill='#718096'
    )
    
    # Draw steering wheel icon
    sw_center_x = center_x
    sw_center_y = center_y + 250
    sw_radius = 120
    
    # Outer circle
    draw.ellipse(
        [sw_center_x - sw_radius, sw_center_y - sw_radius,
         sw_center_x + sw_radius, sw_center_y + sw_radius],
        outline='#f6e05e',
        width=15
    )
    
    # Inner spokes
    for angle in [0, 90, 180, 270]:
        rad = math.radians(angle)
        x1 = sw_center_x + int(40 * math.cos(rad))
        y1 = sw_center_y + int(40 * math.sin(rad))
        x2 = sw_center_x + int(sw_radius * math.cos(rad))
        y2 = sw_center_y + int(sw_radius * math.sin(rad))
        draw.line([(x1, y1), (x2, y2)], fill='#f6e05e', width=10)
    
    # Draw headphones icon
    hp_y = center_y - 350
    hp_width = 300
    hp_height = 150
    
    # Headband
    draw.arc(
        [center_x - hp_width // 2, hp_y - hp_height,
         center_x + hp_width // 2, hp_y + hp_height],
        180, 0,
        fill='#f6e05e',
        width=20
    )
    
    # Left earpiece
    draw.rounded_rectangle(
        [center_x - hp_width // 2 - 40, hp_y - 30,
         center_x - hp_width // 2 + 40, hp_y + 80],
        radius=15,
        fill='#f6e05e'
    )
    
    # Right earpiece
    draw.rounded_rectangle(
        [center_x + hp_width // 2 - 40, hp_y - 30,
         center_x + hp_width // 2 + 40, hp_y + 80],
        radius=15,
        fill='#f6e05e'
    )
    
    # Try to load a font, fallback to default
    try:
        # Try system fonts
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
            '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
        ]
        title_font = None
        subtitle_font = None
        
        for fp in font_paths:
            try:
                title_font = ImageFont.truetype(fp, 180)
                subtitle_font = ImageFont.truetype(fp, 100)
                break
            except:
                continue
        
        if title_font is None:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Draw title
    title = "MVA"
    subtitle = "STUDY"
    
    # Get text bounding boxes
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    
    # Draw title text
    draw.text(
        ((size - title_width) // 2, size - 650),
        title,
        fill='white',
        font=title_font
    )
    
    # Draw subtitle text
    draw.text(
        ((size - subtitle_width) // 2, size - 450),
        subtitle,
        fill='#f6e05e',
        font=subtitle_font
    )
    
    # Draw Maryland text
    md_font = subtitle_font
    md_text = "MARYLAND"
    md_bbox = draw.textbbox((0, 0), md_text, font=md_font)
    md_width = md_bbox[2] - md_bbox[0]
    
    draw.text(
        ((size - md_width) // 2, size - 300),
        md_text,
        fill='white',
        font=md_font
    )
    
    # Save
    output_path = 'podcast/artwork.jpg'
    img.save(output_path, 'JPEG', quality=95, dpi=(72, 72))
    print(f"Generated: {output_path}")
    print(f"Size: {size}x{size} pixels")
    
    # Also save as PNG for backup
    img.save('podcast/artwork.png', 'PNG', dpi=(72, 72))
    print(f"Generated: podcast/artwork.png")


if __name__ == "__main__":
    create_podcast_artwork()
