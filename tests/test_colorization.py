import pytest
import numpy as np

from lib.colorization import _preprocess_image


def test__preprocess_image():
    img_rgb = np.arange(3).reshape(1, 1, 3) / 3
    img_rgb_bw = np.ones((1, 1, 3)) * 0.338
    result = _preprocess_image(img_rgb)
    assert result.shape == img_rgb_bw.shape
    assert np.allclose(result, img_rgb_bw, rtol=1.e-2, atol=1.e-3)
