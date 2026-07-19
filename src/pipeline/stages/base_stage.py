from __future__ import annotations

from abc import ABC
from abc import abstractmethod

from src.core.trading_context import TradingContext


class BaseStage(ABC):
    """
    Base class for every pipeline stage.

    Every stage receives the same TradingContext,
    updates it, and returns it.
    """

    name: str = "BaseStage"

    @abstractmethod
    def execute(
        self,
        context: TradingContext,
    ) -> TradingContext:
        """
        Execute the stage.

        Parameters
        ----------
        context : TradingContext

        Returns
        -------
        TradingContext
        """
        raise NotImplementedError()

    def before_execute(
        self,
        context: TradingContext,
    ) -> None:
        """
        Optional hook.
        """
        pass

    def after_execute(
        self,
        context: TradingContext,
    ) -> None:
        """
        Optional hook.
        """
        pass

    def run(
        self,
        context: TradingContext,
    ) -> TradingContext:

        self.before_execute(context)

        context = self.execute(context)

        self.after_execute(context)

        return context