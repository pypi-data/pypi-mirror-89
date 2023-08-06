import torch

from d3rlpy.dynamics.base import DynamicsImplBase
from d3rlpy.gpu import Device
from d3rlpy.algos.torch.utility import to_cuda, to_cpu
from d3rlpy.algos.torch.utility import torch_api, eval_api
from d3rlpy.algos.torch.utility import map_location
from d3rlpy.algos.torch.utility import get_state_dict, set_state_dict


class TorchImplBase(DynamicsImplBase):
    def __init__(self, observation_shape, action_size, scaler):
        self.observation_shape = observation_shape
        self.action_size = action_size
        self.scaler = scaler
        self.device = 'cpu:0'

    @eval_api
    @torch_api(scaler_targets=['x'])
    def predict(self, x, action):
        with torch.no_grad():
            observation, reward, variance = self._predict(x, action)

            if self.scaler:
                observation = self.scaler.reverse_transform(observation)

        observation = observation.cpu().detach().numpy()
        reward = reward.cpu().detach().numpy()
        variance = variance.cpu().detach().numpy()

        return observation, reward, variance

    def _predict(self, x, action):
        raise NotImplementedError

    @eval_api
    @torch_api(scaler_targets=['x'])
    def generate(self, x, action):
        with torch.no_grad():
            observation, reward = self._generate(x, action)

            if self.scaler:
                observation = self.scaler.reverse_transform(observation)

        observation = observation.cpu().detach().numpy()
        reward = reward.cpu().detach().numpy()
        return observation, reward

    def _generate(self, x, action):
        raise NotImplementedError

    def to_gpu(self, device=Device()):
        self.device = 'cuda:%d' % device.get_id()
        to_cuda(self, self.device)

    def to_cpu(self):
        self.device = 'cpu:0'
        to_cpu(self)

    def save_model(self, fname):
        torch.save(get_state_dict(self), fname)

    def load_model(self, fname):
        chkpt = torch.load(fname, map_location=map_location(self.device))
        set_state_dict(self, chkpt)
