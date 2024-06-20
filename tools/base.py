from abc import ABC, abstractmethod

class BaseClass(ABC):
    """
    Abstract base class for data cleaning framework.

    Defines the core structure and enforces implementation of core methods
    by subclasses.
    """

    def __init__(self):
        pass

    @abstractmethod
    def clean(self, file):
        """
        Abstract method for cleaning data in a file.

        Subclasses must implement this method to define their specific
        cleaning logic.

        Args:
            file (str): Path to the data file.

        Raises:
            NotImplementedError: Always raised by this base class.
        """
        raise NotImplementedError("Subclasses must implement clean()")

    @abstractmethod
    def process(self, file):
        """
        Template method for data cleaning process.

        Subclasses can optionally override this method to provide a complete
        data cleaning workflow that includes loading, cleaning, and saving steps.

        Args:
            file (str): Path to the data file.

        Returns:
            Any: The cleaned data (e.g., DataFrame) or None if not overridden.
        """
        raise NotImplementedError("Subclasses must implement process()")