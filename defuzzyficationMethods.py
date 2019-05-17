import numpy as np
import skfuzzy as fuzz

fuzz.defuzzify.defuzz
def defuzzify(x,mfx,mode):

    """
    Defuzzification of a membership function, returning a defuzzified value
    of the function at x, using various defuzzification methods.

    Parameters
    ----------
    x : 1d array or iterable, length N
        Independent variable.
    mfx : 1d array of iterable, length N
        Fuzzy membership function.
    mode : string
        Controls which defuzzification method will be used.
        * 'centroid': Centroid of area
        * 'bisector': bisector of area
        * 'mom'     : mean of maximum
        * 'som'     : min of maximum
        * 'lom'     : max of maximum

    Returns
    -------
    u : float or int
        Defuzzified result.

    See Also
    --------
    skfuzzy.defuzzify.centroid, skfuzzy.defuzzify.dcentroid
    """
    mode = mode.lower()
    x = x.ravel()
    mfx = mfx.ravel()
    n = len(x)
    assert n == len(mfx), 'Length of x and fuzzy membership function must be \
                          identical.'

    if 'centroide' in mode or 'biseccion' in mode:
        zero_truth_degree = mfx.sum() == 0  # Approximation of total area
        assert not zero_truth_degree, 'Total area is zero in defuzzification!'

        if 'centroide' in mode:
            return centroid(x, mfx)

        elif 'biseccion' in mode:
            return bisector(x, mfx)

    elif 'mdm' in mode:
        return np.mean(x[mfx == mfx.max()])

    elif 'mai' in mode:
        # print(x[mfx==mfx.max()])
        return np.min(x[mfx == mfx.max()])

    elif 'mad' in mode:
        # print(x[mfx==mfx.max()])

        return np.max(x[mfx == mfx.max()])

    else:
        raise ValueError('El modo , %s, es incorrecto.' % (mode))

def centroid(x, mfx):
    """
    Defuzzification using centroid (`center of gravity`) method.

    Parameters
    ----------
    x : 1d array, length M
        Independent variable
    mfx : 1d array, length M
        Fuzzy membership function

    Returns
    -------
    u : 1d array, length M
        Defuzzified result

    See also
    --------
    skfuzzy.defuzzify.defuzz, skfuzzy.defuzzify.dcentroid
    """

    '''
    As we suppose linearity between each pair of points of x, we can calculate
    the exact area of the figure (a triangle or a rectangle).
    '''

    sum_moment_area = 0.0
    sum_area = 0.0

    # If the membership function is a singleton fuzzy set:
    if len(x) == 1:
        return x[0]*mfx[0] / np.fmax(mfx[0], np.finfo(float).eps).astype(float)

    # else return the sum of moment*area/sum of area
    for i in range(1, len(x)):
        x1 = x[i - 1]
        x2 = x[i]
        y1 = mfx[i - 1]
        y2 = mfx[i]

        # if y1 == y2 == 0.0 or x1==x2: --> rectangle of zero height or width
        if not(y1 == y2 == 0.0 or x1 == x2):
            if y1 == y2:  # rectangle
                moment = 0.5 * (x1 + x2)
                area = (x2 - x1) * y1
            elif y1 == 0.0 and y2 != 0.0:  # triangle, height y2
                moment = 2.0 / 3.0 * (x2-x1) + x1
                area = 0.5 * (x2 - x1) * y2
            elif y2 == 0.0 and y1 != 0.0:  # triangle, height y1
                moment = 1.0 / 3.0 * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y1
            else:
                moment = (2.0 / 3.0 * (x2-x1) * (y2 + 0.5*y1)) / (y1+y2) + x1
                area = 0.5 * (x2 - x1) * (y1 + y2)

            sum_moment_area += moment * area
            sum_area += area

    return sum_moment_area / np.fmax(sum_area,
                                     np.finfo(float).eps).astype(float)


def bisector(x, mfx):
    """
    Defuzzification using bisector, or division of the area in two equal parts.

    Parameters
    ----------
    x : 1d array, length M
        Independent variable
    mfx : 1d array, length M
        Fuzzy membership function

    Returns
    -------
    u : 1d array, length M
        Defuzzified result

    See also
    --------
    skfuzzy.defuzzify.defuzz
    """
    '''
    As we suppose linearity between each pair of points of x, we can calculate
    the exact area of the figure (a triangle or a rectangle).
    '''
    sum_area = 0.0
    accum_area = [0.0] * (len(x) - 1)

    # If the membership function is a singleton fuzzy set:
    if len(x) == 1:
        return x[0]

    # else return the sum of moment*area/sum of area
    for i in range(1, len(x)):
        x1 = x[i - 1]
        x2 = x[i]
        y1 = mfx[i - 1]
        y2 = mfx[i]

        # if y1 == y2 == 0.0 or x1==x2: --> rectangle of zero height or width
        if not(y1 == y2 == 0. or x1 == x2):
            if y1 == y2:  # rectangle
                area = (x2 - x1) * y1
            elif y1 == 0. and y2 != 0.:  # triangle, height y2
                area = 0.5 * (x2 - x1) * y2
            elif y2 == 0. and y1 != 0.:  # triangle, height y1
                area = 0.5 * (x2 - x1) * y1
            else:
                area = 0.5 * (x2 - x1) * (y1 + y2)
            sum_area += area
            accum_area[i - 1] = sum_area

    # index to the figure which cointains the x point that divide the area of
    # the whole fuzzy set in two
    index = np.nonzero(np.array(accum_area) >= sum_area / 2.)[0][0]

    # subarea will be the area in the left part of the bisection for this set
    if index == 0:
        subarea = 0
    else:
        subarea = accum_area[index - 1]
    x1 = x[index]
    x2 = x[index + 1]
    y1 = mfx[index]
    y2 = mfx[index + 1]

    # We are interested only in the subarea inside the figure in which the
    # bisection is present.
    subarea = sum_area/2. - subarea

    x2minusx1 = x2 - x1
    if y1 == y2:  # rectangle
        u = subarea/y1 + x1
    elif y1 == 0.0 and y2 != 0.0:  # triangle, height y2
        root = np.sqrt(2. * subarea * x2minusx1 / y2)
        u = (x1 + root)
    elif y2 == 0.0 and y1 != 0.0:  # triangle, height y1
        root = np.sqrt(x2minusx1*x2minusx1 - (2.*subarea*x2minusx1/y1))
        u = (x2 - root)
    else:
        m = (y2-y1) / x2minusx1
        root = np.sqrt(y1*y1 + 2.0*m*subarea)
        u = (x1 - (y1-root) / m)
    return u