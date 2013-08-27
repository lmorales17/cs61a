def find_centroid(polygon):
    """Find the centroid of a polygon.

    http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

    polygon -- A list of positions, in which the first and last are the same

    Returns: 3 numbers; centroid latitude, centroid longitude, and polygon area

    Hint: If a polygon has 0 area, return its first position as its centroid

    >>> p1, p2, p3 = make_position(1, 2), make_position(3, 4), make_position(5, 0)
    >>> triangle = [p1, p2, p3, p1]  # First vertex is also the last vertex
    >>> find_centroid(triangle)
    (3.0, 2.0, 6.0)
    >>> find_centroid([p1, p3, p2, p1])
    (3.0, 2.0, 6.0)
    >>> tuple(map(float, find_centroid([p1, p2, p1]))) # Forces result to be floats
    (1.0, 2.0, 0.0)
    """
    total_a = 0
    total_x = 0
    total_y = 0
    n = len(polygon) - 1
    i = 0
    j = 0
    k = n
    area = 0
    while k > 0: #calculates the area of the polygon
        x1 = polygon[k-1][0]
        y1 = polygon[k][1]
        x2 = polygon[k][0]
        y2 = polygon[k-1][1]
        summation = ((x1*y1)-(x2*y2))
        total_a += summation
        k -= 1
    area = (total_a/2)
    while  i < n: #calculates x-coordinate of the centroid
        z1 = polygon[i][0]
        w1 = polygon[i+1][1]
        z2 = polygon[i+1][0]
        w2 = polygon[i][1]
        summation1 = (z1+z2)*(z1*w1-z2*w2)
        total_x += summation1
        i += 1
    while j < n: #calculates y-coordinate of the centroid
        v1 = polygon[j][0]
        n1 = polygon[j+1][1]
        v2 = polygon[j+1][0]
        n2 = polygon[j][1]
        summation2 = (n2+n1)*(v1*n1-v2*n2)
        total_y += summation2
        j += 1
    if area == 0:
        return (polygon[0][0], polygon[0][1], abs(area))
    else:
        area_divider = (1/(6*area))
        x_coordinate = total_x*area_divider
        y_coordinate = total_y*area_divider
        return (x_coordinate, y_coordinate, abs(area))
