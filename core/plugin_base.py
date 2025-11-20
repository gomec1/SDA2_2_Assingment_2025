from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """
    Common interface for all text processing plugins.
    Core never depends on concrete plugins, only on this base type.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Plugin name."""
        raise NotImplementedError

    @property
    def description(self) -> str:
        """Optional plugin description."""
        return self.__class__.__doc__ or ""

    @abstractmethod
    def process(self, text: str) -> str:
        """
        Process text and return modified text.
        Core will chain selected plugins in order.
        """
        raise NotImplementedError
