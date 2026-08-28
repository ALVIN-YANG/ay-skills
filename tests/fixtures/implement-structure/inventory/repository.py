from .domain import StockAdjustment


class InMemoryInventoryRepository:
    def __init__(self) -> None:
        self._adjustments: list[StockAdjustment] = []

    def save(self, adjustment: StockAdjustment) -> None:
        self._adjustments.append(adjustment)

    def all(self) -> list[StockAdjustment]:
        return list(self._adjustments)
