import cv2 as cv

import ezdxf


def convert(image):
    """
    Converts an image of a segmentation to a DXF drawing
    containing its contours.

    Parameters
    ----------
    image : nd.array
        shape=(width, height, depth)

    Returns
    -------
    drawing : ezdxf.Drawing
        red layer: image edges
        white layer: segmentation contour
    """
    white = 7
    red = 13

    road_contours_color = white
    image_edges_color = red

    drawing = ezdxf.new(setup=True)
    msp = drawing.modelspace()
    drawing.layers.new(
        name='RoadContours',
        dxfattribs={
            'linetype': 'CONTINUOUS',
            'color': road_contours_color,
        }
    )
    drawing.layers.new(
        name='ImageEdges',
        dxfattribs={
            'linetype': 'CONTINUOUS',
            'color': image_edges_color,
        }
    )

    width, height, _ = image.shape

    msp.add_lwpolyline(
        [(0, 0), (height, 0), (height, -width), (0, -width), (0, 0)],
        dxfattribs={
            'layer': 'ImageEdges',
        }
    )
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    _, threshold = cv.threshold(image_gray, 127, 255, 0)
    contours, _ = cv.findContours(
        threshold,
        cv.RETR_TREE,
        cv.CHAIN_APPROX_SIMPLE
    )
    for contour in contours:
        points_x = []
        points_y = []
        for point in contour:
            x = point[0][0]
            y = -point[0][1]
            points_x.append(x)
            points_y.append(y)

        points_x.append(contour[0][0][0])
        points_y.append(-contour[0][0][1])
        points = list(zip(points_x, points_y))

        msp.add_lwpolyline(
            points,
            dxfattribs={
                'layer': 'RoadContours',
            }
        )

    return drawing
