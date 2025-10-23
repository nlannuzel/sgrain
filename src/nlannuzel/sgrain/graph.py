"""Classes for basic in-memory image handling"""

class Color:
    """A color stored as either a grey level, or red, green, blue 8
    bits components"""
    def __init__(self, r, g, b):
        """Build a new Color object from r, g, and b components
        between 0 and 255"""

        if r is None or g is None or b is None:
            raise Exception("some colors are missing")
        for c in (r, g, b):
            if c < 0:
                raise Exception("color cannot be negative")
            if c > 255:
                raise Exception("only 8 bits is supported")
        if r == b and r == g and b == g:
            # grey level
            self.g = g
            self.r = None
            return
        self.r = r
        self.g = g
        self.b = b

    def is_grey(self):
        return self.r is None

    def __repr__(self):
        if self.is_grey():
            return f"Color({self.g})"
        return f"Color({self.r},{self.r},{self.b})"

    def distance_to(self, other):
        """returns the distance between this color and another one"""
        if self.is_grey():
            if other.is_grey():
                return ( 3*(other.g - self.g)**2 )**0.5
            return ((other.r - self.g)**2 + (other.g - self.g)**2 + (other.b - self.g)**2)**0.5
        if other.is_grey():
            return ((other.g - self.r)**2 + (other.g - self.g)**2 + (other.g - self.g)**2)**0.5
        return ((other.r - self.r)**2 + (other.g - self.g)**2 + (other.b - self.b)**2)**0.5

    def posterize(self, palette):
        """find the closest color in a palette, and return the index
        of the color in the palette.

        parameters:
          palette: tuples of Color
        returns:
          position of the nearest color in the palette
        """
        min_d = None
        for i in range(0, len(palette)):
            d = self.distance_to(palette[i])
            if min_d is None or min_d > d:
                min_d = d
                min_i = i
        return min_i

    @classmethod
    def grey(cls, level):
        """returns a grey level from black to white"""
        return cls(level, level, level)

BLACK   = Color( 0  , 0  , 0   )
WHITE   = Color( 255, 255, 255 )
RED     = Color( 255, 0  , 0   )
GREEN   = Color( 0  , 255, 0   )
BLUE    = Color( 0  , 0  , 255 )
YELLOW  = Color( 255, 255, 0   )
PURPLE  = Color( 255, 0  , 255 )
CYAN    = Color( 0  , 255, 255 )

class Pixel:
    """A set of i and j coordinates, and optionally a Color"""
    def __init__(self, i, j, col = None):
        if i < 0 or j < 0:
            raise Exception("coordinates cannot be negative")
        self.i = i
        self.j = j
        self.col = col

    def __repr__(self):
        s = f"Pixel({self.i},{self.j})"
        if self.col is not None:
            s += f" = {self.col}"
        return s

class Box:
    """an area in the image represented by two pixels at the top-left
    (tl) and bottom-right (br)"""
    def __init__(self, tl, br):
        if br.i <= tl.i or br.j <= tl.j:
            raise RuntimeError("invalid box")
        self.tl = tl
        self.br = br

    @classmethod
    def from_coordinates(cls, ia, ja, ib, jb):
        tl = Pixel(i = ia, j = ja)
        br = Pixel(i = ib, j = jb)
        return Box(tl, br)

    def iter_width(self):
        """returns an iterator on the width of this box"""
        return range(self.tl.i, self.br.i+1)
    def iter_height(self):
        """returns an iterator on the height of this box"""
        return range(self.tl.j, self.br.j+1)
    def iter_area(self):
        """returns an iterator on all the coordinates making up the
        inside and boundary of this box"""
        for j in self.iter_height():
            for i in self.iter_width():
                yield([i, j])
    def iter_boundary(self):
        """returns an iterator on all the coordinates making up
        boundary of this box"""
        for j in self.iter_height():
            yield([self.tl.i, j])
            yield([self.br.i, j])
        for i in range(self.tl.i + 1, self.br.i):
            yield([i, self.tl.j])
            yield([i, self.br.j])

class Image:
    """a 8 bits image in memory stored as rows of Color"""
    def __init__(self, width = None, height = None, rows = None):
        """

        parameters:
          width and height: dimensions of the image
          rows: list of list of Color object

        Either (width and height) or rows are needed.
        If width and height are given, rows is initialized as a all
        black image.
        If rows is given, width and height are calculated from the
        number of rows, and length of each row.
        """
        if rows is None:
            if width is None or height is None:
                raise RuntimeError("at least width and height or rows must be given")
            rows = []
            for j in range(0, height):
                row = []
                row.extend([ BLACK for i in range(0, width) ])
                rows.append(row)
        self.rows = rows
        self.height = len(rows)
        self.width = len(rows[0])

    def __repr__(self):
        return f"Image ({self.width}x{self.height})"

    @classmethod
    def from_rgb_rows(cls, rows, has_alpha = False):
        """generate a new image from a list of (r, g, b, r, g, b...)
        lists instead of list of list Color"""
        skip = 4 if has_alpha else 3
        new_rows = []
        for row in rows:
            new_row = [ Color(row[i], row[i+1], row[i+2]) for i in range(0, len(row), skip) ]
            new_rows.append(new_row)
        return Image(rows = new_rows)

    def to_rgb_rows(self):
        """export the image as a list of (r, g, b, r, g, b...) lists
        """
        rows = []
        for row in self.rows:
            new_row = []
            for i in range(0, len(row)):
                new_row.extend([row[i].r, row[i].g, row[i].b])
            rows.append(new_row)
        return rows

    def get_color_at(self, i, j):
        """Return the color at location (i, j) as a Color object"""
        return self.rows[j][i]

    def set_color_at(self, i, j, col):
        """Set the color at location (i, j) to the given Color"""
        self.rows[j][i] = col

    def get_pixel_at(self, i, j):
        """Return the color at location (i, j) in the form of a new
        Pixel object"""
        return Pixel(i, j, self.get_color_at(i, j))

    def get_pixel(self, pixel):
        """Update the given Pixel object with the color stored at
        location(i, j)"""
        row = self.rows[pixel.j]
        pixel.col = self.get_color_at(pixel.i, pixel.j)
        return pixel

    def set_pixel(self, pixel):
        """Set the color at location (i, j) to the color set in the
        given Pixel object"""
        self.set_color_at(pixel.i, pixel.j, pixel.col)

    def iter_rectangle_area(self, box):
        """Returns an iterator on all pixels within the given box
        area"""
        for pos in box.iter_area():
            yield(self.get_pixel_at(pos[0], pos[1]))

    def iter_rectangle_boundary(self, box):
        """Returns an iterator on all pixels within the boundary of
        given box area"""
        for pos in box.iter_boundary():
            yield(self.get_pixel_at(pos[0], pos[1]))

    def iter_neighbours_r(self, pixel, d):
        """Returns an iterator on all pixels within a box (size d x d)
        centered on the given pixel"""
        if d <= 0:
            raise RuntimeError("d must be strictly positive")
        return self.iter_rectangle_area(Box.from_coordinates(
            max(0, pixel.i - d),
            max(0, pixel.j - d),
            min(self.width, pixel.i + d),
            min(self.height, pixel.j + d)))

    def iter_neighbours_r_boundary(self, pixel, d):
        """Returns an iterator on all pixels on the boundary of a box
        (size d x d) centered on the given pixel"""
        if d <= 0:
            raise RuntimeError("d must be strictly positive")
        return self.iter_rectangle_boundary(Box.from_coordinates(
            max(0, pixel.i - d),
            max(0, pixel.j - d),
            min(self.width, pixel.i + d),
            min(self.height, pixel.j + d)))

    def transform(self, func):
        """
        
        Apply functiopn `func` on all pixels of this image, and return a new image.
        `func` takes a Pixel object and must return a Color object.
        """
        new_image = Image(width = self.width, height = self.height)
        box = Box(Pixel(0, 0), Pixel(self.width - 1, self.height - 1))
        for pos in box.iter_area():
            i, j = pos
            pixel = self.get_pixel_at(i, j)
            new_image.set_color_at(i, j, func(pixel))
        return new_image
