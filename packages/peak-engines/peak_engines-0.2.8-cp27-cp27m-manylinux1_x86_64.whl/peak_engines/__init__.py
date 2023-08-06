from builtins import object
from . import peak_engines_impl
import numpy as np

class BridgeRegressionModel(object):
    """Implements bridge regularized regression with regularizers fit so
    as to maximize the performance on the specified cross-validation metric.

    Parameters
    ----------
    init0 : object, default=None
        Functor that can be used to change the starting parameters of the optimizer.

    fit_intercept : bool, default=True
        Whether to center the target values and feature matrix columns.

    normalize : bool, default=False
        Whether to rescale the target vector and feature matrix columns.

    grouper : object, default=None
        Customize how regularization parameters are grouped.

    tolerance : float, default=0.0001
        The tolerance for the optimizer to use when deciding to stop the objective. With a lower
        value, the optimizer will be more stringent when deciding whether to stop searching.

    Examples
    --------
    >>> from sklearn.datasets import load_boston
    >>> from peak_engines import BridgeRegressionModel
    >>> X, y = load_boston(return_X_y=True)
    >>> model = BridgeRegressionModel().fit(X, y) 
    """
    def __init__(
            self,
            init0=None,
            fit_intercept=True,
            normalize=False,
            grouper=None,
            tolerance=0.0001):
        self.params_ = {}
        self.set_params(
                init0 = init0,
                fit_intercept=fit_intercept,
                normalize=normalize,
                grouper=grouper,
                tolerance=tolerance
        )

    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        return self.params_

    def set_params(self, **parameters):
        """Set parameters for this estimator."""
        for parameter, value in parameters.items():
            self.params_[parameter] = value
        self.impl_ = peak_engines_impl.LinearLinkedRegressionModel(penalty='bridge', **self.params_)

    def fit(self, X, y):
        """Fit the ridge regression model."""
        self.impl_.fit(np.array(X), np.array(y))
        return self

    def predict(self, X_test):
        """Predict target values."""
        return self.impl_.predict(np.array(X_test))

    @property
    def coef_(self):
        """Return the regression coefficients."""
        weights = self.impl_.weights
        if self.params_['fit_intercept']:
            weights = weights[:-1]
        return np.array([weights])

    @property
    def intercept_(self):
        """Return the fitted bias."""
        weights = self.impl_.weights
        if self.params_['fit_intercept']:
            return np.array([weights[-1]])
        return np.array([0.0])

    @property
    def alpha_(self):
        """Estimated regularization parameter."""
        if len(self.impl_.hyperparameters) != 2:
            raise RuntimeError("only works with a single group")
        return self.impl_.hyperparameters[0] ** 2

    @property
    def beta_(self):
        """Estimated regularization parameter."""
        if len(self.impl_.hyperparameters) != 2:
            raise RuntimeError("only works with a single group")
        return 1 +  self.impl_.hyperparameters[1] ** 2

    @property
    def within_tolerance_(self):
        """Return True if the optimizer found parameters within the provided tolerance."""
        return self.impl_.within_tolerance

class RidgeRegressionModel(object):
    """Implements regularized regression with regularizers fit so
    as to maximize the performance on the specified cross-validation metric.

    Parameters
    ----------
    init0 : object, default=None
        Functor that can be used to change the starting parameters of the optimizer.

    fit_intercept : bool, default=True
        Whether to center the target values and feature matrix columns.

    normalize : bool, default=False
        Whether to rescale the target vector and feature matrix columns.

    score : {'loocv', 'gcv'}, default='loocv'
        Cross-validation metric to use when fitting regularization parameters:

        - 'loocv' will fit regularization parameters so as to maximize the leave-one-out
          cross-validation

        - 'gcv' will fit regularization parameters so as to maximize the generalized 
          cross-validation

    grouping_mode : {'all', 'none'}, default='all'
        How to group regularization parameters:

        - 'all' will use a single regularization parameter for all regressors.

        - 'none' will use a separate regularization parameter for each regressor.

    num_groups : int, default=0
        If greater than zero, partition regressors and assign regressors of similar magnitude to the
        same regularizer.

    grouper : object, default=None
        Customize how regularization parameters are grouped.

    tolerance : float, default=0.0001
        The tolerance for the optimizer to use when deciding to stop the objective. With a lower
        value, the optimizer will be more stringent when deciding whether to stop searching.

    Examples
    --------
    >>> from sklearn.datasets import load_boston
    >>> from peak_engines import RidgeRegressionModel
    >>> X, y = load_boston(return_X_y=True)
    >>> model = RidgeRegressionModel().fit(X, y) 
                    # Default to Leave-one-out CV with a single regularizer
    >>> model = RidgeRegressionModel(grouping_mode='none').fit(X, y) 
                    # Use separate regularizers for each regressor
    >>> model = RidgeRegressionModel(num_groups=2).fit(X, y)
                    # Use two regularizers and assign regressors of similar magnitude to the same
                    # regularizer
    >>> model = RidgeRegressionModel(
                    grouper=lambda X, y: [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]).fit(X, y) 
                    # Use two regularizers: one for the first three variables; and one for the rest
    """
    def __init__(
            self,
            init0=None,
            fit_intercept=True,
            normalize=False,
            score='loocv',
            grouping_mode='all',
            num_groups=0,
            grouper=None,
            tolerance=0.0001):
        self.params_ = {}
        self.set_params(
                init0 = init0,
                fit_intercept=fit_intercept,
                normalize=normalize,
                score=score,
                grouping_mode=grouping_mode,
                num_groups=num_groups,
                grouper=grouper,
                tolerance=tolerance
        )

    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        return self.params_

    def set_params(self, **parameters):
        """Set parameters for this estimator."""
        for parameter, value in parameters.items():
            self.params_[parameter] = value
        # Migrate to new implementation
        if self.params_['score'] == 'loocv' and \
           self.params_['grouping_mode'] == 'all' and \
           self.params_['num_groups'] == 0:
            self.impl_ = peak_engines_impl.LinearLinkedRegressionModel(
                init0 = self.params_['init0'],
                fit_intercept = self.params_['fit_intercept'],
                normalize = self.params_['normalize'],
                grouper = self.params_['grouper'],
                tolerance = self.params_['tolerance']
            )
        else:
            self.impl_ = peak_engines_impl.RidgeRegressionModel(**self.params_)

    def fit(self, X, y):
        """Fit the ridge regression model."""
        self.impl_.fit(np.array(X), np.array(y))
        return self

    def predict(self, X_test):
        """Predict target values."""
        return self.impl_.predict(np.array(X_test))

    @property
    def regularization_(self):
        """Return the fitted regularization paramers."""
        k = len(self.impl_.weights)
        if self.params_['fit_intercept']:
            k -= 1
        d = k - len(self.impl_.hyperparameters)
        if d > 0:
            return np.array(list(self.impl_.hyperparameters) + [0]*d)
        return self.impl_.hyperparameters[:k]

    @property
    def coef_(self):
        """Return the regression coefficients."""
        return self.impl_.weights

    @property
    def alpha_(self):
        """Estimated regularization parameter."""
        alpha = self.impl_.hyperparameters ** 2
        if self.params_['grouping_mode'] == 'all':
            return alpha[0]
        return alpha

    @property
    def within_tolerance_(self):
        """Return True if the optimizer found parameters within the provided tolerance."""
        return self.impl_.within_tolerance
    

class Warper(object):
    """Warping functor for a dataset's target space."""

    def __init__(self, impl):
        self.impl_ = impl

    def __call__(self, y):
        return self.compute_latent(y)

    def compute_latent(self, y):
        """Compute the warped latent values for a given target vector."""
        return self.impl_.compute_latent(np.array(y))

    def compute_latent_with_derivative(self, y):
        """Compute the warped latent values and derivatives for a given target vector."""
        return self.impl_.compute_latent_with_derivative(np.array(y))

    def invert(self, z):
        """Invert the warping transformation."""
        return self.impl_.invert(np.array(z))

    @property
    def parameters_(self):
        """Return the warping parameters."""
        return self.impl_.parameters

class LogisticRegressionModel(object):
    """Implements logistic regression with regularizers fit so
    as to maximize the performance on the approximate leave-one-out cross-validation.

    Parameters
    ----------
    init0 : object, default=None
        Functor that can be used to change the starting parameters of the optimizer.

    fit_intercept : bool, default=True
        Whether to center the target values and feature matrix columns.

    normalize : bool, default=False
        Whether to rescale the target vector and feature matrix columns.

    penalty : {'l2', 'l1', 'elasticnet', 'bridge'}, default='l2'
        Regularization function to use

        - 'l2' will use the function sum_i alpha |w_i|^2

        - 'l1' will use the function sum_i alpha |w_i|. Near zero, it
          approximates using a polynomial so that the regularizer is differentiable.

        - 'elasticnet' will use the function sum_i alpha |w_i|^2 + beta |w_i|. 
          Near zero, it approximates using a polynomial so that the regularizer is differentiable.

        - 'bridge' will use the function sum_i alpha |w_i|^beta where 1<=beta. 
          Near zero, it approximates using a polynomial so that the regularizer is differentiable.

    grouper : object, default=None
        Customize how regularization parameters are grouped.

    tolerance : float, default=0.0001
        The tolerance for the optimizer to use when deciding to stop the objective. With a lower
        value, the optimizer will be more stringent when deciding whether to stop searching.

    Examples
    --------
    >>> from sklearn.datasets import load_breast_cancer
    >>> from peak_engines import LogisticRegressionModel
    >>> X, y = load_boston(return_X_y=True)
    >>> model = LogisticRegressionModel(normalize=True).fit(X, y)
                    # Defaults to use the regularizer l2 and finds the
                    # hyperparameters that maximize performance on
                    # the approximate leave-one-out cross-validation.
    >>> print(model.C_) # print out the hyperparameters
    """
    def __init__(
            self,
            init0=None,
            fit_intercept=True,
            normalize=False,
            penalty='l2',
            grouper=None,
            tolerance=0.0001):
        self.params_ = {}
        self.set_params(
                init0 = init0,
                fit_intercept=fit_intercept,
                normalize=normalize,
                penalty=penalty,
                grouper=grouper,
                tolerance=tolerance
        )

    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        return self.params_

    def set_params(self, **parameters):
        """Set parameters for this estimator."""
        for parameter, value in parameters.items():
            self.params_[parameter] = value
        self.impl_ = peak_engines_impl.LogisticRegressionModel(**self.params_)

    def fit(self, X, y):
        """Fit the logistic regression model."""
        self.impl_.fit(np.array(X), np.array(y))
        return self

    def predict_proba(self, X_test):
        """Predict target class propabilities."""
        return self.impl_.predict_proba(np.array(X_test))

    def predict(self, X_test):
        """Predict target classes."""
        return self.impl_.predict(np.array(X_test))

    @property
    def hyperparameters_(self):
        """Return the fitted hyperparameters."""
        return self.impl_.hyperparameters

    @property
    def C_(self):
        """Return C the inverse of the regularization strength."""
        if self.params_['penalty'] != 'l2':
            raise RuntimeError("C_ not defined for the specified penalty")
        hyperparameters = self.impl_.hyperparameters
        if len(hyperparameters) > 1:
            raise RuntimeError("C_ is only valid with a single hyperparameter")
        return np.array([0.5 / hyperparameters[0]**2])

    @property
    def coef_(self):
        """Return the regression coefficients."""
        weights = self.impl_.weights
        if self.params_['fit_intercept']:
            weights = weights[:-1]
        return np.array([weights])

    @property
    def intercept_(self):
        """Return the fitted bias."""
        weights = self.impl_.weights
        if self.params_['fit_intercept']:
            return np.array([weights[-1]])
        return np.array([0.0])

    @property
    def within_tolerance_(self):
        """Return True if the optimizer found parameters within the provided tolerance."""
        return self.impl_.within_tolerance

class WarpedLinearRegressionModel(object):
    """Warped linear regression model fit so as to maximize likelihood.

    Parameters
    ----------
    init0 : object, default=None
        Functor that can be used to change the starting parameters of the optimizer.

    fit_intercept : bool, default=True
        Whether to center the target values and feature matrix columns.

    normalize : bool, default=True
        Whether to rescale the target vector and feature matrix columns.

    num_steps : int, default=1
        The number of components to use in the warping function. More components allows for the 
        model to fit more complex warping functions but increases the chance of overfitting.

    tolerance : float, default=0.0001
        The tolerance for the optimizer to use when deciding to stop the objective. With a lower
        value, the optimizer will be more stringent when deciding whether to stop searching.

    Examples
    --------
    """
    def __init__(
            self,
            init0=None,
            fit_intercept=True,
            normalize=True,
            num_steps=1,
            tolerance=0.0001):
        self.params_ = {}
        self.set_params(
                init0 = init0,
                fit_intercept=fit_intercept,
                normalize=normalize,
                num_steps=num_steps,
                tolerance=tolerance
        )

    def get_params(self, deep=True):
        """Get parameters for this estimator."""
        return self.params_

    def set_params(self, **parameters):
        """Set parameters for this estimator."""
        for parameter, value in parameters.items():
            self.params_[parameter] = value
        self.impl_ = peak_engines_impl.WarpedLinearRegressionModel(**self.params_)

    def fit(self, X, y):
        """Fit the warped linear regression model."""
        self.impl_.fit(np.array(X), np.array(y))
        return self

    def predict(self, X_test):
        """Predict target values."""
        return self.impl_.predict(np.array(X_test))

    def predict_latent_with_stddev(self, X_test):
        """Predict latent values along with the standard deviation of the error distribution."""
        return self.impl_.predict_latent_with_stddev(np.array(X_test))

    def predict_logpdf(self, X_test):
        """Predict target values with a functor that returns the log-likelihood of given target
        values under the model's error distribution."""
        z_pred, z_err = self.predict_latent_with_stddev(X_test)

        def logpdf(y):
            assert len(y) == len(z_pred)
            z, z_der = self.warper_.compute_latent_with_derivative(y)
            result = 0
            for i, zi in enumerate(z):
                mean = z_pred[i]
                stddev = z_err[i]
                result += 0.5*(-np.log(2*np.pi*stddev**2) - ((zi - mean) / stddev)**2)
                result += np.log(z_der[i])
            return result
        return logpdf


    @property
    def warper_(self):
        """Return the warper associated with the model."""
        return Warper(self.impl_.warper)

    @property
    def noise_variance_(self):
        """Return the fitted noise variance."""
        return self.impl_.noise_variance

    @property
    def noise_stddev_(self):
        """Return the fitted noise standard deviation."""
        return np.sqrt(self.impl_.noise_variance)

    @property
    def regressors_(self):
        """Return the regressors of the latent linear regression model."""
        return self.impl_.regressors

    @property
    def within_tolerance_(self):
        """Return True if the optimizer found parameters within the provided tolerance."""
        return self.impl_.within_tolerance
