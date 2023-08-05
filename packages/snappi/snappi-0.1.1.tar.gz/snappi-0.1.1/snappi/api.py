from .snappicommon import SnappiRestTransport


class Api(SnappiRestTransport):
    """Snappi Abstract API
    """
    def __init__(self):
        super(Api, self).__init__()

    def set_config(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/config', payload=content)

    def update_config(self, content=None):
        """TBD
        """
        return self.send_recv('patch', '/config', payload=content)

    def get_config(self, content=None):
        """TBD
        """
        return self.send_recv('get', '/config', payload=content)

    def set_transmit(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/control/transmit', payload=content)

    def set_link(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/control/link', payload=content)

    def get_state_results(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/results/state', payload=content)

    def get_capability_results(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/results/capabilities', payload=content)

    def get_port_results(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/results/port', payload=content)

    def get_capture_results(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/results/capture', payload=content)

    def get_flow_results(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/results/flow', payload=content)

    def get_bgpv4_results(self, content=None):
        """TBD
        """
        return self.send_recv('post', '/results/bgpv4', payload=content)

    def config(self):
        """Return instance of auto-generated top level class Config
        """
        from .config import Config
        return Config()

    def transmitstate(self):
        """Return instance of auto-generated top level class TransmitState
        """
        from .transmitstate import TransmitState
        return TransmitState()

    def linkstate(self):
        """Return instance of auto-generated top level class LinkState
        """
        from .linkstate import LinkState
        return LinkState()

    def result_state(self):
        """Return instance of auto-generated top level class ResultState
        """
        from .resultstate import ResultState
        return ResultState()

    def result_capability(self):
        """Return instance of auto-generated top level class ResultCapability
        """
        from .resultcapability import ResultCapability
        return ResultCapability()

    def port_metricsrequest(self):
        """Return instance of auto-generated top level class PortMetricsRequest
        """
        from .portmetricsrequest import PortMetricsRequest
        return PortMetricsRequest()

    def result_capturerequest(self):
        """Return instance of auto-generated top level class ResultCaptureRequest
        """
        from .resultcapturerequest import ResultCaptureRequest
        return ResultCaptureRequest()

    def flow_metricsrequest(self):
        """Return instance of auto-generated top level class FlowMetricsRequest
        """
        from .flowmetricsrequest import FlowMetricsRequest
        return FlowMetricsRequest()

    def bgpv4_metricsrequest(self):
        """Return instance of auto-generated top level class Bgpv4MetricsRequest
        """
        from .bgpv4metricsrequest import Bgpv4MetricsRequest
        return Bgpv4MetricsRequest()
