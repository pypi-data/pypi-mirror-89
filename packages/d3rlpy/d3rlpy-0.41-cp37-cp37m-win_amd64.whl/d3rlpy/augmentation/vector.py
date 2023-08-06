import torch

from .base import Augmentation


class SingleAmplitudeScaling(Augmentation):
    r""" Single Amplitude Scaling augmentation.

    .. math::

        x' = x + z

    where :math:`z \sim \text{Unif}(minimum, maximum)`.

    References:
        * `Laskin et al., Reinforcement Learning with Augmented Data.
          <https://arxiv.org/abs/2004.14990>`_

    Args:
        minimum (float): minimum amplitude scale.
        maximum (float): maximum amplitude scale.

    Attributes:
        minimum (float): minimum amplitude scale.
        maximum (float): maximum amplitude scale.

    """

    TYPE = 'single_amplitude_scaling'

    def __init__(self, minimum=0.8, maximum=1.2):
        self.minimum = minimum
        self.maximum = maximum

    def transform(self, x):
        """ Returns scaled observation.

        Args:
            x (torch.Tensor): observation tensor.

        Returns:
            torch.Tensor: processed observation tensor.

        """
        z = torch.empty(x.shape[0], 1, device=x.device)
        z.uniform_(self.minimum, self.maximum)
        return x * z

    def get_params(self, deep=False):
        """ Returns augmentation parameters.

        Args:
            deep (bool): flag to deeply copy objects.

        Returns:
            dict: augmentation parameters.

        """
        return {'minimum': self.minimum, 'maximum': self.maximum}


class MultipleAmplitudeScaling(SingleAmplitudeScaling):
    r""" Multiple Amplitude Scaling augmentation.

    .. math::

        x' = x + z

    where :math:`z \sim \text{Unif}(minimum, maximum)` and :math:`z`
    is a vector with different amplitude scale on each.

    References:
        * `Laskin et al., Reinforcement Learning with Augmented Data.
          <https://arxiv.org/abs/2004.14990>`_

    Args:
        minimum (float): minimum amplitude scale.
        maximum (float): maximum amplitude scale.

    Attributes:
        minimum (float): minimum amplitude scale.
        maximum (float): maximum amplitude scale.

    """

    TYPE = 'multiple_amplitude_scaling'

    def transform(self, x):
        z = torch.empty(*x.shape, device=x.device)
        z.uniform_(self.minimum, self.maximum)
        return x * z
