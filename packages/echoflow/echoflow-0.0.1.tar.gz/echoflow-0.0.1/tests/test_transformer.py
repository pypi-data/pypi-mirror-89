import unittest

import numpy as np
import pandas as pd

from echoflow.transformer import TableTransformer


class TestTableTransformer(unittest.TestCase):
    def test_transformer(self):
        transformer = TableTransformer()
        df = pd.DataFrame(
            {
                "x": np.linspace(0.0, 1.0, 100),
                "y": 1.0 - np.linspace(0.0, 1.0, 100),
                "z": ["a", "b", "b", "c"] * 25,
            }
        )
        X = transformer.fit_transform(df)
        df_out = transformer.inverse_transform(X)
        assert np.abs(df_out[["x", "y"]].values - df[["x", "y"]].values).max() < 1e-6
        assert (df_out["z"] == df["z"]).all()
