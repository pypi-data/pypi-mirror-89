from nonparametricdensity.utils.gpuoptional import array_module


def boxcar_kernel(x, module=None):
    xp = array_module(module)
    x = xp.asarray(x)
    return xp.where(xp.abs(x) <= 1, 1, 0) / 2


def epanechnikov_kernel(x, module=None):
    xp = array_module(module)
    x = xp.asarray(x)
    return 3 * (1 - x ** 2) * xp.where(xp.abs(x) <= 1, 1, 0) / 4


def tricube_kernel(x, module=None):
    xp = array_module(module)
    x = xp.asarray(x)
    return 70 * (1 - xp.abs(x) ** 3) ** 3 * xp.where(xp.abs(x) <= 1, 1, 0) / 81


def gaussian_kernel(x, module=None):
    xp = array_module(module)
    x = xp.asarray(x)
    return xp.exp(-x ** 2 / 2) / (xp.sqrt(2 * xp.pi))


KERNELS = {
    'boxcar': boxcar_kernel,
    'epanechnikov': epanechnikov_kernel,
    'tricube': tricube_kernel,
    'gaussian': gaussian_kernel
}
