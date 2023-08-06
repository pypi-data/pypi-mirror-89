import inspect
from abc import ABCMeta, abstractmethod
from collections import defaultdict

from nonparametricdensity.utils.exceptions import NotFittedError
from nonparametricdensity.utils.gpuoptional import array_module


class SklearnMixin:
    # Author: Gael Varoquaux <gael.varoquaux@normalesup.org>
    # License: BSD 3 clause
    # https://github.com/scikit-learn/scikit-learn/blob/0fb307bf3/sklearn/base.py
    @classmethod
    def _get_param_names(cls):
        """Get parameter names for the estimator"""
        # fetch the constructor or the original constructor before
        # deprecation wrapping if any
        init = getattr(cls.__init__, 'deprecated_original', cls.__init__)
        if init is object.__init__:
            # No explicit constructor to introspect
            return []

        # introspect the constructor arguments to find the model parameters
        # to represent
        init_signature = inspect.signature(init)
        # Consider the constructor parameters excluding 'self'
        parameters = [p for p in init_signature.parameters.values()
                      if p.name != 'self' and p.kind != p.VAR_KEYWORD]
        for p in parameters:
            if p.kind == p.VAR_POSITIONAL:
                raise RuntimeError("estimators should always "
                                   "specify their parameters in the signature"
                                   " of their __init__ (no varargs)."
                                   " %s with constructor %s doesn't "
                                   " follow this convention."
                                   % (cls, init_signature))
        # Extract and sort argument names excluding 'self'
        return sorted([p.name for p in parameters])

    def get_params(self, deep=True):
        """
        Get parameters for this estimator.

        Args:
            deep (bool, default=True): if True, will return the parameters for this estimator and
                contained subobjects that are estimators

        Returns
            dict: parameter names mapped to their values
        """
        out = dict()
        for key in self._get_param_names():
            value = getattr(self, key)
            if deep and hasattr(value, 'get_params'):
                deep_items = value.get_params().items()
                out.update((key + '__' + k, val) for k, val in deep_items)
            out[key] = value
        return out

    def set_params(self, **params):
        """
        Set the parameters of this estimator.
        The method works on simple estimators as well as on nested objects
        (such as sklearn pipelines). The latter have parameters of the form
        ``<component>__<parameter>`` so that it's possible to update each
        component of a nested object.

        Args:
            params (dict): estimator parameters

        Returns:
            object: estimator instance
        """
        if not params:
            # Simple optimization to gain speed (inspect is slow)
            return self
        valid_params = self.get_params(deep=True)

        nested_params = defaultdict(dict)  # grouped by prefix
        for key, value in params.items():
            key, delim, sub_key = key.partition('__')
            if key not in valid_params:
                raise ValueError('Invalid parameter %s for estimator %s. '
                                 'Check the list of available parameters '
                                 'with `estimator.get_params().keys()`.' %
                                 (key, self))

            if delim:
                nested_params[key][sub_key] = value
            else:
                setattr(self, key, value)
                valid_params[key] = value

        for key, sub_params in nested_params.items():
            valid_params[key].set_params(**sub_params)

        return self


class BaseEstimator(SklearnMixin, metaclass=ABCMeta):

    @abstractmethod
    def __init__(self, module=None):
        self.xp = array_module(module)
        self.fitted = False

    @staticmethod
    @abstractmethod
    def validate_parameters(*args):
        ...

    @abstractmethod
    def fit(self, X, y=None):
        self.fitted = True

    @abstractmethod
    def score_sample(self, X):
        self.check_if_fitted()

    @abstractmethod
    def sample(self, n_samples, random_state):
        self.check_if_fitted()

    def score(self, X, y=None):
        """
        Compute the mean score for a given sample.

        Args:
            X (numpy.ndarray): array of n_features-dimensional data points. Each row corresponds to a single data point.
            y: ignored

        Returns:
            float: average score for a given sample
        """
        return self.xp.mean(self.score_sample(X))

    def check_if_fitted(self):
        if not self.fitted:
            raise NotFittedError('Instance of an estimator is not yet fitted')
