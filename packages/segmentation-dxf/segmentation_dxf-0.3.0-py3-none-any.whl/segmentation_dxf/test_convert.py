import numpy as np

import segmentation_dxf


def test_convert():
    image = np.zeros((128, 128, 3), dtype=np.uint8)
    image[32:64, 32:64, :] = 255

    doc = segmentation_dxf.convert(image)
    
    assert len(doc.modelspace().query('*')) == 2
