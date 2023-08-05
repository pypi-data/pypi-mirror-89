import io

import numpy as np
import cv2 as cv

import segmentation_dxf


def convert_buffer(buffer):
    """
    Converts a buffer of a segmentation image to a buffer of a DXF
    drawing.

    Parameters
    ----------
    buffer : buffer_like
        Input buffer, usually `bytes`.
        Supported filetypes include `PNG` and `JPG`,
        both grayscale and colour.

    Returns
    -------
    output_buffer : bytes
        Output buffer.

    Example
    -------
    >>> from pathlib import Path
    >>> input_path, output_path = Path('input.png'), Path('output.dxf')
    >>> output_path.write_bytes(convert_buffer(input_path.read_bytes()))
    output.dxf

    See Also
    --------
    segmentation_dxf.convert : Underlying convert
    """
    data = np.frombuffer(buffer, dtype=np.uint8)
    image = cv.imdecode(data, cv.IMREAD_COLOR)

    doc = segmentation_dxf.convert(image)

    output_stream = io.StringIO()
    doc.write(output_stream)

    output_buffer = bytes(output_stream.getvalue(), encoding='utf-8')

    return output_buffer
