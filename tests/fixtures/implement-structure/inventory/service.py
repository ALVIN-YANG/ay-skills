from .parsing import parse_adjustments
from .repository import InMemoryInventoryRepository


def import_adjustments(source: str, repository: InMemoryInventoryRepository) -> int:
    adjustments = parse_adjustments(source)
    for adjustment in adjustments:
        repository.save(adjustment)
    return len(adjustments)
