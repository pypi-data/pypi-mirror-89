from abc import ABC, abstractmethod


class Stage(ABC):
    def __init__(self, pipeline: "Pipeline") -> None:
        self.pipeline = pipeline

    @abstractmethod
    def process(self, input: Any) -> Any:
        pass
