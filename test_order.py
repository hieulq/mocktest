import unittest

from order import Order
from warehouse import Warehouse

import mox
import mock

TALISKER = "Talisker"
HIGHLAND_PARK = "Highland Park"


class OrderTests(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.add(TALISKER, 50)
        self.warehouse.add(HIGHLAND_PARK, 25)

    def test_order_is_filled_if_enough_in_warehouse(self):
        order = Order(TALISKER, 50)
        order.fill(self.warehouse)
        self.assertTrue(order.is_filled())
        self.assertEqual(self.warehouse.get_inventory(TALISKER), 0)

    def test_order_does_not_remove_if_not_enough(self):
        order = Order(TALISKER, 51)
        order.fill(self.warehouse)
        self.assertFalse(order.is_filled())
        self.assertEqual(self.warehouse.get_inventory(TALISKER), 50)


class WarehouseTests(unittest.TestCase):

    def setUp(self):
        self.warehouse = Warehouse()
        self.warehouse.add('Glenlivit', 10)

    def test_warehouse_shows_new_inventory(self):
       self.assertEqual(self.warehouse.get_inventory('Glenlivit'), 10)

    def test_warehouse_shows_added_inventory(self):
        self.warehouse.add('Glenlivit', 15)
        self.assertEqual(self.warehouse.get_inventory('Glenlivit'), 25)

    def test_warehouse_shows_removed_inventory(self):
        self.warehouse.remove('Glenlivit', 10)
        self.assertEqual(self.warehouse.get_inventory('Glenlivit'), 0)


class OrderTestsWithMox(unittest.TestCase):

    def test_order_is_filled_if_enough_in_warehouse(self):
        # Create the Order as usual
        order = Order(TALISKER, 50)

        # Create the mock warehouse object in record mode
        mocker = mox.Mox()
        warehouse = mocker.CreateMockAnything()

        # Record the sequence of actions expected from the Order object
        warehouse.get_inventory(TALISKER).AndReturn(50)
        warehouse.remove(TALISKER, 50)

        # Put all mock objects in replay mode
        mocker.ReplayAll()

        # Exercise the Order object
        order.fill(warehouse)

        # Verify that the order is filled and that the warehouse saw
        # the correct behavior
        self.assertTrue(order.is_filled())
        mocker.VerifyAll()


class OrderTestWithMock(unittest.TestCase):

    @mock.patch('warehouse.Warehouse')
    def test_order_filled_if_enough_in_warehouse(self, mock_wh):
        order = Order(TALISKER, 50)

        mock_wh.add(TALISKER, 50)

        order.fill(mock_wh)

        self.assertTrue(order.is_filled())
        mock_wh.get_inventory.assert_called_once_with(TALISKER)
        mock_wh.remove.assert_called_once_with(TALISKER, 50)
