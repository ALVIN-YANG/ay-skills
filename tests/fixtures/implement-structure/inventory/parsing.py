import csv
from io import StringIO

from .domain import StockAdjustment


def parse_adjustments(source: str) -> list[StockAdjustment]:
    adjustments = []
    for row in csv.DictReader(StringIO(source)):
        sku = row["sku"].strip()
        quantity = int(row["quantity"])
        if not sku or quantity == 0:
            raise ValueError("sku must be present and quantity must be nonzero")
        adjustments.append(StockAdjustment(sku=sku, quantity=quantity))
    return adjustments
