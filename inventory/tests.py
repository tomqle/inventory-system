from django.test import TestCase
from inventory.models import Address, Allocation, Batch, Customer, Product, PurchaseOrder, PurchaseOrderLine, SalesOrder, SalesOrderLine, Supplier
from inventory import services

#-- START models tests --#
class BatchTestCase(TestCase):
    def setUp(self):
        pass

    # TODO 
    # 1. Allocate batch only if there is quantity available
    # 2. Allocate batch on hand over batch in transit
    # 3. Value of available and allocated quantity
    # 4. Get batch with allocations
    def test_allocate_batch(self):
        pass



#-- END models tests --#


#-- START services tests --#
class ServiceTestCase(TestCase):
    def setUp(self):
        pass

    # START batch #

    def test_allocate_multiple_batches_to_single_order_line(self):
        line = SalesOrderLine.objects.create(order_ref="ORDER-1", sku="SMALL-PRODUCT", qty=5)
        batch1 = Batch.objects.create(reference="SMALL-BATCH-1", sku="SMALL-PRODUCT", qty=2)
        batch2 = Batch.objects.create(reference="SMALL-BATCH-2", sku="SMALL-PRODUCT", qty=10)

        allocated_batches = services.allocate(line, [batch1, batch2])

        self.assertEqual(allocated_batches, ["SMALL-BATCH-1", "SMALL-BATCH-2"])
        self.assertEqual(line.unallocated_qty, 0)
        self.assertEqual(batch1.available_qty, 0)
        self.assertEqual(batch2.available_qty, 7)

    def test_allocate_single_batch_to_order_line(self):
        line = SalesOrderLine.objects.create(order_ref="ORDER-1", sku="SMALL-PRODUCT", qty=5)
        batch1 = Batch.objects.create(reference="SMALL-BATCH-1", sku="SMALL-PRODUCT", qty=0)
        batch2 = Batch.objects.create(reference="SMALL-BATCH-2", sku="SMALL-PRODUCT", qty=10)
        batch3 = Batch.objects.create(reference="SMALL-BATCH-3", sku="SMALL-PRODUCT", qty=3)

        allocated_batches = services.allocate(line, [batch1, batch2, batch3])

        self.assertEqual(allocated_batches, ["SMALL-BATCH-2"])
        self.assertEqual(line.unallocated_qty, 0)
        self.assertEqual(batch1.available_qty, 0)
        self.assertEqual(batch2.available_qty, 5)
        self.assertEqual(batch3.available_qty, 3)

    def test_order_line_with_no_allocations(self):
        line = SalesOrderLine.objects.create(order_ref="ORDER-1", sku="SMALL-PRODUCT", qty=5)

        self.assertEqual(line.allocated_qty, 0)

    # END batch #


    # START PurchaseOrder #

    def test_create_purchase_order_no_ref(self):
        purchase_order_dict = {}

        purchase_order = services.create_purchase_order(**purchase_order_dict)

        self.assertEqual(purchase_order.reference, f"PO-{purchase_order.id}")
        self.assertEqual(purchase_order.status, "DRF")

    def test_create_purchase_order_custom_ref(self):
        purchase_order_dict = {
            'reference': 'PO-1',
            'status': 'APV'
        }

        purchase_order = services.create_purchase_order(**purchase_order_dict)

        self.assertEqual(purchase_order.reference, "PO-1")
        self.assertEqual(purchase_order.status, "APV")

    def test_create_purchase_order_lines(self):
        product = Product.objects.create(name="USB Flash Drive", status="PRV", sku="FLASH-DRIVE")
        purchase_order = PurchaseOrder.objects.create()

        purchase_order_line_dict = {
            'sku': 'FLASH-DRIVE',
            'qty': 5,
            'cost': 2,
            'purchase_order_id': purchase_order.id,
            'product_id': product.id,
        }

        purchase_order_line = services.create_purchase_order_line(**purchase_order_line_dict)

        self.assertEqual(purchase_order_line.sku, 'FLASH-DRIVE')
        self.assertEqual(purchase_order_line.qty, 5)
        self.assertEqual(purchase_order_line.cost, 2)
        self.assertEqual(purchase_order_line.product_id, product.id)
        self.assertEqual(purchase_order_line.purchase_order_id, purchase_order.id)

    def test_update_purchase_order_lines(self):
        product1 = Product.objects.create(name="Heart Keychain", status="PRV", sku="KEYCHAIN-HEART")
        product2 = Product.objects.create(name="Clover Keychain", status="PRV", sku="KEYCHAIN-CLOVER")
        purchase_order = PurchaseOrder.objects.create(status="DRF", reference="PO-1")
        PurchaseOrderLine.objects.create(purchase_order_id=purchase_order.id, product_id=product1.id, sku=product1.sku, qty=1, cost=3)
        purchase_order_line_data = {
            'id': 1,
            'purchase_order_id': purchase_order.id,
            'sku': product2.sku,
            'qty': 9,
            'cost': 4
        }

        purchase_order_line = services.update_purchase_order_line(**purchase_order_line_data)

        for po_line in PurchaseOrderLine.objects.all():
            print(po_line)

        self.assertEqual(purchase_order_line.id, 1)
        self.assertEqual(purchase_order_line.purchase_order_id, 1)
        self.assertEqual(purchase_order_line.product_id, 2)
        self.assertEqual(purchase_order_line.sku, "KEYCHAIN-CLOVER")
        self.assertEqual(purchase_order_line.qty, 9)
        self.assertEqual(purchase_order_line.cost, 4)

    def test_delete_purchase_order_lines_not_present(self):
        product1 = Product.objects.create(name="Mechanical Keyboard", status="PRV", sku="KEYBOARD-MECH")
        product2 = Product.objects.create(name="HD Webcam 1080p", status="PRV", sku="WEBCAM-HD")
        product3 = Product.objects.create(name="USB Microphone", status="PRV", sku="MIC-USB")

        purchase_order = PurchaseOrder.objects.create(reference="PO-1", status="DRF")

        purchase_order_line1 = PurchaseOrderLine.objects.create(purchase_order=purchase_order, product=product1, sku=product1.sku, qty=3, cost=4)
        PurchaseOrderLine.objects.create(purchase_order=purchase_order, product=product2, sku=product2.sku, qty=5, cost=1)


        purchase_order_lines_data = [
            {
                "id": 1,
                "product_id": 1,
                "sku": product1.sku,
                "qty": 3,
                "cost": 4
            },
            {
                "product_id": 3,
                "sku": product3.sku,
                "qty": 1,
                "cost": 10
            }
        ]

        services.delete_purchase_order_lines_not_present(purchase_order.id, purchase_order_lines_data)

        purchase_order_lines = PurchaseOrderLine.objects.filter(purchase_order_id=purchase_order.id)

        self.assertEqual(purchase_order_lines.count(), 1)
        self.assertEqual(purchase_order_lines[0].id, 1)

    # END PurchaseOrder #

    # START Reception #

    def test_receive_purchase_order_line(self):
        product = Product.objects.create(name="Mechanical Keyboard", status="PRV", sku="KEYBOARD-MECH")
        purchase_order = PurchaseOrder.objects.create(reference="PO-1", status="APV")
        purchase_order_line = PurchaseOrderLine.objects.create(purchase_order=purchase_order, product=product, sku=product.sku, qty=10, cost=4)
        received_qty = 5

        reception_data = {
            "purchase_order_line": purchase_order_line,
            "qty": received_qty
        }

        reception = services.receive_purchase_order_line(**reception_data)
        batch = reception.batch

        self.assertEqual(reception.qty, received_qty)
        self.assertEqual(batch.qty, received_qty)
        self.assertEqual(product.qty, received_qty)
        self.assertEqual(purchase_order_line.received_qty, received_qty)

    def test_update_receive_purchase_order_line(self):
        pass
        #self.assertEqual()

    # END   Reception #

    # START SalesOrder #

    def test_create_sales_order(self):
        product = Product.objects.create(name="Mechanical Keyboard", status="PRV", sku="KEYBOARD-MECH")
        address = Address.objects.create(address1="8584 Industrial Rd", city="Naperville", state="IL", postal_code="60540", country="US")
        customer = Customer.objects.create(status='ACT', company='Bland Co.', name='Bill Bland', email='bill@blandco.com', phone='800-123-4567', payment_terms="Pay in advance", address=address)
        sales_order_data = {
            "status": "APV",
            "customer": customer,
        }

        #sales_order = services.create_sales_order(**sales_order_data)

        #self.assertEqual(sales_order.status, "APV")
        #self.assertEqual(sales_order.customer_id, customer.id)
        #self.assertEqual(sales_order.reference, "SO-1")

    def test_update_sales_order(self):
        pass

    def test_create_sales_order_line(self):
        pass

    def test_update_sales_order_line(self):
        pass

    # END   SalesOrder #

#-- END services tests --#
