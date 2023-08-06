from abc import ABCMeta, abstractmethod
from d3rlpy.models.torch.q_functions import DiscreteMeanQFunction
from d3rlpy.models.torch.q_functions import DiscreteQRQFunction
from d3rlpy.models.torch.q_functions import DiscreteIQNQFunction
from d3rlpy.models.torch.q_functions import DiscreteFQFQFunction
from d3rlpy.models.torch.q_functions import ContinuousMeanQFunction
from d3rlpy.models.torch.q_functions import ContinuousQRQFunction
from d3rlpy.models.torch.q_functions import ContinuousIQNQFunction
from d3rlpy.models.torch.q_functions import ContinuousFQFQFunction


class QFunctionFactory(metaclass=ABCMeta):
    TYPE = 'none'

    @abstractmethod
    def create(self, encoder, action_size=None):
        """ Returns PyTorch's Q function module.

        Args:
            encoder (torch.nn.Module): an encoder module that processes
                the observation (and action in continuous action-space) to
                obtain feature representations.
            action_size (int): dimension of discrete action-space. If the
                action-space is continous, ``None`` will be passed.

        Returns:
            torch.nn.Module: Q function object.

        """
        pass

    def get_type(self):
        """ Returns Q function type.

        Returns:
            str: Q function type.

        """
        return self.TYPE

    @abstractmethod
    def get_params(self, deep=False):
        """ Returns Q function parameters.

        Returns:
            dict: Q function parameters.

        """
        pass


class MeanQFunctionFactory(QFunctionFactory):
    """ Standard Q function factory class.

    This is the standard Q function factory class.

    References:
        * `Mnih et al., Human-level control through deep reinforcement
          learning. <https://www.nature.com/articles/nature14236>`_
        * `Lillicrap et al., Continuous control with deep reinforcement
          learning. <https://arxiv.org/abs/1509.02971>`_

    """

    TYPE = 'mean'

    def __init__(self):
        pass

    def create(self, encoder, action_size=None):
        if action_size is None:
            q_func = ContinuousMeanQFunction(encoder)
        else:
            q_func = DiscreteMeanQFunction(encoder, action_size)
        return q_func

    def get_params(self, deep=False):
        return {}


class QRQFunctionFactory(QFunctionFactory):
    """ Quantile Regression Q function factory class.

    References:
        * `Dabney et al., Distributional reinforcement learning with quantile
          regression. <https://arxiv.org/abs/1710.10044>`_

    Args:
        n_quantiles (int): the number of quantiles.

    Attributes:
        n_quantiles (int): the number of quantiles.

    """

    TYPE = 'qr'

    def __init__(self, n_quantiles=200):
        self.n_quantiles = n_quantiles

    def create(self, encoder, action_size=None):
        if action_size is None:
            q_func = ContinuousQRQFunction(encoder, self.n_quantiles)
        else:
            q_func = DiscreteQRQFunction(encoder, action_size,
                                         self.n_quantiles)
        return q_func

    def get_params(self, deep=False):
        return {'n_quantiles': self.n_quantiles}


class IQNQFunctionFactory(QFunctionFactory):
    """ Implicit Quantile Network Q function factory class.

    References:
        * `Dabney et al., Implicit quantile networks for distributional
          reinforcement learning. <https://arxiv.org/abs/1806.06923>`_

    Args:
        n_quantiles (int): the number of quantiles.
        embed_size (int): the embedding size.

    Attributes:
        n_quantiles (int): the number of quantiles.
        embed_size (int): the embedding size.

    """

    TYPE = 'iqn'

    def __init__(self, n_quantiles=32, embed_size=64):
        self.n_quantiles = n_quantiles
        self.embed_size = embed_size

    def create(self, encoder, action_size=None):
        if action_size is None:
            q_func = ContinuousIQNQFunction(encoder, self.n_quantiles,
                                            self.embed_size)
        else:
            q_func = DiscreteIQNQFunction(encoder, action_size,
                                          self.n_quantiles, self.embed_size)
        return q_func

    def get_params(self, deep=False):
        return {'n_quantiles': self.n_quantiles, 'embed_size': self.embed_size}


class FQFQFunctionFactory(QFunctionFactory):
    """ Fully parameterized Quantile Function Q function factory.

    References:
        * `Yang et al., Fully parameterized quantile function for
          distributional reinforcement learning.
          <https://arxiv.org/abs/1911.02140>`_

    Args:
        n_quantiles (int): the number of quantiles.
        embed_size (int): the embedding size.
        entropy_coeff (float): the coefficiency of entropy penalty term.

    Attributes:
        n_quantiles (int): the number of quantiles.
        embed_size (int): the embedding size.
        entropy_coeff (float): the coefficiency of entropy penalty term.

    """

    TYPE = 'fqf'

    def __init__(self, n_quantiles=32, embed_size=64, entropy_coeff=0.0):
        self.n_quantiles = n_quantiles
        self.embed_size = embed_size
        self.entropy_coeff = entropy_coeff

    def create(self, encoder, action_size=None):
        if action_size is None:
            q_func = ContinuousFQFQFunction(encoder=encoder,
                                            n_quantiles=self.n_quantiles,
                                            embed_size=self.embed_size,
                                            entropy_coeff=self.entropy_coeff)
        else:
            q_func = DiscreteFQFQFunction(encoder=encoder,
                                          action_size=action_size,
                                          n_quantiles=self.n_quantiles,
                                          embed_size=self.embed_size,
                                          entropy_coeff=self.entropy_coeff)
        return q_func

    def get_params(self, deep=False):
        return {
            'n_quantiles': self.n_quantiles,
            'embed_size': self.embed_size,
            'entropy_coeff': self.entropy_coeff
        }


Q_FUNC_LIST = {}


def register_q_func_factory(cls):
    """ Registers Q function factory class.

    Args:
        cls (type): Q function factory class inheriting ``QFunctionFactory``.

    """
    is_registered = cls.TYPE in Q_FUNC_LIST
    assert not is_registered, '%s seems to be already registered' % cls.TYPE
    Q_FUNC_LIST[cls.TYPE] = cls


def create_q_func_factory(name, **kwargs):
    """ Returns registered Q function factory object.

    Args:
        name (str): registered Q function factory type name.
        kwargs (any): Q function arguments.

    Returns:
        d3rlpy.q_functions.QFunctionFactory: Q function factory object.

    """
    assert name in Q_FUNC_LIST, '%s seems not to be registered.' % name
    factory = Q_FUNC_LIST[name](**kwargs)
    assert isinstance(factory, QFunctionFactory)
    return factory


register_q_func_factory(MeanQFunctionFactory)
register_q_func_factory(QRQFunctionFactory)
register_q_func_factory(IQNQFunctionFactory)
register_q_func_factory(FQFQFunctionFactory)
