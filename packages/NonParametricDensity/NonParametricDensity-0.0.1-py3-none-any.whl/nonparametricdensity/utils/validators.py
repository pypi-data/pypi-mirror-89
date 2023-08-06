from nonparametricdensity import kernels


def validate_kernel(kernel):
    assert kernel in kernels.KERNELS.keys(), f"Unknown kernel type has been specified, " \
                                             f"known kernels are {list(kernels.KERNELS.keys())}, " \
                                             f"but {kernel} was provided"


def validate_bandwidth(bandwidth):
    assert bandwidth > 0, f"Wrong bandwidth has been specified ({bandwidth})"
