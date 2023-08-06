#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

__author__ = ["Markus Löning"]
__all__ = ["_StatsModelsAdapter"]

import numpy as np
import pandas as pd

from sktime.forecasting.base._base import DEFAULT_ALPHA
from sktime.forecasting.base._sktime import _SktimeForecaster
from sktime.forecasting.base._sktime import _OptionalForecastingHorizonMixin

from sktime.utils.validation.forecasting import check_y_X, check_sp
from sktime.utils.validation import check_n_jobs


class _TbatsAdapter(_OptionalForecastingHorizonMixin, _SktimeForecaster):
    """Base class for interfacing tbats forecasting algorithms"""

    def __init__(
        self,
        use_box_cox=None,
        box_cox_bounds=(0, 1),
        use_trend=None,
        use_damped_trend=None,
        sp=None,
        use_arma_errors=True,
        show_warnings=True,
        n_jobs=None,
        multiprocessing_start_method="spawn",
        context=None,
    ):

        self.use_box_cox = use_box_cox
        self.box_cox_bounds = box_cox_bounds
        self.use_trend = use_trend
        self.use_damped_trend = use_damped_trend
        self.sp = sp
        self.use_arma_errors = use_arma_errors
        self.show_warnings = show_warnings
        self.n_jobs = n_jobs
        self.multiprocessing_start_method = multiprocessing_start_method
        self.context = context
        # custom sktime args
        self._forecaster = None

        super(_TbatsAdapter, self).__init__()

    def _instantiate_model(self):
        n_jobs = check_n_jobs(self.n_jobs)
        sp = check_sp(self.sp, enforce_list=True)

        return self._ModelClass(
            use_box_cox=self.use_box_cox,
            box_cox_bounds=self.box_cox_bounds,
            use_trend=self.use_trend,
            use_damped_trend=self.use_damped_trend,
            seasonal_periods=sp,
            use_arma_errors=self.use_arma_errors,
            show_warnings=self.show_warnings,
            n_jobs=n_jobs,
            multiprocessing_start_method=self.multiprocessing_start_method,
            context=self.context,
        )

    def fit(self, y, X=None, fh=None):
        """Fit to training data.

        Parameters
        ----------
        y : pd.Series
            Target time series to which to fit the forecaster.
        fh : int, list or np.array, optional (default=None)
            The forecasters horizon with the steps ahead to to predict.
        X : pd.DataFrame, optional (default=None)
            Exogenous variables (ignored)

        Returns
        -------
        self : returns an instance of self.
        """
        y, X = check_y_X(y, X)
        self._set_y_X(y, X)
        self._set_fh(fh)

        self._forecaster = self._instantiate_model()
        self._forecaster = self._forecaster.fit(y)

        self._is_fitted = True
        return self

    def _predict(self, fh, X=None, return_pred_int=False, alpha=DEFAULT_ALPHA):
        fh = fh.to_relative(cutoff=self.cutoff)

        if not fh.is_all_in_sample(cutoff=self.cutoff):
            fh_out = fh.to_out_of_sample(cutoff=self.cutoff)
            steps = fh_out.to_pandas().max()
            out = pd.DataFrame(
                self._forecaster.forecast(steps=steps, confidence_level=1 - alpha)[1]
            )
            y_out = out["mean"]
            # pred_int
            lower = pd.Series(out["lower_bound"])
            upper = pd.Series(out["upper_bound"])
            pred_int = self._get_pred_int(lower=lower, upper=upper)

        else:
            y_out = np.array([])

        # y_pred
        y_in_sample = pd.Series(self._forecaster.y_hat)
        y_out_sample = pd.Series(y_out)
        y_pred = self._get_y_pred(y_in_sample=y_in_sample, y_out_sample=y_out_sample)

        if return_pred_int:
            return y_pred, pred_int
        else:
            return y_pred


class _StatsModelsAdapter(_OptionalForecastingHorizonMixin, _SktimeForecaster):
    """Base class for interfacing statsmodels forecasting algorithms"""

    _fitted_param_names = ()

    def __init__(self):
        self._forecaster = None
        self._fitted_forecaster = None
        super(_StatsModelsAdapter, self).__init__()

    def fit(self, y, X=None, fh=None):
        """Fit to training data.

        Parameters
        ----------
        y : pd.Series
            Target time series to which to fit the forecaster.
        fh : int, list or np.array, optional (default=None)
            The forecasters horizon with the steps ahead to to predict.
        X : pd.DataFrame, optional (default=None)
            Exogenous variables are ignored
        Returns
        -------
        self : returns an instance of self.
        """
        # statsmodels does not support the pd.Int64Index as required,
        # so we coerce them here to pd.RangeIndex
        if isinstance(y, pd.Series) and type(y.index) == pd.Int64Index:
            y, X = _coerce_int_to_range_index(y, X)

        self._set_y_X(y, X)
        self._set_fh(fh)
        self._fit_forecaster(y, X)
        self._is_fitted = True
        return self

    def _fit_forecaster(self, y_train, X_train=None):
        """Internal fit"""
        raise NotImplementedError("abstract method")

    def _predict(self, fh, X=None, return_pred_int=False, alpha=DEFAULT_ALPHA):
        """
        Make forecasts.

        Parameters
        ----------
        fh : ForecastingHorizon
            The forecasters horizon with the steps ahead to to predict.
            Default is one-step ahead forecast,
            i.e. np.array([1])
        X : pd.DataFrame, optional (default=None)
            Exogenous variables are ignored.
        return_pred_int : bool, optional (default=False)
        alpha : int or list, optional (default=0.95)

        Returns
        -------
        y_pred : pd.Series
            Returns series of predicted values.
        """
        if return_pred_int:
            raise NotImplementedError()

        # statsmodels requires zero-based indexing starting at the
        # beginning of the training series when passing integers
        start, end = fh.to_absolute_int(self._y.index[0], self.cutoff)[[0, -1]]
        y_pred = self._fitted_forecaster.predict(start, end)

        # statsmodels forecasts all periods from start to end of forecasting
        # horizon, but only return given time points in forecasting horizon
        return y_pred.loc[fh.to_absolute(self.cutoff).to_pandas()]

    def get_fitted_params(self):
        """Get fitted parameters

        Returns
        -------
        fitted_params : dict
        """
        self.check_is_fitted()
        return {
            name: self._fitted_forecaster.params.get(name)
            for name in self._get_fitted_param_names()
        }

    def _get_fitted_param_names(self):
        """Get names of fitted parameters"""
        return self._fitted_param_names


def _coerce_int_to_range_index(y, X=None):
    new_index = pd.RangeIndex(y.index[0], y.index[-1] + 1)
    try:
        np.testing.assert_array_equal(y.index, new_index)
    except AssertionError:
        raise ValueError(
            "Coercion of pd.Int64Index to pd.RangeIndex "
            "failed. Please provide `y_train` with a "
            "pd.RangeIndex."
        )
    y.index = new_index
    if X is not None:
        X.index = new_index
    return y, X
