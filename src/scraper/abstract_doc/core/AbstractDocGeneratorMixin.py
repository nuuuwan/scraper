from abc import ABC


class AbstractDocGeneratorMixin(ABC):
    @classmethod
    def gen_docs(cls):
        pass
