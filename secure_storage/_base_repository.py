"""Abstract class for repository type classes."""
import abc

from secure_storage.model import IModel


class AbstractRepository(abc.ABC):
    """Defines an interface for repository family type classes."""

    @abc.abstractmethod
    def add(self, model: IModel) -> None:
        """Add an ``Order`` object to our persistent storage.

        Args:
            order (Order): An object representing an order.

        Raises:
            NotImplementedError: Abstract classes have no implementation
            :param model: Abstract class use as interface
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get(self, order_id: int) -> IModel:
        """Get an order from our persistent storage.

        Args:
            order_id (int): Id of order.

        Returns:
            Order: ``Order`` matching with ``order_id``.

        Raises:
            NotImplementedError: Abstract classes have no implementation
        """
        raise NotImplementedError

    @abc.abstractmethod
    def list(self) -> list:
        """List all ``Orders``.

        Returns:
            list: List containing all orders in ``Order`` format.

        Raises:
                NotImplementedError: Abstract classes have no implementation
        """
        raise NotImplementedError

    @abc.abstractmethod
    def remove(self) -> None:
        """List all ``Orders``.

        Returns:
            list: List containing all orders in ``Order`` format.

        Raises:
                NotImplementedError: Abstract classes have no implementation
        """
        raise NotImplementedError
