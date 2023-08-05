from pathlib import Path

import segmentation_dxf


def convert_filename(path):
    """
    Converts a segmentation file to a DXF drawing file.

    Parameters
    ----------
    path : Path | str
        Input filename.

    Returns
    -------
    output_path : Path
        Output filename. <input-directory>/exported/<input-name>.dxf
    """
    path = Path(path)
    path_directory = path.parent
    export_directory = path_directory / 'exported'
    export_directory.mkdir(exist_ok=True)

    output_path = Path(str(export_directory / path.stem) + '.dxf')

    output = segmentation_dxf.convert_buffer(path.read_bytes())

    output_path.write_bytes(output)

    return output_path
