from datetime import date, timedelta
from django.test import TestCase
from inventory.models import Allocation, Batch, OrderLine
from inventory import services

class AllocateTestCase(TestCase):
    def setUp(self):
        self.today = date.today()
        self.tomorrow = self.today + timedelta(days=1)
        self.later = self.today + timedelta(days=2)

    def test_prefers_current_stock_batches_to_shipments(self):
        line = OrderLine.objects.create(order_ref="ORDER-1", sku="RETRO-CLOCK", qty=10)
        air_shipment_batch = Batch.objects.create(reference="air-shipment-batch", sku="RETRO-CLOCK", purchased_quantity=100, eta=self.tomorrow)
        in_stock_batch = Batch.objects.create(reference="in-stock-batch", sku="RETRO-CLOCK", purchased_quantity=100, eta=None)
        sea_shipment_batch = Batch.objects.create(reference="sea-shipment-batch", sku="RETRO-CLOCK", purchased_quantity=100, eta=self.later)

        services.allocate(line, [air_shipment_batch, in_stock_batch, sea_shipment_batch])

        self.assertEqual(in_stock_batch.available_quantity, 90)
        self.assertEqual(air_shipment_batch.available_quantity, 100)
        self.assertEqual(sea_shipment_batch.available_quantity, 100)

    def test_prefers_earlier_batches(self):
        line = OrderLine.objects.create(order_ref="ORDER-1", sku="MINIMALIST_SPOON", qty=10)
        tomorrow_batch = Batch.objects.create(reference="tomorrow-batch", sku="MINIMALIST_SPOON", purchased_quantity=100, eta=self.tomorrow)
        today_batch = Batch.objects.create(reference="today-batch", sku="MINIMALIST_SPOON", purchased_quantity=100, eta=self.today)
        later_batch = Batch.objects.create(reference="later-batch", sku="MINIMALIST_SPOON", purchased_quantity=100, eta=self.later)

        services.allocate(line, [tomorrow_batch, today_batch, later_batch])

        self.assertEqual(today_batch.available_quantity, 90)
        self.assertEqual(tomorrow_batch.available_quantity, 100)
        self.assertEqual(later_batch.available_quantity, 100)

    def test_returns_allocated_batch_ref(self):
        line = OrderLine.objects.create(order_ref="ORDER-1", sku="HIGHBROW-POSTER", qty=10)
        air_shipment_batch = Batch.objects.create(reference="air-shipment-batch-2", sku="HIGHBROW-POSTER", purchased_quantity=100, eta=self.tomorrow)
        in_stock_batch = Batch.objects.create(reference="in-stock-batch-2", sku="HIGHBROW-POSTER", purchased_quantity=100, eta=None)

        batch_ref = services.allocate(line, [air_shipment_batch, in_stock_batch])

        self.assertEqual(batch_ref, "in-stock-batch-2")


    def test_raises_out_of_stock_exception_if_cannot_allocate(self):
        line1 = OrderLine.objects.create(order_ref='order1', sku='SMALL-FORK', qty=10)
        batch = Batch.objects.create(reference='batch1', sku='SMALL-FORK', purchased_quantity=10, eta=self.today)
        services.allocate(line1, [batch])

        line2 = OrderLine.objects.create(order_ref='order2', sku='SMALL-FORK', qty=1)

        with self.assertRaises(services.OutOfStock):
            services.allocate(line2, [batch])

