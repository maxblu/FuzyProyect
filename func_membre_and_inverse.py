
import numpy as np

def membership(x, xmf, xx):
    """
    Find the degree of membership ``u(xx)`` for a given value of ``x = xx``.

    Parameters
    ----------
    x : 1d array
        con el rango de valores de la funcion.
    xmf : 1d array
        la funcion de membrecia.
    xx : valor de x par el cual se quiere saber la membrecia
    
    Returns
    -------
    xxmf : grado de membrecia

    """

    kwargs = (0.0, 0.0)
    return np.interp(xx, x, xmf, left=kwargs[0], right=kwargs[1])


def inverse_membership(x, xmf, y):
    """
    Valor in verso de la funcion de membrecia

    Parameters
    ----------
    x : 1d array
        con el rango de valores de la funcion.
    xmf : 1d array
        funcion de membrecia.
    y : float
        grado de membrecia especifico

    Returns
    -------
    xx : lista
        de valores que satisfacen y en xmf

    """
    # Special case required or zero-level cut does not work with faster method
    if y == 0.:
        idx = np.where(np.diff(xmf > y))[0]
    else:
        idx = np.where(np.diff(xmf >= y))[0]
    xx = x[idx] + (y-xmf[idx]) * (x[idx+1]-x[idx]) / (xmf[idx+1]-xmf[idx])

    # The above method is fast, but duplicates point values where
    # y == peak of a membership function.  Ducking briefly into a set
    # elimniates this.  Benchmarked multiple ways; this is by far the fastest.
    # Speed penalty approximately 10%, worth it.
    return [n for n in set(xx.tolist())]

def funcion_membrecia_triangular(x,abc):
    """
    
    Parameters
    ----------
    x : 1d array
        rango de valores.
    abc : 1d array, length 3
        con los tres valores que definen el intervalo de la triangular

    Returns
    -------
    y : 1d array
        con la funcion tringular.
    """
    assert len(abc) == 3, 'debe tener exactamente tres elementos.'
    a, b, c = np.r_[abc]     # Zero-indexing in Python
    assert a <= b and b <= c, 'los elementos tienen que ser de la forma a <= b <= c.'

    y = np.zeros(len(x))

    # Left side
    if a != b:
        idx = np.nonzero(np.logical_and(a < x, x < b))[0]
        y[idx] = (x[idx] - a) / float(b - a)

    # Right side
    if b != c:
        idx = np.nonzero(np.logical_and(b < x, x < c))[0]
        y[idx] = (c - x[idx]) / float(c - b)

    idx = np.nonzero(x == b)
    y[idx] = 1
    return y

def funcion_membrecia_trapezoidal(x, abcd,tipo):
    """
    
    Parameters
    ----------
    x : 1d array
        rango de valores para la funcion
    abcd : 1d array, length 4
        con los elementos que definen el intervalo de la funcion
    tipo: int
        0->  trapecio a la derecha 
        1->  trapecio a la izq
        eoc->trapecio al centro
    Returns
    -------
    y : 1d array
        con la funcion trapezoidal.
    """
    assert len(abcd) == 4, 'abcd debe tener exactamente 4 elementos.'
    a, b, c, d = np.r_[abcd]
    assert a <= b and b <= c and c <= d, 'los elementos tienen que ser de la forma  \
                                          a <= b <= c <= d.'
    y = np.ones(len(x))

   
    if tipo == 0:
        idx = np.nonzero(x <= b)[0]
        y[idx] = funcion_membrecia_triangular(x[idx], np.r_[a, b, b])

        idx = np.nonzero(x < a)[0]
        y[idx] = np.zeros(len(idx))

        idx = np.nonzero(x > d)[0]
        y[idx] = np.zeros(len(idx))
    
    
    elif tipo == 1:
        idx = np.nonzero(x >= c)[0]
        y[idx] = funcion_membrecia_triangular(x[idx], np.r_[c, c, d])

        idx = np.nonzero(x < a)[0]
        y[idx] = np.zeros(len(idx))

        idx = np.nonzero(x > d)[0]
        y[idx] = np.zeros(len(idx))
 
    else:
        idx = np.nonzero(x <= b)[0]
        y[idx] = funcion_membrecia_triangular(x[idx], np.r_[a, b, b])

        idx = np.nonzero(x >= c)[0]
        y[idx] = funcion_membrecia_triangular(x[idx], np.r_[c, c, d])

        idx = np.nonzero(x < a)[0]
        y[idx] = np.zeros(len(idx))

        idx = np.nonzero(x > d)[0]
        y[idx] = np.zeros(len(idx))


    return y
