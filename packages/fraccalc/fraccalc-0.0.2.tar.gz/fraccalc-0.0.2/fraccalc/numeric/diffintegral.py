import numpy as np
from ..basic import gamma, gammaRatio


def coeff(v, N=7, method='2'):
    '''
    Return the fractional coefficients.

    Parameters
    ----------
    v : float
        Order of the diffinetration.
    N : int, optional
        Length of the corresponding coefficients. Default is 7.
    method : str
        Diffintegration operator. {'1' or '2' (default)}.

    Returns
    ----------
    coefficients : ndarray
        Coefficients are from from C_{0} to C_{N-1}.
    '''

    if method == '2':
        n = N - 2
        coefficients = np.zeros(N)
        temp = np.array([v/4 + v**2 / 8, 1 - v**2 / 4, -v/4 + v**2 / 8])
        coefficients[0] = temp[0]
        coefficients[1] = 1 - v**2 / 2 - v**3 / 8
        for k in range(1, n - 1):
            coefficients[k + 1] = gammaRatio(k - v + 1, -v) / gamma(k + 2) * temp[0] + gammaRatio(
                k - v, -v) / gamma(k + 1) * temp[1] + gammaRatio(k - v - 1, -v) / gamma(k) * temp[2]
        coefficients[n] = gammaRatio(n - v - 1, -v) / gamma(n) * \
            temp[1] + gammaRatio(n - v - 2, -v) / gamma(n - 1) * temp[2]
        coefficients[-1] = gammaRatio(n - v - 1, -v) / gamma(n) * temp[2]
        return coefficients
    elif method == '1':
        n = N - 1
        coefficients = np.zeros(N)
        coefficients[0] = 1
        coefficients[1] = -v
        for k in range(2, N):
            coefficients[k] = gammaRatio(k - v, -v) / gamma(k + 1)
        return coefficients


def dotPos(xq, N=7, a=0, method='2'):
    '''
    Return the position array for the mask convolution.

    Parameters
    ----------
    xq : float
        Point at which function is diffintegrated.
    N : int, optional
        Length of the corresponding coefficients. Default is 7.
    a : float, optional
        Lower limit of the diffintegration. Default is 0.
    method : str
        Diffintegration operator. {'1' or '2' (default)}.

    Returns
    ----------
    h : float
        Step size of the interval.
    x_arr : ndarray
        Positions for mask convolution.
    '''

    if method == '2':
        h = (xq - a) / (N - 2)
        x_arr = np.linspace(xq + h, a, N)
        return h, x_arr
    elif method == '1':
        h = (xq - a) / N
        x_arr = np.linspace(xq, a + h, N)
        return h, x_arr


def deriv(fun, xq, v, N=7, a=0, method='2'):
    '''
    Calculate the fractional diffintegral.

    Parameters
    ----------
    fun : callable
        Diffintegrand function.
    xq : ndarray or float
        Point at which fun is diffintegrated.
    v : float
        Diffintegration order.
    N : int, optional
        Length of the corresponding coefficients. Default is 7.
    a : float, optional
        Lower limit of the diffintegration. Default is 0.
    method : str
        Diffintegration operator. {'1' or '2' (default)}.

    Returns
    ----------
    yq : ndarray or float
        The diffintegral value at xq.
    '''

    C = coeff(v, N, method)
    if hasattr(xq, "__len__"):
        num = len(xq)
        yq = np.zeros(num)
        for i in range(num):
            h, x_tmp = dotPos(xq[i], N, a, method)
            yq[i] = np.dot(C, fun(x_tmp)) / h**(v)
        return yq
    else:
        h, x_tmp = dotPos(xq, N, a, method)
        return np.dot(C, fun(x_tmp)) / h**(v)


def mask(v, N=13, method='Tiansi'):
    '''
    Return fractional mask operator.

    Parameters
    ----------
    v : float
        Diffintegration order.
    N : int, optional
        Mask size of the corresponding operator. Default is 13 x 13.
    method : str
        Diffintegration operator. {'Tiansi' (1, default) or 'lcr' (2)}.

    Returns
    ----------
    result_mask : 2darray
        The fractional mask.
    '''

    center = int((N - 1) / 2)
    result_mask = np.zeros((N, N))
    if method == 'Tiansi' or method == '1':
        C = coeff(v, center + 1, '1')
    elif method == 'lcr' or method == '2':
        C = coeff(v, center + 2, '2')
        C[2] += C[0]
        C = C[1:]
    
    result_mask[center, center] = 8 * C[0]
    for i in range(1, center + 1):
        c = C[i]
        result_mask[center - i, center] = c
        result_mask[center + i, center] = c
        result_mask[center, center - i] = c
        result_mask[center, center + i] = c
        result_mask[center + i, center - i] = c
        result_mask[center - i, center + i] = c
        result_mask[center - i, center - i] = c
        result_mask[center + i, center + i] = c
    return result_mask
    