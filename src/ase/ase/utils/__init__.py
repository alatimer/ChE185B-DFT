import errno
import os
import sys
import time
from math import sin, cos, radians, atan2, degrees
from contextlib import contextmanager

try:
    from math import gcd
except ImportError:
    from fractions import gcd

import numpy as np

from ase.data import chemical_symbols

__all__ = ['exec_', 'basestring', 'import_module', 'seterr', 'plural',
           'devnull', 'gcd', 'convert_string_to_fd', 'Lock',
           'opencew', 'OpenLock', 'hill', 'rotate', 'irotate', 'givens',
           'hsv2rgb', 'hsv']


# Python 2+3 compatibility stuff:
if sys.version_info[0] == 3:
    import builtins
    exec_ = getattr(builtins, 'exec')
    basestring = str
    from io import StringIO
else:
    def exec_(code, dct):
        exec('exec code in dct')
    basestring = basestring
    from StringIO import StringIO
StringIO  # appease pyflakes

if sys.version_info >= (2, 7):
    from importlib import import_module
else:
    # Python 2.6:
    def import_module(name):
        module = __import__(name)
        for part in name.split('.')[1:]:
            module = getattr(module, part)
        return module


@contextmanager
def seterr(**kwargs):
    """Set how floating-point errors are handled.

    See np.seterr() for more details.
    """
    old = np.seterr(**kwargs)
    yield
    np.seterr(**old)


def plural(n, word):
    if n == 1:
        return '1 ' + word
    return '%d %ss' % (n, word)


class DevNull:
    encoding = 'UTF-8'

    def write(self, string):
        pass

    def flush(self):
        pass

    def seek(self, offset, whence=0):
        return 0

    def tell(self):
        return 0

    def close(self):
        pass

    def isatty(self):
        return False


devnull = DevNull()


def convert_string_to_fd(name, world=None):
    """Create a file-descriptor for text output.

    Will open a file for writing with given name.  Use None for no output and
    '-' for sys.stdout.
    """
    if world is None:
        from ase.parallel import world
    if name is None or world.rank != 0:
        return devnull
    if name == '-':
        return sys.stdout
    if isinstance(name, basestring):
        return open(name, 'w')
    return name  # we assume name is already a file-descriptor


# Only Windows has O_BINARY:
CEW_FLAGS = os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, 'O_BINARY', 0)


def opencew(filename, world=None):
    """Create and open filename exclusively for writing.

    If master cpu gets exclusive write access to filename, a file
    descriptor is returned (a dummy file descriptor is returned on the
    slaves).  If the master cpu does not get write access, None is
    returned on all processors."""

    if world is None:
        from ase.parallel import world

    if world.rank == 0:
        try:
            fd = os.open(filename, CEW_FLAGS)
        except OSError as ex:
            error = ex.errno
        else:
            error = 0
            fd = os.fdopen(fd, 'wb')
    else:
        error = 0
        fd = devnull

    # Syncronize:
    error = world.sum(error)
    if error == errno.EEXIST:
        return None
    if error:
        raise OSError(error, 'Error', filename)
    return fd


class Lock:
    def __init__(self, name='lock', world=None):
        self.name = name

        if world is None:
            from ase.parallel import world
        self.world = world

    def acquire(self):
        while True:
            fd = opencew(self.name, self.world)
            if fd is not None:
                break
            time.sleep(1.0)

    def release(self):
        self.world.barrier()
        if self.world.rank == 0:
            os.remove(self.name)

    def __enter__(self):
        self.acquire()

    def __exit__(self, type, value, tb):
        self.release()


class OpenLock:
    def acquire(self):
        pass

    def release(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self, type, value, tb):
        pass


def hill(numbers):
    """Convert list of atomic numbers to a chemical formula as a string.

    Elements are alphabetically ordered with C and H first."""

    if isinstance(numbers, dict):
        count = dict(numbers)
    else:
        count = {}
        for Z in numbers:
            symb = chemical_symbols[Z]
            count[symb] = count.get(symb, 0) + 1
    result = [(s, count.pop(s)) for s in 'CH' if s in count]
    result += [(s, count[s]) for s in sorted(count)]
    return ''.join('{0}{1}'.format(symbol, n) if n > 1 else symbol
                   for symbol, n in result)


def rotate(rotations, rotation=np.identity(3)):
    """Convert string of format '50x,-10y,120z' to a rotation matrix.

    Note that the order of rotation matters, i.e. '50x,40z' is different
    from '40z,50x'.
    """

    if rotations == '':
        return rotation.copy()

    for i, a in [('xyz'.index(s[-1]), radians(float(s[:-1])))
                 for s in rotations.split(',')]:
        s = sin(a)
        c = cos(a)
        if i == 0:
            rotation = np.dot(rotation, [(1, 0, 0),
                                         (0, c, s),
                                         (0, -s, c)])
        elif i == 1:
            rotation = np.dot(rotation, [(c, 0, -s),
                                         (0, 1, 0),
                                         (s, 0, c)])
        else:
            rotation = np.dot(rotation, [(c, s, 0),
                                         (-s, c, 0),
                                         (0, 0, 1)])
    return rotation


def givens(a, b):
    """Solve the equation system::

      [ c s]   [a]   [r]
      [    ] . [ ] = [ ]
      [-s c]   [b]   [0]
    """
    sgn = np.sign
    if b == 0:
        c = sgn(a)
        s = 0
        r = abs(a)
    elif abs(b) >= abs(a):
        cot = a / b
        u = sgn(b) * (1 + cot**2)**0.5
        s = 1. / u
        c = s * cot
        r = b * u
    else:
        tan = b / a
        u = sgn(a) * (1 + tan**2)**0.5
        c = 1. / u
        s = c * tan
        r = a * u
    return c, s, r


def irotate(rotation, initial=np.identity(3)):
    """Determine x, y, z rotation angles from rotation matrix."""
    a = np.dot(initial, rotation)
    cx, sx, rx = givens(a[2, 2], a[1, 2])
    cy, sy, ry = givens(rx, a[0, 2])
    cz, sz, rz = givens(cx * a[1, 1] - sx * a[2, 1],
                        cy * a[0, 1] - sy * (sx * a[1, 1] + cx * a[2, 1]))
    x = degrees(atan2(sx, cx))
    y = degrees(atan2(-sy, cy))
    z = degrees(atan2(sz, cz))
    return x, y, z


def hsv2rgb(h, s, v):
    """http://en.wikipedia.org/wiki/HSL_and_HSV

    h (hue) in [0, 360[
    s (saturation) in [0, 1]
    v (value) in [0, 1]

    return rgb in range [0, 1]
    """
    if v == 0:
        return 0, 0, 0
    if s == 0:
        return v, v, v

    i, f = divmod(h / 60., 1)
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))

    if i == 0:
        return v, t, p
    elif i == 1:
        return q, v, p
    elif i == 2:
        return p, v, t
    elif i == 3:
        return p, q, v
    elif i == 4:
        return t, p, v
    elif i == 5:
        return v, p, q
    else:
        raise RuntimeError('h must be in [0, 360]')


def hsv(array, s=.9, v=.9):
    array = (array + array.min()) * 359. / (array.max() - array.min())
    result = np.empty((len(array.flat), 3))
    for rgb, h in zip(result, array.flat):
        rgb[:] = hsv2rgb(h, s, v)
    return np.reshape(result, array.shape + (3,))

# This code does the same, but requires pylab
# def cmap(array, name='hsv'):
#     import pylab
#     a = (array + array.min()) / array.ptp()
#     rgba = getattr(pylab.cm, name)(a)
#     return rgba[:-1] # return rgb only (not alpha)


def longsum(x):
    """128-bit floating point sum."""
    return float(np.asarray(x, dtype=np.longdouble).sum())
