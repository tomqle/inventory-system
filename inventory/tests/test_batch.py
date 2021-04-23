from django.test import TestCase
from inventory.models import Allocation, Batch, OrderLine

class BatchTestCase(TestCase):

    def setUp(self):
        pass

    def test_allocating_to_a_batch_reduces_the_available_quantity(self):
        line = OrderLine.objects.create(order_ref="order1", sku="BLACK-SHOES", qty=2)
        batch = Batch.objects.create(reference="batch1", sku="BLACK-SHOES", purchased_quantity=20)

        batch.allocate(line)

        self.assertEqual(batch.available_quantity, 18)

    def test_can_allocate_if_available_greater_than_required(self):
        line = OrderLine.objects.create(order_ref="order2", sku="BLUE-STOOL", qty=3)
        batch = Batch.objects.create(reference="batch2", sku="BLUE-STOOL", purchased_quantity=10)

        self.assertEqual(batch.can_allocate(line), True)

    def test_cannot_allocate_if_available_smaller_than_required(self):
        line = OrderLine.objects.create(order_ref="order3", sku="GREEN-STOOL", qty=10)
        batch = Batch.objects.create(reference="batch3", sku="GREEN-STOOL", purchased_quantity=1)

        self.assertEqual(batch.can_allocate(line), False)

    def test_can_allocate_if_available_equal_to_required(self):
        line = OrderLine.objects.create(order_ref="order4", sku="PURPLE-STOOL", qty=10)
        batch = Batch.objects.create(reference="batch4", sku="PURPLE-STOOL", purchased_quantity=10)

        self.assertEqual(batch.can_allocate(line), True)

    def test_cannot_allocate_if_skus_do_not_match(self):
        line = OrderLine.objects.create(order_ref="order5", sku="RED-STOOL", qty=10)
        batch = Batch.objects.create(reference="batch5", sku="WHITE-STOOL", purchased_quantity=10)

        self.assertEqual(batch.can_allocate(line), False)

    def test_allocation_is_idempotent(self):
        line = OrderLine.objects.create(order_ref="order5", sku="ORANGE-STOOL", qty=3)
        batch = Batch.objects.create(reference="batch5", sku="ORANGE-STOOL", purchased_quantity=20)

        batch.allocate(line)
        batch.allocate(line)

        self.assertEqual(batch.available_quantity, 17)

    def test_deallocate(self):
        pass

    def test_can_only_deallocate_allocated_lines(self):
        pass
