class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def translated(self, x, y):
        return Point(self.x+x, self.y+y)

    def to_tuple(self):
        return self.x, self.y


class Rect:
    def __init__(self, origin: Point, width: int, height: int):
        self.origin = origin
        self.width = width
        self.height = height

    def in_bounds(self, p: Point):
        return self.origin.x <= p.x < self.origin.x+self.width and self.origin.y <= p.y < self.origin.y+self.height

    def overlaps(self, other):
        if other.origin.x > self.origin.x+self.width or \
           other.origin.y > self.origin.y+self.height or \
           other.origin.x+other.width < self.origin.x or \
           other.origin.y+other.height < self.origin.y:
            return False
        return True

    def to_tuple(self):
        return self.origin.x, self.origin.y, self.width, self.height


class QuadTree:
    def __init__(self, boundary: Rect, capacity: int):
        self.boundary = boundary
        self.capacity = capacity
        self.points = set()
        self.is_split = False
        self.subtreeNE = None
        self.subtreeNW = None
        self.subtreeSE = None
        self.subtreeSW = None

    def split(self):
        self.subtreeNE = QuadTree(
            Rect(self.boundary.origin,
                 int(self.boundary.width / 2), int(self.boundary.height / 2)),
            self.capacity
        )
        self.subtreeNW = QuadTree(
            Rect(self.boundary.origin.translated(self.boundary.width / 2, 0),
                 int(self.boundary.width / 2), int(self.boundary.height / 2)),
            self.capacity
        )
        self.subtreeSE = QuadTree(
            Rect(self.boundary.origin.translated(0, self.boundary.height / 2),
                 int(self.boundary.width / 2), int(self.boundary.height / 2)),
            self.capacity
        )
        self.subtreeSW = QuadTree(
            Rect(self.boundary.origin.translated(self.boundary.width / 2, self.boundary.height / 2),
                 int(self.boundary.width / 2), int(self.boundary.height / 2)),
            self.capacity
        )
        self.is_split = True

    def insert_point(self, p: Point):
        if not self.boundary.in_bounds(p):
            return

        if len(self.points) < self.capacity:
            self.points.add(p)
        else:
            if not self.is_split:
                self.split()

            self.subtreeNE.insert_point(p)
            self.subtreeNW.insert_point(p)
            self.subtreeSE.insert_point(p)
            self.subtreeSW.insert_point(p)

    def get_all(self):
        yield self.boundary, self.points
        if self.is_split:
            for boundary, points in self.subtreeNE.get_all():
                yield boundary, points
            for boundary, points in self.subtreeNW.get_all():
                yield boundary, points
            for boundary, points in self.subtreeSE.get_all():
                yield boundary, points
            for boundary, points in self.subtreeSW.get_all():
                yield boundary, points

    def get_points_in_area(self, area: Rect, out=None):
        if out is None:
            out = []

        if not self.boundary.overlaps(area):
            return

        for p in self.points:
            if area.in_bounds(p):
                out.append(p)

        if self.is_split:
            self.subtreeNE.get_points_in_area(area, out)
            self.subtreeNW.get_points_in_area(area, out)
            self.subtreeSE.get_points_in_area(area, out)
            self.subtreeSW.get_points_in_area(area, out)

        return out
