from phi.tf.flow import *
from ..hierarchy import ObservationPredictor


class PDE(ObservationPredictor):

    def __init__(self):
        self.fields = {}

    def create_pde(self, world, control_trainable, constant_prediction_offset):
        raise NotImplementedError(self)

    def placeholder_state(self, world, age):
        raise NotImplementedError(self)

    def target_matching_loss(self, target_state, actual_state):
        raise NotImplementedError(self)

    def total_force_loss(self, states):
        raise NotImplementedError(self)


def property_name(trace): return trace.name


def collect_placeholders_channels(placeholder_states, trace_to_channel=property_name):
    if trace_to_channel is None: trace_to_channel = property_name
    placeholders = []
    channels = []

    for i, state in enumerate(placeholder_states):
        if state is not None:
            traces = struct.flatten(state, trace=True)
            for trace in traces:
                if isplaceholder(trace.value):
                    placeholders.append(trace.value)
                    channel = trace_to_channel(trace)
                    channels.append(consecutive_frames(channel, len(placeholder_states))[i])
    return placeholders, tuple(channels)