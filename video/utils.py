def in_rect(pos, corner, size):
    """
    Check if point is inside rectangle
    @param pos: point to be checked
    @param corner: upper left corner rectangle
    @param size: rect size
    @return:
    """
    x, y = pos
    rx, ry = corner
    w, h = size
    return rx <= x <= rx + w and ry <= y <= ry + h
