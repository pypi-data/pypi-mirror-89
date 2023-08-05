"""
Core geodesic functions
=======================
This file is part of NavLab and is available from www.navlab.net/nvector

"""
from __future__ import division, print_function
import warnings
import numpy as np
from numpy import arctan2, sin, cos, cross, dot, sqrt
from numpy.linalg import norm
from nvector import _examples, license as _license
from nvector.rotation import E_rotation, n_E2R_EN, n_E2lat_lon  # @UnusedImport
from nvector.util import mdot, nthroot, unit, _check_length_deviation
from nvector._common import test_docstrings, use_docstring_from, _make_summary


__all__ = ['closest_point_on_great_circle',
           'cross_track_distance',
           'euclidean_distance',
           'great_circle_distance',
           'great_circle_normal',
           'interpolate',
           'intersect',
           'mean_horizontal_position',
           'lat_lon2n_E',
           'n_E2lat_lon',
           'n_EA_E_and_n_EB_E2p_AB_E',
           'n_EA_E_and_p_AB_E2n_EB_E',
           'n_EB_E2p_EB_E',
           'p_EB_E2n_EB_E',
           'n_EA_E_distance_and_azimuth2n_EB_E',
           'n_EA_E_and_n_EB_E2azimuth',
           'on_great_circle',
           'on_great_circle_path',
           ]


def lat_lon2n_E(latitude, longitude, R_Ee=None):
    """
    Converts latitude and longitude to n-vector.

    Parameters
    ----------
    latitude, longitude: real scalars or vectors of length n.
        Geodetic latitude and longitude given in [rad]
    R_Ee : 3 x 3 array
        rotation matrix defining the axes of the coordinate frame E.

    Returns
    -------
    n_E: 3 x n array
        n-vector(s) [no unit] decomposed in E.

    See also
    --------
    n_E2lat_lon
    """
    if R_Ee is None:
        R_Ee = E_rotation()
    # Equation (3) from Gade (2010):
    nvec = np.vstack((sin(latitude),
                      sin(longitude) * cos(latitude),
                      -cos(longitude) * cos(latitude)))
    n_E = dot(R_Ee.T, nvec)
    return n_E


class _Nvector2ECEFvector(object):
    __doc__ = """Converts n-vector to Cartesian position vector in meters.

Parameters
----------
n_EB_E:  3 x n array
    n-vector(s) [no unit] of position B, decomposed in E.
depth:  1 x n array
    Depth(s) [m] of system B, relative to the ellipsoid (depth = -height)
a: real scalar, default WGS-84 ellipsoid.
    Semi-major axis of the Earth ellipsoid given in [m].
f: real scalar, default WGS-84 ellipsoid.
    Flattening [no unit] of the Earth ellipsoid. If f==0 then spherical
    Earth with radius a is used in stead of WGS-84.
R_Ee : 3 x 3 array
    rotation matrix defining the axes of the coordinate frame E.

Returns
-------
p_EB_E:  3 x n array
    Cartesian position vector(s) from E to B, decomposed in E.

Notes
-----
The position of B (typically body) relative to E (typically Earth) is
given into this function as n-vector, n_EB_E. The function converts
to cartesian position vector ("ECEF-vector"), p_EB_E, in meters.
The calculation is exact, taking the ellipsity of the Earth into account.
It is also non-singular as both n-vector and p-vector are non-singular
(except for the center of the Earth).
The default ellipsoid model used is WGS-84, but other ellipsoids/spheres
might be specified.

Examples
--------
{0}

See also
--------
p_EB_E2n_EB_E, n_EA_E_and_p_AB_E2n_EB_E, n_EA_E_and_n_EB_E2p_AB_E
""".format(_examples.get_examples_no_header([4], OO=False))


@use_docstring_from(_Nvector2ECEFvector)
def n_EB_E2p_EB_E(n_EB_E, depth=0, a=6378137, f=1.0 / 298.257223563, R_Ee=None):
    if R_Ee is None:
        R_Ee = E_rotation()
    _check_length_deviation(n_EB_E)

    n_EB_E = unit(dot(R_Ee, n_EB_E))
    b = a * (1 - f)  # semi-minor axis

    # The following code implements equation (22) in Gade (2010):
    scale = np.vstack((1,
                       (1 - f),
                       (1 - f)))
    denominator = norm(n_EB_E / scale, axis=0)

    # We first calculate the position at the origin of coordinate system L,
    # which has the same n-vector as B (n_EL_E = n_EB_E),
    # but lies at the surface of the Earth (z_EL = 0).

    p_EL_E = b / denominator * n_EB_E / scale**2
    p_EB_E = dot(R_Ee.T, p_EL_E - n_EB_E * depth)

    return p_EB_E


class _ECEFvector2Nvector(object):
    __doc__ = """Converts Cartesian position vector in meters to n-vector.

Parameters
----------
p_EB_E:  3 x n array
    Cartesian position vector(s) from E to B, decomposed in E.
a: real scalar, default WGS-84 ellipsoid.
    Semi-major axis of the Earth ellipsoid given in [m].
f: real scalar, default WGS-84 ellipsoid.
    Flattening [no unit] of the Earth ellipsoid. If f==0 then spherical
    Earth with radius a is used in stead of WGS-84.
R_Ee : 3 x 3 array
    rotation matrix defining the axes of the coordinate frame E.

Returns
-------
n_EB_E:  3 x n array
    n-vector(s) [no unit] of position B, decomposed in E.
depth:  1 x n array
    Depth(s) [m] of system B, relative to the ellipsoid (depth = -height)


Notes
-----
The position of B (typically body) relative to E (typically Earth) is
given into this function as cartesian position vector p_EB_E, in meters.
("ECEF-vector"). The function converts to n-vector, n_EB_E and its
depth, depth.
The calculation is excact, taking the ellipsity of the Earth into account.
It is also non-singular as both n-vector and p-vector are non-singular
(except for the center of the Earth).
The default ellipsoid model used is WGS-84, but other ellipsoids/spheres
might be specified.

Examples
--------
{0}

See also
--------
n_EB_E2p_EB_E, n_EA_E_and_p_AB_E2n_EB_E, n_EA_E_and_n_EB_E2p_AB_E

""".format(_examples.get_examples_no_header([3], OO=False))


@use_docstring_from(_ECEFvector2Nvector)
def p_EB_E2n_EB_E(p_EB_E, a=6378137, f=1.0 / 298.257223563, R_Ee=None):
    if R_Ee is None:
        # R_Ee selects correct E-axes, see E_rotation for details
        R_Ee = E_rotation()
    p_EB_E = dot(R_Ee, p_EB_E)

    # e_2 = eccentricity**2
    e_2 = 2 * f - f**2  # = 1-b**2/a**2

    # The following code implements equation (23) from Gade (2010):
    R_2 = p_EB_E[1, :]**2 + p_EB_E[2, :]**2
    R = sqrt(R_2)   # R = component of p_EB_E in the equatorial plane

    p = R_2 / a**2
    q = (1 - e_2) / (a**2) * p_EB_E[0, :]**2
    r = (p + q - e_2**2) / 6

    s = e_2**2 * p * q / (4 * r**3)
    t = nthroot((1 + s + sqrt(s * (2 + s))), 3)
    # t = (1 + s + sqrt(s * (2 + s)))**(1. / 3)
    u = r * (1 + t + 1. / t)
    v = sqrt(u**2 + e_2**2 * q)

    w = e_2 * (u + v - q) / (2 * v)
    k = sqrt(u + v + w**2) - w
    d = k * R / (k + e_2)

    temp0 = sqrt(d**2 + p_EB_E[0, :]**2)
    # Calculate height:
    height = (k + e_2 - 1) / k * temp0

    temp1 = 1. / temp0
    temp2 = temp1 * k / (k + e_2)

    n_EB_E_x = temp1 * p_EB_E[0, :]
    n_EB_E_y = temp2 * p_EB_E[1, :]
    n_EB_E_z = temp2 * p_EB_E[2, :]

    n_EB_E = np.vstack((n_EB_E_x, n_EB_E_y, n_EB_E_z))
    n_EB_E = unit(dot(R_Ee.T, n_EB_E))  # Ensure unit length

    depth = -height
    return n_EB_E, depth


class _DeltaFromPositionAtoB(object):
    __doc__ = """Returns the delta vector from position A to B decomposed in E.

Parameters
----------
n_EA_E, n_EB_E:  3 x n array
    n-vector(s) [no unit] of position A and B, decomposed in E.
z_EA, z_EB:  1 x n array
    Depth(s) [m] of system A and B, relative to the ellipsoid.
    (z_EA = -height, z_EB = -height)
a: real scalar, default WGS-84 ellipsoid.
    Semi-major axis of the Earth ellipsoid given in [m].
f: real scalar, default WGS-84 ellipsoid.
    Flattening [no unit] of the Earth ellipsoid. If f==0 then spherical
    Earth with radius a is used in stead of WGS-84.
R_Ee : 3 x 3 array
    rotation matrix defining the axes of the coordinate frame E.

Returns
-------
p_AB_E:  3 x n array
    Cartesian position vector(s) from A to B, decomposed in E.

Notes
-----
The n-vectors for positions A (n_EA_E) and B (n_EB_E) are given. The
output is the delta vector from A to B (p_AB_E).
The calculation is excact, taking the ellipsity of the Earth into account.
It is also non-singular as both n-vector and p-vector are non-singular
(except for the center of the Earth).
The default ellipsoid model used is WGS-84, but other ellipsoids/spheres
might be specified.

Examples
--------
{0}


See also
--------
n_EA_E_and_p_AB_E2n_EB_E, p_EB_E2n_EB_E, n_EB_E2p_EB_E

""".format(_examples.get_examples_no_header([1], False))


@use_docstring_from(_DeltaFromPositionAtoB)
def n_EA_E_and_n_EB_E2p_AB_E(n_EA_E, n_EB_E, z_EA=0, z_EB=0, a=6378137,
                             f=1.0 / 298.257223563, R_Ee=None):

    # Function 1. in Section 5.4 in Gade (2010):
    p_EA_E = n_EB_E2p_EB_E(n_EA_E, z_EA, a, f, R_Ee)
    p_EB_E = n_EB_E2p_EB_E(n_EB_E, z_EB, a, f, R_Ee)
    p_AB_E = p_EB_E - p_EA_E
    return p_AB_E


def n_EA_E_and_p_AB_E2n_EB_E(n_EA_E, p_AB_E, z_EA=0, a=6378137,
                             f=1.0 / 298.257223563, R_Ee=None):
    __doc__="""Returns position B from position A and delta.

Parameters
----------
n_EA_E:  3 x n array
    n-vector(s) [no unit] of position A, decomposed in E.
p_AB_E:  3 x n array
    Cartesian position vector(s) from A to B, decomposed in E.
z_EA:  1 x n array
    Depth(s) [m] of system A, relative to the ellipsoid. (z_EA = -height)
a: real scalar, default WGS-84 ellipsoid.
    Semi-major axis of the Earth ellipsoid given in [m].
f: real scalar, default WGS-84 ellipsoid.
    Flattening [no unit] of the Earth ellipsoid. If f==0 then spherical
    Earth with radius a is used in stead of WGS-84.
R_Ee : 3 x 3 array
    rotation matrix defining the axes of the coordinate frame E.

Returns
-------
n_EB_E:  3 x n array
    n-vector(s) [no unit] of position B, decomposed in E.
z_EB:  1 x n array
    Depth(s) [m] of system B, relative to the ellipsoid.
    (z_EB = -height)

Notes
-----
The n-vector for position A (n_EA_E) and the position-vector from position
A to position B (p_AB_E) are given. The output is the n-vector of position
B (n_EB_E) and depth of B (z_EB).
The calculation is excact, taking the ellipsity of the Earth into account.
It is also non-singular as both n-vector and p-vector are non-singular
(except for the center of the Earth).
The default ellipsoid model used is WGS-84, but other ellipsoids/spheres
might be specified.

{0}

See also
--------
n_EA_E_and_n_EB_E2p_AB_E, p_EB_E2n_EB_E, n_EB_E2p_EB_E
""".format(_examples.get_examples_no_header([2], OO=False))

    if R_Ee is None:
        R_Ee = E_rotation()

    # Function 2. in Section 5.4 in Gade (2010):
    p_EA_E = n_EB_E2p_EB_E(n_EA_E, z_EA, a, f, R_Ee)
    p_EB_E = p_EA_E + p_AB_E
    n_EB_E, z_EB = p_EB_E2n_EB_E(p_EB_E, a, f, R_Ee)
    return n_EB_E, z_EB


def interpolate(path, ti):
    """
    Returns the interpolated point along the path

    Parameters
    ----------
    path: tuple of n-vectors (positionA, positionB)

    ti: real scalar
        interpolation time assuming position A and B is at t0=0 and t1=1,
        respectively.

    Returns
    -------
    point: Nvector
        point of interpolation along path
    """

    n_EB_E_t0, n_EB_E_t1 = path
    n_EB_E_ti = unit(n_EB_E_t0 + ti * (n_EB_E_t1 - n_EB_E_t0),
                     norm_zero_vector=np.nan)
    return n_EB_E_ti


class _Intersect(object):
    __doc__ = """Returns the intersection(s) between the great circles of the two paths

Parameters
----------
path_a, path_b: tuple of 2 n-vectors
    defining path A and path B, respectively.
    Path A and B has shape 2 x 3 x n and 2 x 3 x m, respectively.

Returns
-------
n_EC_E : array of shape 3 x max(n, m)
    n-vector(s) [no unit] of position C decomposed in E.
    point(s) of intersection between paths.

Examples
--------
{0}

""".format(_examples.get_examples_no_header([9], OO=False))


@use_docstring_from(_Intersect)
def intersect(path_a, path_b):
    n_EA1_E, n_EA2_E = path_a
    n_EB1_E, n_EB2_E = path_b
    # Find the intersection between the two paths, n_EC_E:
    n_EC_E_tmp = unit(cross(cross(n_EA1_E, n_EA2_E, axis=0),
                            cross(n_EB1_E, n_EB2_E, axis=0), axis=0),
                      norm_zero_vector=np.nan)

    # n_EC_E_tmp is one of two solutions, the other is -n_EC_E_tmp. Select
    # the one that is closet to n_EA1_E, by selecting sign from the dot
    # product between n_EC_E_tmp and n_EA1_E:
    n_EC_E = np.sign(dot(n_EC_E_tmp.T, n_EA1_E)) * n_EC_E_tmp
    if np.any(np.isnan(n_EC_E)):
        warnings.warn('Paths are Equal. Intersection point undefined. '
                      'NaN returned.')
    return n_EC_E


def great_circle_normal(n_EA_E, n_EB_E):
    """
    Returns the unit normal(s) to the great circle(s)

    Parameters
    ----------
    n_EA_E, n_EB_E:  3 x n array
        n-vector(s) [no unit] of position A and B, decomposed in E.

    """
    return unit(cross(n_EA_E, n_EB_E, axis=0), norm_zero_vector=np.nan)


def _euclidean_cross_track_distance(sin_theta, radius=1):
    return sin_theta * radius


def _great_circle_cross_track_distance(sin_theta, radius=1):
    return np.arcsin(sin_theta) * radius
    # ill conditioned for small angles:
    # return (np.arccos(-sin_theta) - np.pi / 2) * radius


class _CrossTrackDistance(object):
    __doc__ = """Returns  cross track distance between path A and position B.

Parameters
----------
path: tuple of 2 n-vectors
    2 n-vectors of positions defining path A, decomposed in E.
n_EB_E:  3 x m array
    n-vector(s) of position B to measure the cross track distance to.
method: string
    defining distance calculated. Options are: 'greatcircle' or 'euclidean'
radius: real scalar
    radius of sphere. (default 6371009.0)

Returns
-------
distance : array of length max(n, m)
    cross track distance(s)

Examples
--------
{0}

""".format(_examples.get_examples_no_header([10], OO=False))


@use_docstring_from(_CrossTrackDistance)
def cross_track_distance(path, n_EB_E, method='greatcircle', radius=6371009.0):

    c_E = great_circle_normal(path[0], path[1])
    sin_theta = -np.dot(c_E.T, n_EB_E).ravel()
    if method[0].lower() == 'e':
        return _euclidean_cross_track_distance(sin_theta, radius)
    return _great_circle_cross_track_distance(sin_theta, radius)


class _OnGreatCircle(object):
    __doc__ = """Returns True if position B is on great circle through path A.

Parameters
----------
path: tuple of 2 n-vectors
    2 n-vectors of positions defining path A, decomposed in E.
n_EB_E:  3 x m array
    n-vector(s) of position B to check to.
radius: real scalar
    radius of sphere. (default 6371009.0)
atol: real scalar
    The absolute tolerance parameter (See notes).

Returns
-------
on : bool array of length max(n, m)
    True if position B is on great circle through path A.

Notes
-----
The default value of `atol` is not zero, and is used to determine what
small values should be considered close to zero. The default value is
appropriate for expected values of order unity. However, `atol` should
be carefully selected for the use case at hand. Typically the value
should be set to the accepted error tolerance. For GPS data the error
ranges from 0.01 m to 15 m.

Examples
--------
{0}

""".format(_examples.get_examples_no_header([10], OO=False))


@use_docstring_from(_OnGreatCircle)
def on_great_circle(path, n_EB_E, radius=6371009.0, atol=1e-8):
    distance = np.abs(cross_track_distance(path, n_EB_E, radius=radius))
    return distance <= atol


class _OnGreatCirclePath(object):
    __doc__ = """Returns True if position B is on great circle and between endpoints of path A.

Parameters
----------
path: tuple of 2 n-vectors
    2 n-vectors of positions defining path A, decomposed in E.
n_EB_E:  3 x m array
    n-vector(s) of position B to measure the cross track distance to.
radius: real scalar
    radius of sphere. (default 6371009.0)
atol: real scalars
    The absolute tolerance parameter (See notes).

Returns
-------
on : bool array of length max(n, m)
    True if position B is on great circle and between endpoints of path A.

Notes
-----
The default value of `atol` is not zero, and is used to determine what
small values should be considered close to zero. The default value is
appropriate for expected values of order unity. However, `atol` should
be carefully selected for the use case at hand. Typically the value
should be set to the accepted error tolerance. For GPS data the error
ranges from 0.01 m to 15 m.

Examples
--------
{0}

""".format(_examples.get_examples_no_header([10], OO=False))


@use_docstring_from(_OnGreatCirclePath)
def on_great_circle_path(path, n_EB_E, radius=6371009.0, atol=1e-8):
    n_EA1_E, n_EA2_E = path
    scale = norm(n_EA2_E - n_EA1_E, axis=0)
    ti1 = norm(n_EB_E - n_EA1_E, axis=0) / scale
    ti2 = norm(n_EB_E - n_EA2_E, axis=0) / scale
    return (ti1 <= 1) & (ti2 <= 1) & on_great_circle(path, n_EB_E, radius, atol=atol)


class _ClosestPointOnGreatCircle(object):
    __doc__ = """Returns closest point C on great circle path A to position B.

Parameters
----------
path: tuple of 2 n-vectors of 3 x n arrays
    2 n-vectors of positions defining path A, decomposed in E.
n_EB_E:  3 x m array
    n-vector(s) of position B to find the closest point to.

Returns
-------
n_EC_E:  3 x max(m, n) array
    n-vector(s) of closest position C on great circle path A

Examples
--------
{0}

""".format(_examples.get_examples_no_header([10], OO=False))


@use_docstring_from(_ClosestPointOnGreatCircle)
def closest_point_on_great_circle(path, n_EB_E):

    n_EA1_E, n_EA2_E = path

    c1 = cross(n_EA1_E, n_EA2_E, axis=0)
    c2 = cross(n_EB_E, c1, axis=0)
    n_EC_E = unit(cross(c1, c2, axis=0))
    return n_EC_E


class _GreatCircleDistance(object):
    __doc__ = """Returns great circle distance between positions A and B

Parameters
----------
n_EA_E, n_EB_E:  3 x n array
    n-vector(s) [no unit] of position A and B, decomposed in E.
radius: real scalar
    radius of sphere.

Formulae is given by equation (16) in Gade (2010) and is well
conditioned for all angles.

Examples
--------
{0}

""".format(_examples.get_examples_no_header([5], OO=False))


@use_docstring_from(_GreatCircleDistance)
def great_circle_distance(n_EA_E, n_EB_E, radius=6371009.0):

    sin_theta = norm(np.cross(n_EA_E, n_EB_E, axis=0), axis=0)
    cos_theta = dot(n_EA_E.T, n_EB_E)
    theta = np.arctan2(sin_theta, cos_theta).ravel()
    s_AB = theta * radius

    # ill conditioned for small angles:
    # s_AB_version1 = arccos(dot(n_EA_E,n_EB_E))*radius

    # ill-conditioned for angles near pi/2 (and not valid above pi/2)
    # s_AB_version2 = arcsin(norm(cross(n_EA_E,n_EB_E)))*radius

    return s_AB


class _EuclideanDistance(object):
    __doc__ = """Returns Euclidean distance between positions A and B

Parameters
----------
n_EA_E, n_EB_E:  3 x n array
    n-vector(s) [no unit] of position A and B, decomposed in E.
radius: real scalar
    radius of sphere.

Examples
--------
{0}
""".format(_examples.get_examples_no_header([5], OO=False))


@use_docstring_from(_EuclideanDistance)
def euclidean_distance(n_EA_E, n_EB_E, radius=6371009.0):
    d_AB = norm(n_EB_E - n_EA_E, axis=0).ravel() * radius
    return d_AB


def n_EA_E_and_n_EB_E2azimuth(n_EA_E, n_EB_E, a=6378137, f=1.0 / 298.257223563, R_Ee=None):
    """
    Returns azimuth from A to B, relative to North:

    Parameters
    ----------
    n_EA_E, n_EB_E:  3 x n array
        n-vector(s) [no unit] of position A and B, respectively,
        decomposed in E.
    a: real scalar, default WGS-84 ellipsoid.
        Semi-major axis of the Earth ellipsoid given in [m].
    f: real scalar, default WGS-84 ellipsoid.
        Flattening [no unit] of the Earth ellipsoid. If f==0 then spherical
        Earth with radius a is used in stead of WGS-84.
    R_Ee : 3 x 3 array
        rotation matrix defining the axes of the coordinate frame E.

    Returns
    -------
    azimuth: n array
        Angle [rad] the line makes with a meridian, taken clockwise from north.
    """
    if R_Ee is None:
        R_Ee = E_rotation()
    # Step2: Find p_AB_E (delta decomposed in E).
    p_AB_E = n_EA_E_and_n_EB_E2p_AB_E(n_EA_E, n_EB_E, z_EA=0, z_EB=0, a=a, f=f, R_Ee=R_Ee)

    # Step3: Find R_EN for position A:
    R_EN = n_E2R_EN(n_EA_E, R_Ee=R_Ee)

    # Step4: Find p_AB_N
    # p_AB_N = dot(R_EN.T, p_AB_E)
    p_AB_N = mdot(np.swapaxes(R_EN, 1, 0), p_AB_E[:, None, ...]).reshape(3, -1)
    # (Note the transpose of R_EN: The "closest-rule" says that when
    # decomposing, the frame in the subscript of the rotation matrix that
    # is closest to the vector, should equal the frame where the vector is
    # decomposed. Thus the calculation np.dot(R_NE, p_AB_E) is correct,
    # since the vector is decomposed in E, and E is closest to the vector.
    # In the example we only had R_EN, and thus we must transpose it:
    # R_EN'=R_NE)

    # Step5: Also find the direction (azimuth) to B, relative to north:
    return arctan2(p_AB_N[1], p_AB_N[0])


class _PositionBFromAzimuthAndDistanceFromPositionA(object):
    __doc__ = """Returns position B from azimuth and distance from position A

Parameters
----------
n_EA_E:  3 x n array
    n-vector(s) [no unit] of position A decomposed in E.
distance_rad: n, array
    great circle distance [rad] from position A to B
azimuth: n array
    Angle [rad] the line makes with a meridian, taken clockwise from north.

Returns
-------
n_EB_E:  3 x n array
    n-vector(s) [no unit] of position B decomposed in E.

Examples
--------
{0}

""".format(_examples.get_examples_no_header([8], OO=False))


@use_docstring_from(_PositionBFromAzimuthAndDistanceFromPositionA)
def n_EA_E_distance_and_azimuth2n_EB_E(n_EA_E, distance_rad, azimuth, R_Ee=None):

    if R_Ee is None:
        R_Ee = E_rotation()
    # Step1: Find unit vectors for north and east:
    k_east_E = unit(cross(dot(R_Ee.T, [[1], [0], [0]]), n_EA_E, axis=0))
    k_north_E = cross(n_EA_E, k_east_E, axis=0)

    # Step2: Find the initial direction vector d_E:
    d_E = k_north_E * cos(azimuth) + k_east_E * sin(azimuth)

    # Step3: Find n_EB_E:
    n_EB_E = n_EA_E * cos(distance_rad) + d_E * sin(distance_rad)
    return n_EB_E


class _MeanHorizontalPosition(object):
    __doc__ = """Returns the n-vector of the horizontal mean position.

Parameters
----------
n_EB_E:  3 x n array
    n-vectors [no unit] of positions Bi, decomposed in E.

Returns
-------
p_EM_E:  3 x 1 array
    n-vector [no unit] of the mean positions of all Bi, decomposed in E.

Examples
--------
{0}

""".format(_examples.get_examples_no_header([7], OO=False))


@use_docstring_from(_MeanHorizontalPosition)
def mean_horizontal_position(n_EB_E):
    n_EM_E = unit(np.sum(n_EB_E, axis=1).reshape((3, 1)))
    return n_EM_E


_odict = globals()
__doc__ = (__doc__  # @ReservedAssignment
           + _make_summary(dict((n, _odict[n]) for n in __all__))
           + 'License\n-------\n'
           + _license.__doc__)


if __name__ == "__main__":
    test_docstrings(__file__)
