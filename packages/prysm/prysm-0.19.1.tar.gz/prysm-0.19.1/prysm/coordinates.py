"""Coordinate conversions."""
from .conf import config
from .mathops import np, interpolate_engine as interpolate


def cart_to_polar(x, y):
    '''Return the (rho,phi) coordinates of the (x,y) input points.

    Parameters
    ----------
    x : `numpy.ndarray` or number
        x coordinate
    y : `numpy.ndarray` or number
        y coordinate

    Returns
    -------
    rho : `numpy.ndarray` or number
        radial coordinate
    phi : `numpy.ndarray` or number
        azimuthal coordinate

    '''
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def polar_to_cart(rho, phi):
    '''Return the (x,y) coordinates of the (rho,phi) input points.

    Parameters
    ----------
    rho : `numpy.ndarray` or number
        radial coordinate
    phi : `numpy.ndarray` or number
        azimuthal coordinate

    Returns
    -------
    x : `numpy.ndarray` or number
        x coordinate
    y : `numpy.ndarray` or number
        y coordinate

    '''
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def uniform_cart_to_polar(x, y, data):
    """Interpolate data uniformly sampled in cartesian coordinates to polar coordinates.

    Parameters
    ----------
    x : `numpy.ndarray`
        sorted 1D array of x sample pts
    y : `numpy.ndarray`
        sorted 1D array of y sample pts
    data : `numpy.ndarray`
        data sampled over the (x,y) coordinates

    Returns
    -------
    rho : `numpy.ndarray`
        samples for interpolated values
    phi : `numpy.ndarray`
        samples for interpolated values
    f(rho,phi) : `numpy.ndarray`
        data uniformly sampled in (rho,phi)

    """
    # create a set of polar coordinates to interpolate onto
    xmin, xmax = x.min(), x.max()
    ymin, ymax = y.min(), y.max()

    _max = max(abs(np.asarray([xmin, xmax, ymin, ymax])))

    rho = np.linspace(0, _max, len(x))
    phi = np.linspace(0, 2 * np.pi, len(y))
    rv, pv = np.meshgrid(rho, phi)

    # map points to x, y and make a grid for the original samples
    xv, yv = polar_to_cart(rv, pv)

    # interpolate the function onto the new points
    f = interpolate.RegularGridInterpolator((y, x), data, bounds_error=False, fill_value=0)
    return rho, phi, f((yv, xv), method='linear')


def resample_2d(array, sample_pts, query_pts, kind='cubic'):
    """Resample 2D array to be sampled along queried points.

    Parameters
    ----------
    array : `numpy.ndarray`
        2D array
    sample_pts : `tuple`
        pair of `numpy.ndarray` objects that contain the x and y sample locations,
        each array should be 1D
    query_pts : `tuple`
        points to interpolate onto, also 1D for each array
    kind : `str`, {'linear', 'cubic', 'quintic'}
        kind / order of spline to use

    Returns
    -------
    `numpy.ndarray`
        array resampled onto query_pts

    """
    interpf = interpolate.interp2d(*sample_pts, array, kind=kind)
    return interpf(*query_pts)


def resample_2d_complex(array, sample_pts, query_pts, kind='linear'):
    """Resample 2D array to be sampled along queried points.

    Parameters
    ----------
    array : `numpy.ndarray`
        2D array
    sample_pts : `tuple`
        pair of `numpy.ndarray` objects that contain the x and y sample locations,
        each array should be 1D
    query_pts : `tuple`
        points to interpolate onto, also 1D for each array
    kind : `str`, {'linear', 'cubic', 'quintic'}
        kind / order of spline to use

    Returns
    -------
    `numpy.ndarray`
        array resampled onto query_pts

    """
    r, c = [resample_2d(a,
                        sample_pts=sample_pts,
                        query_pts=query_pts,
                        kind=kind) for a in (array.real, array.imag)]

    return r + 1j * c


def make_xy_grid(samples_x, samples_y=None, radius=1):
    """Create an x, y grid from -1, 1 with n number of samples.

    Parameters
    ----------
    samples_x : `int`
        number of samples in x direction
    samples_y : `int`
        number of samples in y direction, if None, copied from sample_x
    radius : `float`
        radius of the output array, will span -radius, radius

    Returns
    -------
    xx : `numpy.ndarray`
        x meshgrid
    yy : `numpy.ndarray`
        y meshgrid

    """
    if samples_y is None:
        samples_y = samples_x
    x = np.linspace(-radius, radius, samples_x, dtype=config.precision)
    y = np.linspace(-radius, radius, samples_y, dtype=config.precision)
    xx, yy = np.meshgrid(x, y)
    return xx, yy


def make_rho_phi_grid(samples_x, samples_y=None, aligned='x', radius=1):
    """Create an rho, phi grid from -1, 1 with n number of samples.

    Parameters
    ----------
    samples_x : `int`
        number of samples in x direction
    samples_y : `int`
        number of samples in y direction, if None, copied from sample_x
    radius : `float`
        radius of the output array

    Returns
    -------
    rho : `numpy.ndarray`
        radial meshgrid
    phi : `numpy.ndarray`
        angular meshgrid

    """
    xx, yy = make_xy_grid(samples_x, samples_y, radius)
    if aligned == 'x':
        rho, phi = cart_to_polar(xx, yy)
    else:
        rho, phi = cart_to_polar(yy, xx)
    return rho, phi


def v_to_2v_minus_one(v):
    """Transform v -> 2v-1."""
    return 2 * v - 1


def v_to_2v2_minus_one(v):
    """Transform v -> 2v^2-1."""
    return 2 * v ** 2 - 1


def v_to_v_squared(v):
    """Transform v -> v^2."""
    return v ** 2


def v_to_v_fouth(v):
    """Transform v -> v^4."""
    return v ** 4


def v_to_v2_times_1_minus_v2(v):
    """Transform v -> v^2(1 - v^2)."""
    v2 = v ** 2
    return v2 * (1 - v2)


def v_to_4v2_minus_4v_plus1(v):
    """Transform v -> (4v)^2 - 4v - 1."""
    v4 = 4 * v
    return v4 * v4 - v4 + 1


def v_to_v_plus90(v):
    """Transform v -> v+90 deg, v should be in radians."""
    return v - (np.pi/2)
    # return v


def convert_transformation_to_v(transformation):
    """Replace any of x,y,r,t with v in a transformation string."""
    s = transformation
    for letter in ('x', 'y', 'r', 't'):
        s = s.replace(letter, 'v')

    return s


class GridCache:
    """Cache of grid points."""
    def __init__(self):
        """Create a new GridCache instance."""
        self.grids = {}
        self.transformation_functions = {
            'v -> 4v^2 - 4v + 1': v_to_4v2_minus_4v_plus1,
            'v -> v^2 (1-v^2)': v_to_v2_times_1_minus_v2,
            'v -> 2v^2 - 1': v_to_2v2_minus_one,
            'v -> 2v - 1': v_to_2v_minus_one,
            'v -> v^2': v_to_v_squared,
            'v -> v^4': v_to_v_fouth,
            'v -> v+90': v_to_v_plus90
        }

    def make_basic_grids(self, samples, radius):
        """Create basic (unmodified) grids.

        Parameters
        ----------
        samples : `int`
            number of samples in the square grid
        radius : `float`
            radius of the array in units (not samples)

        """
        x, y = make_xy_grid(samples, radius=radius)
        r, t = cart_to_polar(x, y)
        self.grids[(samples, radius)] = {
            'original': {
                'x': x,
                'y': y,
                'r': r,
                't': t,
            },
            'transformed': {}
        }

    def make_transformation(self, samples, radius, transformation):
        """Make a transformed grid.

        Parameters
        ----------
        samples : `int`
            number of samples in the square grid
        radius : `float`
            radius of the array in units (not samples)
        transformation : `str`
            looks like "r => 2r^2 - 1"

        """
        # transformation looks like "r -> 2r^2 - 1"
        # first letter is the variable
        var = transformation[0]
        trans2 = convert_transformation_to_v(transformation)

        # the string is a key into a registry of functions
        func = self.transformation_functions[trans2]

        # there is a cache of this shape and radius,
        # get the original variable and make/store the transformation
        original = self.get_original_variable(samples, radius, var)
        transformed = func(original)
        self.grids[(samples, radius)]['transformed'][transformation] = transformed

    def get_original_variable(self, samples, radius, variable):
        """Retrieve an unmodified variable.

        Parameters
        ----------
        samples : `int`
            number of samples in the square grid
        radius : `float`
            radius of the array in units (not samples)
        variable : `str`, {'x', 'y', 'r', 'p'}
            which variable on the grid

        Returns
        -------
        `numpy.ndarray`
            array of shape (samples,samples)

        """
        outer = self.grids.get((samples, radius), None)
        if outer is None:
            self.make_basic_grids(samples, radius)
            outer = self.grids.get((samples, radius), None)

        return outer['original'][variable]

    def get_transformed_variable(self, samples, radius, transformation):
        """Retrieve a modified variable.

        Parameters
        ----------
        samples : `int`
            number of samples in the square grid
        radius : `float`
            radius of the array in units (not samples)
        variable : `str`, {'x', 'y', 'r', 't'}
            which variable on the grid
        transformation : `str`
            looks like "r => 2r^2 - 1"

        Returns
        -------
        `numpy.ndarray`
            array of shape (samples,samples)

        """
        outer = self.grids.get((samples, radius), None)
        if outer is None:
            self.make_transformation(samples, radius, transformation)
            outer = self.grids.get((samples, radius), None)

        try:
            return outer['transformed'][transformation]
        except KeyError:
            # not DRY, doesn't really matter over 2 lines
            self.make_transformation(samples, radius, transformation)
            outer = self.grids.get((samples, radius), None)
            return outer['transformed'][transformation]

    def get_variable_transformed_or_not(self, samples, radius, variable_or_transformation):
        """Retrieve a modified variable.

        Parameters
        ----------
        samples : `int`
            number of samples in the square grid
        radius : `float`
            radius of the array in units (not samples)
        variable_or_transformation : `str` or None
            looks like "r => 2r^2 - 1" for a transformation, or "r" for a variable
            if None, returns None

        Returns
        -------
        `numpy.ndarray`
            array of shape (samples,samples)

        """
        if variable_or_transformation is None:
            return None
        elif len(variable_or_transformation) > 1:
            return self.get_transformed_variable(samples, radius, variable_or_transformation)
        else:
            return self.get_original_variable(samples, radius, variable_or_transformation)

    def __call__(self, samples, radius, x=None, y=None, r=None, t=None):
        """Retrieve a modified variable.

        Parameters
        ----------
        samples : `int`
            number of samples in the square grid
        radius : `float`
            radius of the array in units (not samples)
        x : `str`, optional
            either 'x' or a transformation string which looks like "r => 2r^2 - 1"
        y : `str`, optional
            either 'y' or a transformation string which looks like "r => 2r^2 - 1"
        r : `str`, optional
            either 'r' or a transformation string which looks like "r => 2r^2 - 1"
        t : `str`, optional
            either 't' or a transformation string which looks like "r => 2r^2 - 1"
        transformation : `str`
            looks like "r => 2r^2 - 1"

        Returns
        -------
        `dict`
            has keys x,y,r,t which are 2D arrays of shape (samples,samples)

        """
        return {
            'x': self.get_variable_transformed_or_not(samples, radius, x),
            'y': self.get_variable_transformed_or_not(samples, radius, y),
            'r': self.get_variable_transformed_or_not(samples, radius, r),
            't': self.get_variable_transformed_or_not(samples, radius, t),
        }

    def clear(self):
        """Empty the cache."""
        self.grids = {}


gridcache = GridCache()
