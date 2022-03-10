from PIL import Image, ImageEnhance
import numpy as np

import io


# Image type conversions
def image_to_bytes(image: Image, format: str = 'PNG') -> bytes:
    """Converts a PIL Image to a bytes object.

    Parameters
    ----------
    image : PIL Image,

    format : string, default PNG
        Will check for the image format in the Image. If not present, 
        then uses the value in this argument.
    """
    
    if image.format:
        format = image.format
    
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=format)    
    return imgByteArr.getvalue()


def bytes_to_image(bytes_obj: bytes) -> Image:
    """Converts a Image bytes object to PIL Image
    
    Parameters
    ----------
    bytes_obj : Bytes Object,
    """
    return Image.open(io.BytesIO(bytes_obj))


# Image Augmentation Functions
def vary_sharp(image):
    """Vary image sharpness randomly"""
    factor = np.random.randint(100, 500) * 0.01
    return ImageEnhance.Sharpness(image).enhance(factor)

def vary_bright(image):
    """Vary image brightness randomly"""
    factor = np.random.randint(75, 125) * 0.01
    return ImageEnhance.Brightness(image).enhance(factor)

def vary_contrast(image):
    """Vary image contrast randomly"""
    factor = np.random.randint(50, 150) * 0.01
    return ImageEnhance.Contrast(image).enhance(factor)

def vary_angle(image, segment = None):
    """Rotate image by a random angle"""
    angle = np.random.randint(1, 100) * 0.1
    if np.random.randint(1, 10) <= 5:
        angle = -angle

    if segment:
        return image.rotate(angle, fillcolor='#404040'), segment.rotate(angle)
    else:
        return image.rotate(angle, fillcolor='#404040')

def vary_flip(image, segment = None):
    """Flip image vertical or horizontal"""
    side = np.random.choice([Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM])

    if segment:
        return image.transpose(method=side), segment.transpose(method=side)
    else:
        return image.transpose(method=side)


def random_augment(image: Image, segment: Image = None, prob: int = 20):
    """Apply random augmentations to image and segment mask

    Parameters
    ----------
    image : PIL Image,

    segment : PIL Image, default None
        Corresponding segment mask.

    prob: int, default 20
        Probability of applying a transformation
    """
    if np.random.randint(1, 100) <= prob:
        image = vary_sharp(image)       
    if np.random.randint(1, 100) <= prob:
        image = vary_bright(image)       
    if np.random.randint(1, 100) <= prob*1.2:
        image = vary_contrast(image)

    if segment:
        if np.random.randint(1, 100) <= prob:
            image, segment = vary_angle(image, segment)
        if np.random.randint(1, 100) <= prob*1.5:
            image, segment = vary_flip(image, segment)
        return image, segment
    else:
        if np.random.randint(1, 100) <= prob:
            image = vary_angle(image)
        if np.random.randint(1, 100) <= prob*1.5:
            image = vary_flip(image)
        return image
