from overrides import overrides
import torch

from alnlp.metrics.average import Average


class Perplexity(Average):
    """
    Perplexity is a common metric used for evaluating how well a language model
    predicts a sample.

    Notes
    -----
    Assumes negative log likelihood loss of each batch (base e). Provides the
    average perplexity of the batches.
    """

    @overrides
    def get_metric(self, reset: bool = False) -> float:
        """
        # Returns

        The accumulated perplexity.
        """
        average_loss = super().get_metric(reset)
        if average_loss == 0:
            return 0.0

        # Exponentiate the loss to compute perplexity
        return float(torch.exp(average_loss))
