import unittest

import numpy as np
import pandas as pd

from echoflow import EchoFlow


class TestEchoFlow(unittest.TestCase):
    def test_rnvp(self):
        model = EchoFlow(nb_epochs=10, block_type="RNVP")
        df = pd.DataFrame(
            {
                "x": np.linspace(0.0, 1.0, 100),
                "y": 1.0 - np.linspace(0.0, 1.0, 100),
            }
        )
        model.fit(df)
        df_out = model.sample(num_samples=10)
        assert len(df_out) == 10
        assert (df_out.columns == df.columns).all()

    def test_rnvp_conditional(self):
        model = EchoFlow(nb_epochs=10, block_type="RNVP")
        df = pd.DataFrame(
            {
                "x": np.linspace(0.0, 1.0, 100),
                "y": 1.0 - np.linspace(0.0, 1.0, 100),
            }
        )
        df, context = df[["x"]], df[["y"]]

        model.fit(df, context)
        df_out = model.sample(context=context)
        assert len(df_out) == len(df)
        assert (df_out.columns == df.columns).all()

    def test_made(self):
        model = EchoFlow(nb_epochs=10, block_type="MADE")
        df = pd.DataFrame(
            {
                "x": np.linspace(0.0, 1.0, 100),
                "y": 1.0 - np.linspace(0.0, 1.0, 100),
            }
        )
        model.fit(df)
        df_out = model.sample(num_samples=10)
        assert len(df_out) == 10
        assert (df_out.columns == df.columns).all()
