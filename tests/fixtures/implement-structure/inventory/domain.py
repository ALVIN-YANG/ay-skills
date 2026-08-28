from dataclasses import dataclass


@dataclass(frozen=True)
class StockAdjustment:
    sku: str
    quantity: int
