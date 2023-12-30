# This file has been modified by the Nextpy Team in 2023 using AI tools and automation scripts. 
# We have rigorously tested these modifications to ensure reliability and performance. Based on successful test results, we are confident in the quality and stability of these changes.

# PIL is only available in python 3.8+
import numpy as np
import PIL
import pytest
from PIL.Image import Image as Img

import nextpy as xt
from nextpy.frontend.components.next.image import Image  # type: ignore
from nextpy.utils.serializers import serialize, serialize_image


@pytest.fixture
def pil_image() -> Img:
    """Get an image.

    Returns:
        A random PIL image.
    """
    imarray = np.random.rand(100, 100, 3) * 255
    return PIL.Image.fromarray(imarray.astype("uint8")).convert("RGBA")  # type: ignore


def test_serialize_image(pil_image: Img):
    """Test that serializing an image works.

    Args:
        pil_image: The image to serialize.
    """
    data = serialize(pil_image)
    assert isinstance(data, str)
    assert data == serialize_image(pil_image)
    assert data.startswith("data:image/png;base64,")


def test_set_src_str():
    """Test that setting the src works."""
    image = xt.image(src="pic2.jpeg")
    assert str(image.src) == "{`pic2.jpeg`}"  # type: ignore


def test_set_src_img(pil_image: Img):
    """Test that setting the src works.

    Args:
        pil_image: The image to serialize.
    """
    image = Image.create(src=pil_image)
    assert str(image.src._var_name) == serialize_image(pil_image)  # type: ignore


def test_render(pil_image: Img):
    """Test that rendering an image works.

    Args:
        pil_image: The image to serialize.
    """
    image = Image.create(src=pil_image)
    assert image.src._var_is_string  # type: ignore
