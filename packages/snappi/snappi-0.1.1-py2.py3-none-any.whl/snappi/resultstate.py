from .snappicommon import SnappiObject


class ResultState(SnappiObject):
    _TYPES = {
        'port_state': '.resultportstatelist.ResultPortStateList',
        'flow_state': '.resultflowstatelist.ResultFlowStateList',
    }

    def __init__(self):
        super(ResultState, self).__init__()

    @property
    def port_state(self):
        """port_state getter

        TBD  

        Returns: list[obj(snappi.ResultPortState)]
        """
        from .resultportstatelist import ResultPortStateList
        if 'port_state' not in self._properties or self._properties['port_state'] is None:
            self._properties['port_state'] = ResultPortStateList()
        return self._properties['port_state']

    @property
    def flow_state(self):
        """flow_state getter

        TBD  

        Returns: list[obj(snappi.ResultFlowState)]
        """
        from .resultflowstatelist import ResultFlowStateList
        if 'flow_state' not in self._properties or self._properties['flow_state'] is None:
            self._properties['flow_state'] = ResultFlowStateList()
        return self._properties['flow_state']
