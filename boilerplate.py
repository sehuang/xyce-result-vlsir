import enum

class AnalysisType(enum.Enum):
    SINGLE = 1
    SWEEP = 2
    MONTE = 10


class Analysis:
    def __init__(self, name: str) -> None:
        self.name = name
    

class OpAnalysis(Analysis):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        
        
class DcAnalysis(Analysis):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        
        
class AcAnalysis(Analysis):
    def __init__(self, name: str) -> None:
        super().__init__(name)


class TranAnalysis(Analysis):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        

class CustomAnalysis(Analysis):
    def __init__(self, name: str) -> None:
        super().__init__(name)