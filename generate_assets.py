"""
One-time asset generator for BlogSpace demo data.

Creates:
  - profile_pics/avatar_<username>.jpg : gradient avatar with initials
  - covers/<category>_<1|2>.jpg        : gradient cover images used on blog cards

Run from the project root:  python generate_assets.py
The generated images are committed to the repository, so this only needs
to be re-run when the demo users or categories change.
"""
import os

from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.join(os.path.dirname(__file__), 'flaskblog', 'static')
PROFILE_DIR = os.path.join(BASE_DIR, 'profile_pics')
COVER_DIR = os.path.join(BASE_DIR, 'covers')

# username -> (initials, top color, bottom color)
AVATARS = {
    'admin':            ('KB', '#2563eb', '#7c3aed'),
    'maya_chen':        ('MC', '#0ea5e9', '#6366f1'),
    'arjun_mehta':      ('AM', '#10b981', '#0d9488'),
    'sophia_reyes':     ('SR', '#f59e0b', '#ef4444'),
    'david_kim':        ('DK', '#6366f1', '#a855f7'),
    'aisha_patel':      ('AP', '#ec4899', '#f43f5e'),
    'lucas_weber':      ('LW', '#14b8a6', '#2563eb'),
    'emma_wilson':      ('EW', '#8b5cf6', '#d946ef'),
    'rahul_verma':      ('RV', '#22c55e', '#84cc16'),
    'nina_kovac':       ('NK', '#f97316', '#eab308'),
    'omar_hassan':      ('OH', '#ef4444', '#b91c1c'),
    'grace_liu':        ('GL', '#06b6d4', '#3b82f6'),
    'tom_bennett':      ('TB', '#64748b', '#334155'),
    'zara_ali':         ('ZA', '#d946ef', '#8b5cf6'),
}

# category -> (two color variants, each a (top, bottom) gradient pair)
CATEGORY_COLORS = {
    'technology':   [('#1d4ed8', '#7c3aed'), ('#0f172a', '#2563eb')],
    'ai':           [('#7c3aed', '#db2777'), ('#312e81', '#7c3aed')],
    'travel':       [('#0ea5e9', '#22c55e'), ('#f59e0b', '#ef4444')],
    'lifestyle':    [('#f472b6', '#fb923c'), ('#fda4af', '#f472b6')],
    'productivity': [('#0d9488', '#059669'), ('#334155', '#0d9488')],
    'photography':  [('#334155', '#0f172a'), ('#525252', '#171717')],
    'career':       [('#2563eb', '#0891b2'), ('#475569', '#2563eb')],
    'health':       [('#16a34a', '#84cc16'), ('#10b981', '#0891b2')],
    'finance':      [('#065f46', '#059669'), ('#1e3a8a', '#0891b2')],
    'education':    [('#9333ea', '#4f46e5'), ('#2563eb', '#0ea5e9')],
    'general':      [('#475569', '#94a3b8'), ('#64748b', '#334155')],
}


def _font(size):
    """Pick a bold system font, falling back gracefully."""
    for path in (r'C:\Windows\Fonts\arialbd.ttf', r'C:\Windows\Fonts\arial.ttf',
                 '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'):
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def _diagonal_gradient(draw_obj, size, top, bottom):
    """Paint a smooth diagonal gradient directly onto a draw context."""
    width, height = size
    for y in range(height):
        for segment in range(0, width, 8):
            t = (y / height + segment / width) / 2
            r1, g1, b1 = tuple(int(top[i:i + 2], 16) for i in (1, 3, 5))
            r2, g2, b2 = tuple(int(bottom[i:i + 2], 16) for i in (1, 3, 5))
            color = (int(r1 + (r2 - r1) * t), int(g1 + (g2 - g1) * t), int(b1 + (b2 - b1) * t))
            draw_obj.rectangle([segment, y, segment + 8, y + 1], fill=color)


def make_avatar(username, initials, top, bottom):
    img = Image.new('RGB', (256, 256))
    _diagonal_gradient(ImageDraw.Draw(img), img.size, top, bottom)

    # soft highlight circle for depth
    highlight = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(highlight).ellipse((-70, -70, 150, 150), fill=(255, 255, 255, 38))
    img = Image.alpha_composite(img.convert('RGBA'), highlight).convert('RGB')

    draw = ImageDraw.Draw(img)
    font = _font(96)
    box = draw.textbbox((0, 0), initials, font=font)
    x = (256 - (box[2] - box[0])) / 2 - box[0]
    y = (256 - (box[3] - box[1])) / 2 - box[1]
    draw.text((x + 2, y + 2), initials, font=font, fill=(0, 0, 0, 120))  # soft shadow
    draw.text((x, y), initials, font=font, fill='white')

    img.save(os.path.join(PROFILE_DIR, f'avatar_{username}.jpg'), quality=90)


def make_cover(category, variant, top, bottom):
    img = Image.new('RGB', (960, 480))
    draw = ImageDraw.Draw(img)
    _diagonal_gradient(draw, img.size, top, bottom)

    # decorative translucent shapes + label chip (alpha works on the overlay)
    overlay = Image.new('RGBA', img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse((640, -140, 1100, 320), fill=(255, 255, 255, 26))
    od.ellipse((-120, 260, 300, 620), fill=(255, 255, 255, 20))
    od.ellipse((760, 300, 1020, 560), fill=(0, 0, 0, 22))
    for i in range(4):
        od.line([(0, 430 - i * 14), (960, 350 - i * 14)], fill=(255, 255, 255, 14), width=3)
    label = category.upper()
    lfont = _font(30)
    lbox = od.textbbox((0, 0), label, font=lfont)
    tw, th = lbox[2] - lbox[0], lbox[3] - lbox[1]
    od.rounded_rectangle((36, 36, 36 + tw + 36, 36 + th + 30), radius=24, fill=(15, 23, 42, 110))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')

    # category label text on the flattened image
    draw = ImageDraw.Draw(img)
    draw.text((54, 49), label, font=lfont, fill='white')

    img.save(os.path.join(COVER_DIR, f'{category}_{variant}.jpg'), quality=88)


if __name__ == '__main__':
    os.makedirs(PROFILE_DIR, exist_ok=True)
    os.makedirs(COVER_DIR, exist_ok=True)

    for username, (initials, top, bottom) in AVATARS.items():
        make_avatar(username, initials, top, bottom)
    print(f'Created {len(AVATARS)} avatars in {PROFILE_DIR}')

    count = 0
    for category, variants in CATEGORY_COLORS.items():
        for i, (top, bottom) in enumerate(variants, start=1):
            make_cover(category, i, top, bottom)
            count += 1
    print(f'Created {count} cover images in {COVER_DIR}')
