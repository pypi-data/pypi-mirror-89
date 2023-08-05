from .snappicommon import SnappiList


class ResultPortStateList(SnappiList):
    def __init__(self):
        super(ResultPortStateList, self).__init__()


    def resultportstate(self, name=None, link='None', capture='None'):
        from .resultportstate import ResultPortState
        item = ResultPortState(name, link, capture)
        self._add(item)
        return self
