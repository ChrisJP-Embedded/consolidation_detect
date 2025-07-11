
from abc import ABC, abstractmethod
import pandas as pd

class ConsolidationScorer(ABC):
    @abstractmethod
    def compute_score(self, data: pd.DataFrame) -> float:
        pass
