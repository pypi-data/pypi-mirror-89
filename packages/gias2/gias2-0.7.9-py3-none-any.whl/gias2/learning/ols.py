"""
FILE: ols.py
LAST MODIFIED: 24-12-2015 
DESCRIPTION: Ordinary Least-squares.

Author: Vincent Nijs (+ ?)
Email: v-nijs at kellogg.northwestern.edu
Last Modified: Mon Jan 15 17:56:17 CST 2007

===============================================================================
This file is part of GIAS2. (https://bitbucket.org/jangle/gias2)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
===============================================================================
"""
import logging
import time
from numpy import log, pi, sqrt, square, diagonal
from numpy.random import randn, seed
from numpy import c_, ones, dot, diff
from scipy import stats
from scipy.linalg import inv

log = logging.getLogger(__name__)


class ols:
    """
    Author: Vincent Nijs (+ ?)

    Email: v-nijs at kellogg.northwestern.edu

    Last Modified: Mon Jan 15 17:56:17 CST 2007
    
    Dependencies: See import statement at the top of this file

    Doc: Class for multi-variate regression using OLS

    For usage examples of other class methods see the class tests at the bottom of this file. To see the class in action
    simply run this file using 'python ols.py'. This will generate some simulated data and run various analyses. If you have rpy installed
    the same model will also be estimated by R for confirmation.

    Input:
        y = dependent variable
        y_varnm = string with the variable label for y
        x = independent variables, note that a constant is added by default
        x_varnm = string or list of variable labels for the independent variables
    
    Output:
        There are no values returned by the class. Summary provides printed output.
        All other measures can be accessed as follows:

        Step 1: Create an OLS instance by passing data to the class

            m = ols(y,x,y_varnm = 'y',x_varnm = ['x1','x2','x3','x4'])

        Step 2: Get specific metrics

            To print the coefficients: 
                >>> print m.b
            To print the coefficients p-values: 
                >>> print m.p
    
    """

    def __init__(self, y, x, y_varnm='y', x_varnm=''):
        """
        Initializing the ols class. 
        """
        self.y = y
        self.x = c_[ones(x.shape[0]), x]
        self.y_varnm = y_varnm
        if not isinstance(x_varnm, list):
            self.x_varnm = ['const'] + list(x_varnm)
        else:
            self.x_varnm = ['const'] + x_varnm

        # Estimate model using OLS
        self.estimate()

    def estimate(self):

        # estimating coefficients, and basic stats
        self.inv_xx = inv(dot(self.x.T, self.x))
        xy = dot(self.x.T, self.y)
        self.b = dot(self.inv_xx, xy)  # estimate coefficients

        self.nobs = self.y.shape[0]  # number of observations
        self.ncoef = self.x.shape[1]  # number of coef.
        self.df_e = self.nobs - self.ncoef  # degrees of freedom, error
        self.df_r = self.ncoef - 1  # degrees of freedom, regression

        self.e = self.y - dot(self.x, self.b)  # residuals
        self.sse = dot(self.e, self.e) / self.df_e  # SSE
        self.se = sqrt(diagonal(self.sse * self.inv_xx))  # coef. standard errors
        self.t = self.b / self.se  # coef. t-statistics
        self.p = (1 - stats.t.cdf(abs(self.t), self.df_e)) * 2  # coef. p-values

        self.R2 = 1 - self.e.var() / self.y.var()  # model R-squared
        self.R2adj = 1 - (1 - self.R2) * ((self.nobs - 1) / (self.nobs - self.ncoef))  # adjusted R-square

        self.F = (self.R2 / self.df_r) / ((1 - self.R2) / self.df_e)  # model F-statistic
        self.Fpv = 1 - stats.f.cdf(self.F, self.df_r, self.df_e)  # F-statistic p-value

    def dw(self):
        """
        Calculates the Durbin-Waston statistic
        """
        de = diff(self.e, 1)
        dw = dot(de, de) / dot(self.e, self.e);

        return dw

    def omni(self):
        """
        Omnibus test for normality
        """
        return stats.normaltest(self.e)

    def JB(self):
        """
        Calculate residual skewness, kurtosis, and do the JB test for normality
        """

        # Calculate residual skewness and kurtosis
        skew = stats.skew(self.e)
        kurtosis = 3 + stats.kurtosis(self.e)

        # Calculate the Jarque-Bera test for normality
        JB = (self.nobs / 6) * (square(skew) + (1 / 4) * square(kurtosis - 3))
        JBpv = 1 - stats.chi2.cdf(JB, 2);

        return JB, JBpv, skew, kurtosis

    def ll(self):
        """
        Calculate model log-likelihood and two information criteria
        """

        # Model log-likelihood, AIC, and BIC criterion values 
        ll = -(self.nobs * 1 / 2) * (1 + log(2 * pi)) - (self.nobs / 2) * log(dot(self.e, self.e) / self.nobs)
        aic = -2 * ll / self.nobs + (2 * self.ncoef / self.nobs)
        bic = -2 * ll / self.nobs + (self.ncoef * log(self.nobs)) / self.nobs

        return ll, aic, bic

    def summary(self):
        """
        Printing model output to screen
        """

        # local time & date
        t = time.localtime()

        # extra stats
        ll, aic, bic = self.ll()
        JB, JBpv, skew, kurtosis = self.JB()
        omni, omnipv = self.omni()

        # printing output to screen
        log.debug('\n==============================================================================')
        log.debug("Dependent Variable: " + self.y_varnm)
        log.debug("Method: Least Squares")
        log.debug("Date: ", time.strftime("%a, %d %b %Y", t))
        log.debug("Time: ", time.strftime("%H:%M:%S", t))
        log.debug('# obs:               %5.0f' % self.nobs)
        log.debug('# variables:     %5.0f' % self.ncoef)
        log.debug('==============================================================================')
        log.debug('variable     coefficient     std. Error      t-statistic     prob.')
        log.debug('==============================================================================')
        for i in range(len(self.x_varnm)):
            log.debug('''% -5s          % -5.6f     % -5.6f     % -5.6f     % -5.6f''' % tuple(
                [self.x_varnm[i], self.b[i], self.se[i], self.t[i], self.p[i]]))
        log.debug('==============================================================================')
        log.debug('Models stats                         Residual stats')
        log.debug('==============================================================================')
        log.debug('R-squared            % -5.6f         Durbin-Watson stat  % -5.6f' % tuple([self.R2, self.dw()]))
        log.debug('Adjusted R-squared   % -5.6f         Omnibus stat        % -5.6f' % tuple([self.R2adj, omni]))
        log.debug('F-statistic          % -5.6f         Prob(Omnibus stat)  % -5.6f' % tuple([self.F, omnipv]))
        log.debug('Prob (F-statistic)   % -5.6f			JB stat             % -5.6f' % tuple([self.Fpv, JB]))
        log.debug('Log likelihood       % -5.6f			Prob(JB)            % -5.6f' % tuple([ll, JBpv]))
        log.debug('AIC criterion        % -5.6f         Skew                % -5.6f' % tuple([aic, skew]))
        log.debug('BIC criterion        % -5.6f         Kurtosis            % -5.6f' % tuple([bic, kurtosis]))
        log.debug('==============================================================================')


if __name__ == '__main__':

    ##########################
    ### testing the ols class
    ##########################

    # creating simulated data and variable labels
    seed(1)
    data = randn(100, 5)  # the data array

    # intercept is added, by default
    m = ols(data[:, 0], data[:, 1:], y_varnm='y', x_varnm=['x1', 'x2', 'x3', 'x4'])
    m.summary()

    # if you have rpy installed, use it to test the results
    have_rpy = False
    try:
        log.debug("\n")
        log.debug("=" * 30)
        log.debug("Validating OLS results in R")
        log.debug("=" * 30)

        import rpy

        have_rpy = True
    except ImportError:
        log.debug("\n")
        log.debug("=" * 30)
        log.debug("Validating OLS-class results in R")
        log.debug("=" * 30)
        log.debug("rpy is not installed")
        log.debug("=" * 30)

    if have_rpy:
        y = data[:, 0]
        x1 = data[:, 1]
        x2 = data[:, 2]
        x3 = data[:, 3]
        x4 = data[:, 4]
        rpy.set_default_mode(rpy.NO_CONVERSION)
        linear_model = rpy.r.lm(rpy.r("y ~ x1 + x2 + x3 + x4"), data=rpy.r.data_frame(x1=x1, x2=x2, x3=x3, x4=x4, y=y))
        rpy.set_default_mode(rpy.BASIC_CONVERSION)
        log.debug(linear_model.as_py()['coefficients'])
        summary = rpy.r.summary(linear_model)
        log.debug(summary)
