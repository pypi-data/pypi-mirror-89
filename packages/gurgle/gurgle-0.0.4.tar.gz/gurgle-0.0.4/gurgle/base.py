from functools import wraps

import numpy as np
from sklearn.base import TransformerMixin, BaseEstimator

# TODO: Make identity_func "identifiable". If we use the following one, we can use == to detect it's use,
# TODO: ... but there may be a way to annotate, register, or type any identity function so it can be detected.
def identity_func(x):
    return x

static_identity_method = staticmethod(identity_func)


class NoSuchItem:
    pass


no_such_item = NoSuchItem()


def cls_wrap(cls, obj):
    if isinstance(obj, type):

        @wraps(obj, updated=())
        class Wrap(cls):
            @wraps(obj.__init__)
            def __init__(self, *args, **kwargs):
                wrapped = obj(*args, **kwargs)
                super().__init__(wrapped)

        # Wrap.__signature__ = signature(obj)

        return Wrap
    else:
        return cls(obj)


class CallableModel:
    _call_method_str = 'transform'

    def __init__(self, model):
        if isinstance(model, type):
            model = model()
        self.model = model
        self.call_method = getattr(self.model, self._call_method_str)

    def __getattr__(self, attr):
        """Delegate method to wrapped store if not part of wrapper store methods"""
        return getattr(self.model, attr)

    def __dir__(self):
        return list(set(dir(self.__class__)).union(self.model.__dir__()))  # to forward dir to delegated stream

    wrap = classmethod(cls_wrap)

    def fit(self, X, y=None, *args, **kwargs):
        self.model.fit(X, y, *args, **kwargs)
        return self

    @staticmethod
    def preproc(self, x):
        return np.array([x])

    @staticmethod
    def postproc(self, x, model_output):
        return model_output[0]

    def __call__(self, x):
        x = self.preproc(x)
        model_output = self.call_method(x)
        post_output = self.postproc(x, model_output)
        return post_output


class TransparentModel(TransformerMixin, BaseEstimator):
    def __init__(self, **kwargs):
        pass

    def fit(self, X, y=None, *args, **kwargs):
        return self

    def partial_fit(self, X, y=None, *args, **kwargs):
        return self

    def transform(self, X):
        return X

    def predict_proba(self, X):
        return X

    def predict(self, X):
        return np.nan * np.zeros(X.shape[0])
