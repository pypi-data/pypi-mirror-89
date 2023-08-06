import math
from typing import Optional

import pandas as pd
import torch
import torch.optim as optim

from echoflow.core import MADE, BatchNorm, Coupling, Reverse, SequentialFlow
from echoflow.transformer import Transformer


class EchoFlow:
    """Wrapper for training normalizing flow models."""

    def __init__(
        self,
        lr: float = 0.0001,
        nb_epochs: int = 1000,
        batch_size: int = 100,
        nb_blocks: int = 3,
        block_type: str = "RNVP",
        transformer: Transformer = None,
    ):
        self.lr = lr
        self.nb_blocks = nb_blocks
        self.nb_epochs = nb_epochs
        self.batch_size = batch_size
        self.block_type = block_type
        self.transformer = transformer if transformer else Transformer()

    def fit(self, df: pd.DataFrame, context: Optional[pd.DataFrame] = None):
        """Fit the flow model.

        Parameters
        ----------
        df:
            The dataframe containing the samples to model.
        contexts:
            The (optional) context dataframe for conditional sampling.
        """
        inputs, contexts = self.transformer.fit_transform(df, context)

        layers = []
        for _ in range(self.nb_blocks):
            if self.block_type == "RNVP":
                input_mask = torch.arange(0, self.transformer.input_dims) % 2
                layers.extend(
                    [
                        Coupling(
                            self.transformer.input_dims,
                            100,
                            input_mask,
                            self.transformer.context_dims,
                        ),
                        BatchNorm(self.transformer.input_dims),
                        Coupling(
                            self.transformer.input_dims,
                            100,
                            1.0 - input_mask,
                            self.transformer.context_dims,
                        ),
                        BatchNorm(self.transformer.input_dims),
                    ]
                )
            else:
                layers.extend(
                    [
                        MADE(
                            self.transformer.input_dims,
                            100,
                            self.transformer.context_dims,
                        ),
                        BatchNorm(self.transformer.input_dims),
                        Reverse(self.transformer.input_dims),
                    ]
                )
        self.flow = SequentialFlow(*layers)
        self.flow.train()

        dataset = torch.utils.data.TensorDataset(inputs)
        if context is not None:
            contexts = torch.FloatTensor(context.values)
            dataset = torch.utils.data.TensorDataset(inputs, contexts)
        dataloader = torch.utils.data.DataLoader(
            dataset, batch_size=self.batch_size, shuffle=True
        )

        # TODO: add validation loss
        optimizer = optim.Adam(self.flow.parameters(), lr=self.lr)
        scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, "min")
        for epoch in range(1, self.nb_epochs + 1):
            train_loss = []
            for _, data in enumerate(dataloader):
                optimizer.zero_grad()
                if isinstance(data, list) and len(data) == 2:
                    inputs, contexts = data
                    loss = -self._log_likelihood(inputs, contexts).mean()
                else:
                    loss = -self._log_likelihood(data[0], None).mean()
                loss.backward()
                train_loss.append(loss.item())
                optimizer.step()
            train_loss = sum(train_loss) / len(train_loss)
            scheduler.step(train_loss)
            print(f"Epoch {epoch} | Train Loss {train_loss:.3f}")

    def sample(
        self, num_samples: Optional[int] = None, context: Optional[pd.DataFrame] = None
    ) -> pd.DataFrame:
        """Generate samples via the inverse transform.

        Either `num_samples` or `contexts` must be provided. If both are provided, then
        they must be consistent (i.e. there are `num_samples` rows in `contexts`).

        Parameters
        ----------
        num_samples:
            The number of samples.
        contexts:
            The (optional) context dataframe for conditional sampling.
        """
        self.flow.eval()
        contexts = torch.FloatTensor(context.values) if context is not None else None

        if num_samples is None:
            assert contexts is not None
            num_samples = contexts.size(0)
        elif contexts is not None:
            assert num_samples == contexts.size(0)

        noise = torch.randn(num_samples, self.transformer.input_dims)
        samples, _ = self.flow(noise, contexts, inverse=True)

        return self.transformer.inverse_transform(samples)

    def _log_likelihood(
        self, inputs: torch.Tensor, contexts: Optional[torch.Tensor] = None
    ):
        """Compute the log-likelihood to be maximized.

        Parameters
        ----------
        inputs:
            The input tensor.
        contexts:
            An optional context tensor (for conditional sampling).
        """
        u, log_jacob = self.flow(inputs, contexts)
        log_probs = (-0.5 * u.pow(2) - 0.5 * math.log(2 * math.pi)).sum(
            -1, keepdim=True
        )
        return (log_probs + log_jacob).sum(-1, keepdim=True)
