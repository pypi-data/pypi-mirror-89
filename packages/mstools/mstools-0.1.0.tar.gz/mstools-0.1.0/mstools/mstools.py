"""
``mstools.py`` module.

Contains the functions and routines that are often used but are not included
in current common packages. It may include code used in different areas of
knowledge.
"""

import numpy as np


def r2_score(y_true, y_pred):
    """
    Calculate the coefficient of determination (:math:`R^2`).

    :math:`R^2`, pronounced "R squared", is the proportion of the variance in
    the dependent variable that is predictable from the independent
    variable(s).

    Parameters
    ----------
    y_true : List, tuple or array
        Actual value of the predictied variable.
    y_pred : List, tuple or array
        Predicted value from the linear regression model.

    Returns
    -------
    float
        Coefficient of determination (:math:`R^2`).

    Examples
    --------
    >>> y_true = [1, 2, 3, 4, 5]
    >>> y_pred = [1.1, 2.3, 2.8, 4.1, 4.9]
    >>> r2_score(y_true, y_pred)
    0.984

    """
    y_true, y_pred = np.array([y_true, y_pred])
    y_bar = y_true.mean()  # mean of the observed data
    ss_tot = ((y_true - y_bar)**2).sum()  # total sum of squares (variance)
    ss_res = ((y_true - y_pred)**2).sum()  # sum of squares of residuals
    return 1 - ss_res / ss_tot