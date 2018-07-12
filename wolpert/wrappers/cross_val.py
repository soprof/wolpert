"""Stacked ensemble wrapper using cross validation"""

# Author: Caio Oliveira <caioaao@gmail.com>
# License: BSD 3 clause

from sklearn.base import (BaseEstimator, TransformerMixin, MetaEstimatorMixin,
                          clone)
from sklearn.model_selection import cross_val_predict

from .base import BaseStackableTransformer


class CVStackableTransformer(BaseStackableTransformer):
    """Transformer to turn estimators into meta-estimators for model stacking

    This class uses the k-fold predictions to "blend" the estimator. This
    allows the subsequent layers to use all the data for training. The drawback
    is that, as the metaestimators will be re-trained using the whole training
    set, the train and test set for subsequent layers won't be generated from
    the same probability distribution. Either way, this method still proves
    useful in practice.

    Parameters
    ----------
    estimator : predictor
        The estimator to be blended.

    method : string, optional (default='auto')
        This method will be called on the estimator to produce the output of
        transform. If the method is ``auto``, will try to invoke, for each
        estimator, ``predict_proba``, ``decision_function`` or ``predict``
        in that order.

    cv : int, cross-validation generator or an iterable, optional (default=3)
        Determines the cross-validation splitting strategy to be used for
        generating features to train the next layer on the stacked ensemble or,
        more specifically, during ``blend``.

        Possible inputs for cv are:

        - None, to use the default 3-fold cross-validation,
        - integer, to specify the number of folds.
        - An object to be used as a cross-validation generator.
        - An iterable yielding train/test splits.

        For integer/None inputs, if the estimator is a classifier and ``y`` is
        either binary or multiclass,
        ``sklearn.model_selection.StratifiedKFold`` is used. In all other
        cases, ``sklearn.model_selection.KFold`` is used.

    n_cv_jobs : int, optional (default=1)
        Number of jobs to be passed to ``cross_val_predict`` during
        ``blend``.

    Examples
    --------
    >>> from sklearn.naive_bayes import GaussianNB
    >>> from wolpert.wrappers import CVStackableTransformer
    >>> CVStackableTransformer(GaussianNB(priors=None), cv=5,
    ...                        method='predict_proba')
    ...     # doctest: +NORMALIZE_WHITESPACE
    CVStackableTransformer(cv=5, estimator=GaussianNB(priors=None),
                           method='predict_proba', n_cv_jobs=1)
    """
    def __init__(self, estimator, method='auto', cv=3, n_cv_jobs=1):
        super(CVStackableTransformer, self).__init__(estimator, method)
        self.cv = cv
        self.n_cv_jobs = n_cv_jobs

    def blend(self, X, y, **fit_params):
        """Transform dataset using cross validation.

        Parameters
        ----------
        X : array-like or sparse matrix, shape=(n_samples, n_features)
            Input data used to build forests. Use ``dtype=np.float32`` for
            maximum efficiency.

        y : array-like, shape = [n_samples]
            Target values.

        **fit_params : parameters to be passed to the base estimator.

        Returns
        -------
        X_transformed : sparse matrix, shape=(n_samples, n_out)
            Transformed dataset.

        """
        self.estimator_ = clone(self.estimator)
        preds = cross_val_predict(self.estimator_, X, y, cv=self.cv,
                                  method=self._estimator_function_name,
                                  n_jobs=self.n_cv_jobs, fit_params=fit_params)
        self.estimator_ = None

        if preds.ndim == 1:
            preds = preds.reshape(-1, 1)

        return preds
