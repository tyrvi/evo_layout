from shapely.geometry import Polygon


class Layout:
    """
    The polygon which represents the outer walls of the building.
    """
    def __init__(self, points=[]):
        """
        Parameters
        ----------
        points : List of [x, y] coordinates
        """
        self.points = points

    def get_shapely_polygon(self):
        return Polygon(self.points)

    def contains(self, vertex):
        """
        Check if the vertex is contained within the polygon.
        """
        raise NotImplementedError("Bound has not been implemented yet.")
