from nonparametricdensity import kernels
from nonparametricdensity.base_estimator import BaseEstimator
from nonparametricdensity.utils.validators import validate_kernel, validate_bandwidth


class KernelDensityEstimator(BaseEstimator):
    def __init__(self, kernel, bandwidth, module=None):
        super().__init__(module)
        self.validate_parameters(kernel, bandwidth)

        self.kernel = kernels.KERNELS[kernel]
        self.X = None
        self.bandwidth = bandwidth

    @staticmethod
    def validate_parameters(kernel, bandwidth):
        validate_kernel(kernel)
        validate_bandwidth(bandwidth)

    def fit(self, X, y=None):
        super().fit(X, y)
        self.X = self.xp.asarray(X).reshape(-1, 1)

    def score_sample(self, X):
        super().score_sample(X)
        return self.xp.mean(self.kernel((X - self.X) / self.bandwidth, module=self.xp), axis=0) / self.bandwidth

    def sample(self, n_samples, random_state=None):
        super().sample(n_samples, random_state)
