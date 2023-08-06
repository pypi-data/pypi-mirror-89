import numpy as np
import pandas as pd


def load_dataset() -> pd.DataFrame:
    t = np.linspace(0.0, 1.0, num=1000)
    df = pd.DataFrame(
        {
            "x": np.sin(t * 12.0) * t,  # type: ignore
            "y": np.cos(t * 12.0) * t,  # type: ignore
        }
    )
    return df
