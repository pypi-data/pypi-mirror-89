import unittest

import numpy as np
import pandas as pd

from echoflow import demo


class TestDemo(unittest.TestCase):
    def test_demo(self):
        df = demo.load_dataset()
        assert len(df.columns) == 2
