from .snappicommon import SnappiList


class ResultFlowStateList(SnappiList):
    def __init__(self):
        super(ResultFlowStateList, self).__init__()


    def resultflowstate(self, name=None, transmit='None'):
        from .resultflowstate import ResultFlowState
        item = ResultFlowState(name, transmit)
        self._add(item)
        return self
