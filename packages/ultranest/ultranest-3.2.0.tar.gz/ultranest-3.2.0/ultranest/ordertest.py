#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

This implements the same idea as https://arxiv.org/abs/2006.03371
except their KS test is problematic because the variable (insertion order)
is not continuous. Instead, this implements a Mann-Whitney-Wilcoxon
U test, which also is in practice more sensitive than the KS test.
A highly efficient implementation is achieved by keeping only
a histogram of the insertion orders and comparing those
to expectations from a uniform distribution.

To quantify the convergence of a run, one route is to apply this test
at the end of the run. Another approach is to reset the counters every
time the test exceeds a z-score of 3 sigma, and report the run lengths,
which quantify how many iterations nested sampling was able to proceed
without detection of a insertion order problem.

"""

from __future__ import print_function, division

__all__ = ['infinite_U_zscore', 'UniformOrderAccumulator']


def infinite_U_zscore(sample, B):
    """z-score for *sample* of integers to be uniformly distributed between 0 and *B*. """
    N = len(sample)
    return ((sample + 0.5).sum() - N * B * 0.5) / ((N / 12.0)**0.5 * B)


class UniformOrderAccumulator():
    """
    Store orders (1 to N), for comparison with a uniform order.
    """
    def __init__(self, N):
        self.N = 0
        self.U = 0.0

    def reset(self):
        """Set all counts to zero. """
        self.N = 0
        self.U = 0.0

    def add(self, order, N):
        """ add order out of N to histogram. """
        if not 0 <= order <= N:
            raise ValueError("order %d out of %d invalid" % (order, N))
        self.U += (order + 0.5) / N
        self.N += 1

    @property
    def zscore(self):
        """ Mann-Whitney-Wilcoxon U test z-score, against a uniform distribution. """
        N = self.N
        if N == 0:
            return 0.0
        m_U = N * 0.5
        sigma_U_corr = (N / 12.0)**0.5
        return (self.U - m_U) / sigma_U_corr

    def __len__(self):
        return self.N
