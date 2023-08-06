from .base import AlgoBase
from .torch.bc_impl import BCImpl, DiscreteBCImpl
from ..optimizers import AdamFactory
from ..argument_utils import check_encoder, check_use_gpu, check_augmentation


class BC(AlgoBase):
    r""" Behavior Cloning algorithm.

    Behavior Cloning (BC) is to imitate actions in the dataset via a supervised
    learning approach.
    Since BC is only imitating action distributions, the performance will be
    close to the mean of the dataset even though BC mostly works better than
    online RL algorithms.

    .. math::

        L(\theta) = \mathbb{E}_{a_t, s_t \sim D}
            [(a_t - \pi_\theta(s_t))^2]

    Args:
        learning_rate (float): learing rate.
        optim_factory (d3rlpy.optimizers.OptimizerFactory): optimizer factory.
        encoder_factory (d3rlpy.encoders.EncoderFactory or str):
            encoder factory.
        batch_size (int): mini-batch size.
        n_frames (int): the number of frames to stack for image observation.
        use_gpu (bool, int or d3rlpy.gpu.Device):
            flag to use GPU, device ID or device.
        scaler (d3rlpy.preprocessing.Scaler or str): preprocessor.
            The available options are `['pixel', 'min_max', 'standard']`
        augmentation (d3rlpy.augmentation.AugmentationPipeline or list(str)):
            augmentation pipeline.
        dynamics (d3rlpy.dynamics.base.DynamicsBase): dynamics model for data
            augmentation.
        impl (d3rlpy.algos.torch.bc_impl.BCImpl):
            implemenation of the algorithm.

    Attributes:
        learning_rate (float): learing rate.
        optim_factory (d3rlpy.optimizers.OptimizerFactory): optimizer factory.
        encoder_factory (d3rlpy.encoders.EncoderFactory): encoder factory.
        batch_size (int): mini-batch size.
        n_frames (int): the number of frames to stack for image observation.
        use_gpu (d3rlpy.gpu.Device): GPU device.
        scaler (d3rlpy.preprocessing.Scaler): preprocessor.
        augmentation (d3rlpy.augmentation.AugmentationPipeline):
            augmentation pipeline.
        dynamics (d3rlpy.dynamics.base.DynamicsBase): dynamics model.
        impl (d3rlpy.algos.torch.bc_impl.BCImpl):
            implemenation of the algorithm.
        eval_results_ (dict): evaluation results.

    """
    def __init__(self,
                 *,
                 learning_rate=1e-3,
                 optim_factory=AdamFactory(),
                 encoder_factory='default',
                 batch_size=100,
                 n_frames=1,
                 use_gpu=False,
                 scaler=None,
                 augmentation=None,
                 dynamics=None,
                 impl=None,
                 **kwargs):
        super().__init__(batch_size=batch_size,
                         n_frames=n_frames,
                         n_steps=1,
                         gamma=1.0,
                         scaler=scaler,
                         dynamics=dynamics)
        self.learning_rate = learning_rate
        self.optim_factory = optim_factory
        self.encoder_factory = check_encoder(encoder_factory)
        self.augmentation = check_augmentation(augmentation)
        self.use_gpu = check_use_gpu(use_gpu)
        self.impl = impl

    def create_impl(self, observation_shape, action_size):
        self.impl = BCImpl(observation_shape=observation_shape,
                           action_size=action_size,
                           learning_rate=self.learning_rate,
                           optim_factory=self.optim_factory,
                           encoder_factory=self.encoder_factory,
                           use_gpu=self.use_gpu,
                           scaler=self.scaler,
                           augmentation=self.augmentation)
        self.impl.build()

    def update(self, epoch, itr, batch):
        loss = self.impl.update_imitator(batch.observations, batch.actions)
        return (loss, )

    def predict_value(self, x, action):
        """ value prediction is not supported by BC algorithms.
        """
        raise NotImplementedError('BC does not support value estimation.')

    def sample_action(self, x):
        """ sampling action is not supported by BC algorithm.
        """
        raise NotImplementedError('BC does not support sampling action.')

    def _get_loss_labels(self):
        return ['loss']


class DiscreteBC(BC):
    r""" Behavior Cloning algorithm for discrete control.

    Behavior Cloning (BC) is to imitate actions in the dataset via a supervised
    learning approach.
    Since BC is only imitating action distributions, the performance will be
    close to the mean of the dataset even though BC mostly works better than
    online RL algorithms.

    .. math::

        L(\theta) = \mathbb{E}_{a_t, s_t \sim D}
            [-\sum_a p(a|s_t) \log \pi_\theta(a|s_t)]

    where :math:`p(a|s_t)` is implemented as a one-hot vector.

    Args:
        learning_rate (float): learing rate.
        optim_factory (d3rlpy.optimizers.OptimizerFactory): optimizer factory.
        encoder_factory (d3rlpy.encoders.EncoderFactory or str):
            encoder factory.
        batch_size (int): mini-batch size.
        n_frames (int): the number of frames to stack for image observation.
        beta (float): reguralization factor.
        use_gpu (bool, int or d3rlpy.gpu.Device):
            flag to use GPU, device ID or device.
        scaler (d3rlpy.preprocessing.Scaler or str): preprocessor.
            The available options are `['pixel', 'min_max', 'standard']`
        augmentation (d3rlpy.augmentation.AugmentationPipeline or list(str)):
            augmentation pipeline.
        dynamics (d3rlpy.dynamics.base.DynamicsBase): dynamics model for data
            augmentation.
        impl (d3rlpy.algos.torch.bc_impl.DiscreteBCImpl):
            implemenation of the algorithm.

    Attributes:
        learning_rate (float): learing rate.
        optim_factory (d3rlpy.optimizers.OptimizerFactory): optimizer factory.
        encoder_factory (d3rlpy.encoders.EncoderFactory): encoder factory.
        batch_size (int): mini-batch size.
        n_frames (int): the number of frames to stack for image observation.
        beta (float): reguralization factor.
        use_gpu (d3rlpy.gpu.Device): GPU device.
        scaler (d3rlpy.preprocessing.Scaler): preprocessor.
        augmentation (d3rlpy.augmentation.AugmentationPipeline):
            augmentation pipeline.
        dynamics (d3rlpy.dynamics.base.DynamicsBase): dynamics model.
        impl (d3rlpy.algos.torch.bc_impl.DiscreteBCImpl):
            implemenation of the algorithm.
        eval_results_ (dict): evaluation results.

    """
    def __init__(self,
                 *,
                 learning_rate=1e-3,
                 optim_factory=AdamFactory(),
                 encoder_factory='default',
                 batch_size=100,
                 n_frames=1,
                 beta=0.5,
                 use_gpu=False,
                 scaler=None,
                 augmentation=None,
                 dynamics=None,
                 impl=None,
                 **kwargs):
        super().__init__(learning_rate=learning_rate,
                         optim_factory=optim_factory,
                         encoder_factory=encoder_factory,
                         batch_size=batch_size,
                         n_frames=n_frames,
                         use_gpu=use_gpu,
                         scaler=scaler,
                         augmentation=augmentation,
                         dynamics=dynamics,
                         impl=impl,
                         **kwargs)
        self.beta = beta

    def create_impl(self, observation_shape, action_size):
        self.impl = DiscreteBCImpl(observation_shape=observation_shape,
                                   action_size=action_size,
                                   learning_rate=self.learning_rate,
                                   optim_factory=self.optim_factory,
                                   encoder_factory=self.encoder_factory,
                                   beta=self.beta,
                                   use_gpu=self.use_gpu,
                                   scaler=self.scaler,
                                   augmentation=self.augmentation)
        self.impl.build()
