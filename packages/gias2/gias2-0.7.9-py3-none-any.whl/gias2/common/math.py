"""
FILE: math.py
LAST MODIFIED: 24-12-2015
DESCRIPTION: Commonly used math functions

===============================================================================
This file is part of GIAS2. (https://bitbucket.org/jangle/gias2)

This Source Code Form is subject to the terms of the Mozilla Public
License, v. 2.0. If a copy of the MPL was not distributed with this
file, You can obtain one at http://mozilla.org/MPL/2.0/.
===============================================================================
"""
from typing import Tuple

import numpy as np
import scipy.stats as stats


def norm(v: np.ndarray) -> np.ndarray:
    """
    Normalise a vector v
    """
    return np.divide(v, mag(v))


def norms(v: np.ndarray) -> np.ndarray:
    """
    Normalise a list of vectors v
    """
    return np.divide(v, mag(v)[:, np.newaxis])


def mag(v: np.ndarray) -> float:
    return np.sqrt((np.array(v) ** 2.0).sum(-1))


def angle(v1: np.ndarray, v2: np.ndarray, tol: float = 1e-9) -> float:
    x = (v1 * v2).sum(-1) / (mag(v1) * mag(v2))
    if abs(1.0 - x) <= tol:
        return 0.0
    else:
        return np.arccos(x)


def rms(x: np.ndarray) -> float:
    return np.sqrt((x * x).mean(-1))


def meanConfidenceInterval(data: np.ndarray, confidence: float = 0.95) -> Tuple[float, float, float]:
    a = 1.0 * np.array(data)
    n = a.shape[0]
    m = float(np.mean(a))
    se = float(stats.sem(a))
    h = se * stats.t.ppf((1 + confidence) / 2., n - 1)
    return m, m - h, m + h


def trimAngle(x: float) -> float:
    return np.mod(x, 2 * np.pi * np.sign(x))
