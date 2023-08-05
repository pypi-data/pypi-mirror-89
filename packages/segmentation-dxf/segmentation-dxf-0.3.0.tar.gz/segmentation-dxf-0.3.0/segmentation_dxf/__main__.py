if __name__ == '__main__':
    import segmentation_dxf

    import argparse

    parser = argparse.ArgumentParser(
        description='Convert segmentation to DXF'
    )

    parser.add_argument(
        'filename',
        help='Filename of the segmentation'
    )

    args = parser.parse_args()

    output_path = segmentation_dxf.convert_filename(args.filename)

    print(output_path)
