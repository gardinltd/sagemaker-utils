import numpy as np
from PIL import Image, ImageDraw

from typing import Sequence
from .palette import colors, palette


def mask_array_to_image(
    arr: np.array, palette: Sequence[int] = palette
) -> Image:
    """Converts a Numpy segment mask array into PIL Image with
    palette for segments.

    Parameters
    ----------
    arr : Numpy Array,
        2D Mask array with each unique integer belonging to an instance.

    palette : Sequence[int], default pallete with 55 colors
        Palette to be set for the PNG Image object.
    """
    num_segments = len(np.unique(arr))

    image = Image.fromarray(arr, mode='P')
    image.putpalette(palette[:num_segments*3])
    return image


def overlay_mask(
    image: Image,
    segment: Image,
    alpha: int = 127
) -> Image:
    """Overlays segment mask on the image"""
    segment_alpha = segment.convert('RGBA')
    segment_alpha_mask = Image.fromarray((np.array(segment)!=0).astype('uint8') * alpha).convert('L')
    segment_alpha.putalpha(segment_alpha_mask)
    overlay = image.copy().convert('RGB')
    overlay.paste(segment, (0,0), segment_alpha)
    return overlay


def draw_bounding_box(
    image: Image,
    coordinates: Sequence[Sequence],
    alpha: int = 50,
    colors: Sequence[tuple] = colors[1:]
) -> Image:
    """Draw bounding boxes on top of images"""
    overlay = image.copy().convert('RGB')

    for i, (x1, y1, x2, y2) in enumerate(coordinates):
        box_im = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(box_im)
        draw.rectangle(
            [x1, y1, x2, y2],
            fill=tuple(list(colors[i])+[alpha]),
            outline=colors[i], width=2
        )
        overlay.paste(box_im, (0,0), box_im)

    return overlay


def plot_points(
    image: Image,
    points: Sequence[Sequence],
    radius: int = 5,
    alpha: int = 255,
    color: tuple = (255, 0, 0)
) -> Image:
    """Plot points on top of image"""
    overlay = image.copy().convert('RGB')

    for (x, y) in points:
        point_im = Image.new("RGBA", image.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(point_im)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=tuple(list(color) + [alpha]))

        overlay.paste(point_im, (0,0), point_im)

    return overlay

