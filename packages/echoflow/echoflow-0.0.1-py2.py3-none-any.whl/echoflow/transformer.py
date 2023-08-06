from typing import Optional, Tuple

import numpy as np
import pandas as pd
import torch


class Transformer:
    def __init__(self, use_parity_padding: bool = True):
        self.use_parity_padding = use_parity_padding

    def fit_transform(
        self, df: pd.DataFrame, context: Optional[pd.DataFrame] = None
    ) -> Tuple[torch.Tensor, Optional[torch.Tensor]]:
        """Fit and transform the data.

        Parameters
        ----------
        df:
            The dataframe containing continuous and categorical values.
        context:
            A dataframe containing continuous and categorical values which is
            used for conditional sampling.

        Returns
        ----------
        torch.Tensor:
            A tensor representation of the data and, optionally, a tensor representation
            of the conditioning variables.
        """
        self.df_encoder = TableTransformer()
        inputs = self.df_encoder.fit_transform(df)
        self.input_dims = self.df_encoder.dims

        contexts = None
        self.context_dims = 0
        if context is not None:
            self.context_encoder = TableTransformer()
            contexts = self.context_encoder.fit_transform(df)
            self.context_dims = self.context_encoder.dims

        self.parity_padding = False
        if self.use_parity_padding and inputs.size(1) % 2 == 1:
            inputs = torch.FloatTensor(
                torch.cat([inputs, torch.zeros(inputs.size(0), 1)], dim=1)
            )
            self.input_dims += 1
            self.parity_padding = True

        return inputs, contexts

    def inverse_transform(self, inputs: torch.Tensor) -> pd.DataFrame:
        """Inverse transform a tensor into a dataframe.

        Parameters
        ----------
        inputs:
            The tensor to apply the inverse transform to.
        """
        if self.parity_padding:
            inputs = inputs[:, :-1]
        return self.df_encoder.inverse_transform(inputs)


class TableTransformer:
    """Transform a dataframe into a tensor."""

    def fit_transform(self, df: pd.DataFrame) -> torch.Tensor:
        """Fit and transform a dataframe into a tensor.

        Continuous values are normalized to the [-1.0, 1.0] range and
        categorical values are converted into a one-hot representation.

        Parameters
        ----------
        df:
            The dataframe containing continuous and categorical values.

        Returns
        ----------
        torch.Tensor:
            A tensor representation of the data.
        """
        self.dims = 0
        self.mappings = []
        self.columns = df.columns
        for i, column in enumerate(df.columns):
            if df[column].dtype.kind in "f":
                self.mappings.append(
                    {
                        "type": "continuous",
                        "column": column,
                        "dst_idx": self.dims,
                        "min": df[column].min(),
                        "max": df[column].max(),
                    }
                )
                self.dims += 1
            elif df[column].dtype.kind in "O":
                values = set(df[column])
                self.mappings.append(
                    {
                        "type": "categorical",
                        "column": column,
                        "dst_idx": {
                            value: self.dims + i for i, value in enumerate(values)
                        },
                    }
                )
                self.dims += len(values)
            else:
                raise ValueError("Unsupported data type.")

        X = torch.zeros(len(df), self.dims)
        for mapping in self.mappings:
            if mapping["type"] == "continuous":
                X[:, mapping["dst_idx"]] = (
                    torch.FloatTensor(df[mapping["column"]].values) - mapping["min"]
                ) / (mapping["max"] - mapping["min"])
            elif mapping["type"] == "categorical":
                for value, idx in mapping["dst_idx"].items():
                    # TODO: Investigate better ways to handle categorical values
                    X[df[mapping["column"]] == value, idx] = (
                        1.0 + np.random.normal(0.0, 1.0) / 10.0  # type: ignore
                    )
        return X

    def inverse_transform(self, inputs: torch.Tensor) -> pd.DataFrame:
        """Inverse transform a tensor into a dataframe.

        Parameters
        ----------
        inputs:
            The tensor to apply the inverse transform to.
        """
        X = inputs.detach().numpy()
        cols = {}
        for mapping in self.mappings:
            if mapping["type"] == "continuous":
                cols[mapping["column"]] = (
                    X[:, mapping["dst_idx"]] * (mapping["max"] - mapping["min"])
                    + mapping["min"]
                )
            elif mapping["type"] == "categorical":
                values, indices = zip(*mapping["dst_idx"].items())
                cols[mapping["column"]] = [
                    values[i] for i in np.argmax(X[:, indices], axis=1)
                ]
        return pd.DataFrame(cols, columns=self.columns)
