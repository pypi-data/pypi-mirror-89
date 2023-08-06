"""
__author__ = Hagai Hargil
"""

from unittest import TestCase
from pysight.nd_hist_generator.line_signal_validators.validation_tools import (
    SignalValidator,
)
from pysight.nd_hist_generator.line_signal_validators.scanimage import (
    ScanImageLineValidator,
)
import pandas as pd
import numpy as np


class TestScanImage(TestCase):
    """
    Tests for the ScanImageValidator class
    """

    dict_of_data = dict(
        PMT1=pd.DataFrame([1, 10, 20, 30], columns=["abs_time"]),
        Lines=pd.DataFrame([0, 5, 10, 15, 20, 25, 30, 35]),
        columns=["abs_time"],
    )
    vlad = SignalValidator(dict_of_data)

    def test_pairwise(self):
        dict_of_data = {}
        iter = ScanImageLineValidator(
            SignalValidator(dict_of_data)
        )._ScanImageLineValidator__pairwise([1, 2, 3, 4])
        self.assertSequenceEqual([(1, 2), (2, 3), (3, 4)], list(iter))
