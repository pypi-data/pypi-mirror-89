from typing import Union

import numpy as np
from .number import Const, Float


def _type_check_internal(x: Float):
    """Internal type checking function

    :param x: the object
    :return: None
    """
    if not isinstance(x, Float):
        raise TypeError("x must be a Float object")


# https://en.wikipedia.org/wiki/Significance_arithmetic
# https://www.cl.cam.ac.uk/~jrh13/papers/transcendentals.pdf

# significant figures of f(x) = significant figures of x - log10( df/dx * x / f )
#   significant figures of f(x) has a min of 1

def __calculate_sf_from_cn(z: float, sf: int) -> int:
    return max(int(np.floor(sf - np.log10(np.abs(z)))), 1)


def exp(x: Float) -> Float:
    """Exponential

    :param x: Exponent value
    :return: the result
    """
    _type_check_internal(x)
    # sf - log10(exp * x / exp)
    new_sf = __calculate_sf_from_cn(x.v, x.sf)
    return Float(np.exp(x.v), new_sf)


def exp2(x: Float) -> Float:
    """Base 2 Exponential

    :param x: Exponent value
    :return: the result
    """
    _type_check_internal(x)
    # sf - log10(log(2)*2^x * x / 2^x)
    new_sf = __calculate_sf_from_cn(np.log(2) * x.v, x.sf)
    return Float(np.exp2(x.v), new_sf)


def exp10(x: Float) -> Float:
    """Base 10 Exponential

    :param x: Exponent value
    :return: the result
    """
    _type_check_internal(x)
    # sf - log10(log(10)*10^x * x / 10^x)
    new_sf = __calculate_sf_from_cn(np.log(10) * x.v, x.sf)
    return Float(10.0 ** x.v, new_sf)


def __calculate_log_sf(val: float, sf: int) -> int:
    if np.isclose(val, 1.0):
        return 1
    elif val <= 0.0:
        raise RuntimeError("Cannot compute the log of a negative number")
    else:
        return __calculate_sf_from_cn(1.0 / np.log(val), sf)


def log(x: Float) -> Float:
    """Natural logarithm

    :param x: value to be logged
    :return: the result
    """
    _type_check_internal(x)
    # sf - log10(1/x * x / ln(x))
    new_sf = __calculate_log_sf(x.v, x.sf)
    return Float(np.log(x.v), new_sf)


def ln(x: Float) -> Float:
    """Natural logarithm

    :param x: value to be logged
    :return: the result
    """
    return log(x)


def log10(x: Float, basic_rule: bool = False) -> Float:
    """Base 10 logarithm

    :param x: value to be logged
    :param basic_rule: should the significant figures be calculated according to the rule that the number of
    decimal places in the log10 result is equal to the sig figs of the number being logged
    :return: the result
    """
    _type_check_internal(x)
    if basic_rule:
        new_sf = Float._calc_sf(np.log10(x.v), -x.sf)
    else:
        # log10(x) = ln(x) / ln(10)
        new_sf = __calculate_log_sf(x.v, x.sf)
    return Float(np.log10(x.v), new_sf)


def log2(x: Float) -> Float:
    """Base 2 logarithm

    :param x: value to be logged
    :return: the result
    """
    # log2(x) = ln(x) / ln(2)
    # log2(x) = ln(x) / ln(10) so log2(x) and ln(x) should have the same sig figs
    _type_check_internal(x)
    new_sf = __calculate_log_sf(x.v, x.sf)
    return Float(np.log2(x.v), (log(x)).sf)


def log1p(x: Float) -> Float:
    """Natural logarithm of 1 plus x

    :param x: value to be logged
    :return: the result
    """
    _type_check_internal(x)
    # sf - log10(1/(x+1) * x / ln(x+1))
    if np.isclose(1.0 + x.v, 1.0):
        new_sf = 1
    elif x.v <= -1.0:
        raise RuntimeError("negative number in log1p(Float)")
    else:
        new_sf = __calculate_sf_from_cn(x.v / (x.v + 1.0) / np.log1p(x.v), x.sf)
    return Float(np.log1p(x.v), new_sf)


def sin(x: Float) -> Float:
    _type_check_internal(x)
    # sf - log10(cos(x) * x / sin(x)) = sf - log10(x / tan(x))
    tanx = np.tan(x.v)
    if abs(tanx) < 1E-12:
        # if x = 0, pi, etc then tan(x) = 0, the cn gets large and the sig figs get small.
        #  at these places, sin(x) = approx x so it is reasonable to use the sig figs of x
        new_sf = x.sf
    else:
        # if x = pi/2, 3pi/2, 5pi/2, etc then tan(x) = +- Inf, the cn gets small, and the sig figs get large
        with np.errstate(all="raise"):
            try:
                cn = x.v / tanx
            except (ZeroDivisionError, RuntimeWarning, FloatingPointError):
                print("x.v {0}, tanx {1}".format([x.v, tanx]))
            except Exception:
                return None
            else:
                if np.isnan(cn):
                    new_sf = x.sf
                else:
                    new_sf = __calculate_sf_from_cn(cn, x.sf)
    return Float(np.sin(x.v), new_sf)


def cos(x: Float) -> Float:
    _type_check_internal(x)
    # sf - log10(-sin(x) * x / cos(x)) = sf - log10(x * tan(x))
    try:
        cn = x.v * np.tan(x.v)
    except RuntimeWarning:
        new_sf = x.sf
    else:
        new_sf = __calculate_sf_from_cn(cn, x.sf)
    return Float(np.cos(x.v), new_sf)


def tan(x: Float) -> Float:
    # TODO: docstrings
    # TODO: trap illegal values
    _type_check_internal(x)
    # sf - log10(sec^2 * x / tan) = sf - log10(x(tan + cot))
    cn = x.v * (np.tan(x.v) + 1.0 / np.tan(x.v))
    new_sf = __calculate_sf_from_cn(cn, x.sf)
    return Float(np.tan(x.v), new_sf)
