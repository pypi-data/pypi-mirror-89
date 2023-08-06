import torch
import torch.nn as nn
import torch.nn.functional as F


class PixelEncoder(nn.Module):
    def __init__(self,
                 observation_shape,
                 filters=None,
                 feature_size=None,
                 use_batch_norm=False,
                 activation=torch.relu):
        super().__init__()

        # default architecture is based on Nature DQN paper.
        if filters is None:
            filters = [(32, 8, 4), (64, 4, 2), (64, 3, 1)]
        if feature_size is None:
            feature_size = 512

        self.observation_shape = observation_shape
        self.use_batch_norm = use_batch_norm
        self.activation = activation
        self.feature_size = feature_size

        # convolutional layers
        in_channels = [observation_shape[0]] + [f[0] for f in filters[:-1]]
        self.convs = nn.ModuleList()
        self.conv_bns = nn.ModuleList()
        for in_channel, f in zip(in_channels, filters):
            out_channel, kernel_size, stride = f
            conv = nn.Conv2d(in_channel,
                             out_channel,
                             kernel_size=kernel_size,
                             stride=stride)
            self.convs.append(conv)

            if use_batch_norm:
                self.conv_bns.append(nn.BatchNorm2d(out_channel))

        # last dense layer
        self.fc = nn.Linear(self._get_linear_input_size(), feature_size)
        if use_batch_norm:
            self.fc_bn = nn.BatchNorm1d(feature_size)

    def _get_linear_input_size(self):
        x = torch.rand((1, ) + self.observation_shape)
        with torch.no_grad():
            return self._conv_encode(x).view(1, -1).shape[1]

    def _conv_encode(self, x):
        h = x
        for i in range(len(self.convs)):
            h = self.activation(self.convs[i](h))
            if self.use_batch_norm:
                h = self.conv_bns[i](h)
        return h

    def forward(self, x):
        h = self._conv_encode(x)

        h = self.activation(self.fc(h.view(h.shape[0], -1)))
        if self.use_batch_norm:
            h = self.fc_bn(h)

        return h

    def get_feature_size(self):
        return self.feature_size


class PixelEncoderWithAction(PixelEncoder):
    def __init__(self,
                 observation_shape,
                 action_size,
                 filters=None,
                 feature_size=None,
                 use_batch_norm=False,
                 discrete_action=False,
                 activation=torch.relu):
        self.action_size = action_size
        self.discrete_action = discrete_action
        super().__init__(observation_shape, filters, feature_size,
                         use_batch_norm, activation)

    def _get_linear_input_size(self):
        size = super()._get_linear_input_size()
        return size + self.action_size

    def forward(self, x, action):
        h = self._conv_encode(x)

        if self.discrete_action:
            action = F.one_hot(action.view(-1).long(),
                               num_classes=self.action_size).float()

        # cocat feature and action
        h = torch.cat([h.view(h.shape[0], -1), action], dim=1)
        h = self.activation(self.fc(h))
        if self.use_batch_norm:
            h = self.fc_bn(h)

        return h


class VectorEncoder(nn.Module):
    def __init__(self,
                 observation_shape,
                 hidden_units=None,
                 use_batch_norm=False,
                 use_dense=False,
                 activation=torch.relu):
        super().__init__()
        self.observation_shape = observation_shape

        if hidden_units is None:
            hidden_units = [256, 256]

        self.use_batch_norm = use_batch_norm
        self.feature_size = hidden_units[-1]
        self.activation = activation
        self.use_dense = use_dense

        in_units = [observation_shape[0]] + hidden_units[:-1]
        self.fcs = nn.ModuleList()
        self.bns = nn.ModuleList()
        for i, (in_unit, out_unit) in enumerate(zip(in_units, hidden_units)):
            if use_dense and i > 0:
                in_unit += observation_shape[0]
            self.fcs.append(nn.Linear(in_unit, out_unit))
            if use_batch_norm:
                self.bns.append(nn.BatchNorm1d(out_unit))

    def forward(self, x):
        h = x
        for i in range(len(self.fcs)):
            if self.use_dense and i > 0:
                h = torch.cat([h, x], dim=1)
            h = self.activation(self.fcs[i](h))
            if self.use_batch_norm:
                h = self.bns[i](h)
        return h

    def get_feature_size(self):
        return self.feature_size


class VectorEncoderWithAction(VectorEncoder):
    def __init__(self,
                 observation_shape,
                 action_size,
                 hidden_units=None,
                 use_batch_norm=False,
                 use_dense=False,
                 discrete_action=False,
                 activation=torch.relu):
        self.action_size = action_size
        self.discrete_action = discrete_action
        concat_shape = (observation_shape[0] + action_size, )
        super().__init__(concat_shape, hidden_units, use_batch_norm, use_dense,
                         activation)
        self.observation_shape = observation_shape

    def forward(self, x, action):
        if self.discrete_action:
            action = F.one_hot(action.view(-1).long(),
                               num_classes=self.action_size).float()

        x = torch.cat([x, action], dim=1)
        return super().forward(x)
