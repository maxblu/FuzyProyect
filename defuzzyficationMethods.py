import numpy as np


def defuzzify(x,mfx,mode):

    """
    Desdifuzificacion usando el modo selecionado.

    Parameters
    ----------
    x : 1d array or iterable, length N
        rango de valores de la variable.
    mfx : 1d array of iterable, length N
        funcion de membrecia.
    mode : string
        Controla cual metodo de desdefusificacion se elige.
    Returns
    -------
    u : float or int
        Resultado desdifuzificado

    """
    mode = mode.lower()
    x = x.ravel()
    mfx = mfx.ravel()
    n = len(x)
    assert n == len(mfx), 'La longitud de x y mfx debe ser la misma '

    if 'centroide' in mode or 'biseccion' in mode:
        zero_truth_degree = mfx.sum() == 0  # Approximation of total area
        assert not zero_truth_degree, 'Area total es cero luego de la desdefusificacion!'

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
    Desdifuzificacion usando centroide.

    Parameters
    ----------
    x : 1d array, length M
        Rango de valoes de la funcion
    mfx : 1d array, length M
        funcion de membrecia

    Returns
    -------
    u : 1d array, length M
        resultado desdefuzificado
    """

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
    Desdifuzificacion usando biseccion

    Parameters
    ----------
    x : 1d array, length M
        rango de valores de la funcion mfx
    mfx : 1d array, length M
        funcion de membrecia mfx

    Returns
    -------
    u : 1d array, length M
        Resultdo desdifuzificado
    """

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