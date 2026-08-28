from decimal import Decimal
import unittest

from orders import InMemoryOrderRepository, import_orders


class ImportOrdersTests(unittest.TestCase):
    def test_imports_valid_order_lines(self) -> None:
        repository = InMemoryOrderRepository()
        result = import_orders(
            "sku,quantity,unit_price\nA-1,2,3.25\nB-2,1,6.00\n",
            repository,
        )

        self.assertEqual(result.accepted_count, 2)
        self.assertEqual(result.total, Decimal("12.50"))
        self.assertEqual([line.sku for line in repository.all()], ["A-1", "B-2"])

    def test_rejects_invalid_order_lines(self) -> None:
        invalid_sources = (
            "sku,quantity,unit_price\n,1,2.00\n",
            "sku,quantity,unit_price\nA-1,0,2.00\n",
            "sku,quantity,unit_price\nA-1,1,-2.00\n",
        )
        for source in invalid_sources:
            with self.subTest(source=source):
                with self.assertRaises(ValueError):
                    import_orders(source, InMemoryOrderRepository())


if __name__ == "__main__":
    unittest.main()
