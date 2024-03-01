import random
from pathlib import Path

import typer
from PIL import Image, ImageDraw, ImageFilter

from palettes import PUNK_DOPAMINE


def main(path: Path):
    if path.is_file():
        files = [path]
    elif path.is_dir():
        files = path.rglob("*.jpg")
    else:
        raise ValueError("No valid file or directory specified.")

    for f in files:
        src_img = Image.open(f)
        src_img = src_img.convert("RGBA")
        width = src_img.width
        height = src_img.height

        padding = int(width * 0.1)
        new_width = width + 2 * padding
        new_height = height + 2 * padding

        new_img = Image.new("RGBA", (new_width, new_height), (255, 255, 255))

        draw = ImageDraw.Draw(new_img)
        palette = PUNK_DOPAMINE
        x_offset = 0
        color_index = 0
        while x_offset < new_width:
            stripe_width = random.randint(int(width * 0.025), int(width * 0.1))
            if stripe_width % 2 != 0:
                stripe_width += 1
            x = x_offset + stripe_width/2 - 1
            draw.line([(x, 0), (x, new_height)], palette[color_index], stripe_width)
            x_offset += stripe_width
            color_index += 1
            if color_index >= len(palette):
                color_index = 0

        # drop shadow
        overlay = Image.new("RGBA", new_img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle(((padding, padding), (padding + width, padding + height)), fill=(0, 0, 0, 200))
        for _ in range(3):
            overlay = overlay.filter(ImageFilter.GaussianBlur(20))
        new_img = Image.alpha_composite(new_img, overlay)

        # paste source image over new image
        new_img.paste(src_img, (padding, padding), src_img)

        new_img = new_img.convert("RGB")
        new_img.save("new.jpg", quality=95)


if __name__ == "__main__":
    typer.run(main)
