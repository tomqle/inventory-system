from re import I
from django.db.utils import ConnectionDoesNotExist, IntegrityError
from django.utils.text import slugify
from rest_framework import response
from inventory.models import Address, Allocation, Batch, Customer, InboundShipment, InboundShipmentLine, SalesOrder, SalesOrderLine, Product, PurchaseOrder, PurchaseOrderLine, Reception, Supplier
from typing import List, Optional, Set



# -------------------- START Batch services -------------------- #

class OutOfStock(Exception):
    pass

def allocate(line: SalesOrderLine, batches: List[Batch]) -> List[str]:
    try:
        for batch in sorted(batches):
            batch.allocate(line)
            if line.unallocated_qty == 0:
                break

        return [batch.reference for batch in line.batch_set.all()]
    except StopIteration:
        raise OutOfStock(f'Out of stock for sku {line.sku}')

# -------------------- END Batch services -------------------- #



# -------------------- START Order services -------------------- #

def init_order():
    pass

def add_order_line_to_order():
    pass

# -------------------- END Order services -------------------- #



# -------------------- START PurchaseOrder services -------------------- #

def validate_purchase_order(**kwargs):
    if 'reference' not in kwargs.keys() or kwargs['reference'] == None or kwargs['reference'] == '':
        kwargs['reference'] = f"PO-{kwargs['reference']}"
    else:
        kwargs['reference'] = slugify(kwargs['reference']).upper()

    if 'status' in kwargs.keys() and (kwargs['status'] == None or kwargs['status'] == ''):
            kwargs['status'] = 'DRF'
    else:
        kwargs['status']

    if PurchaseOrder.objects.filter(reference=kwargs['reference']).first() != None:
        return kwargs, False

    return kwargs, True

def create_purchase_order(**kwargs) -> PurchaseOrder:
    if 'reference' in kwargs.keys():
        if not _purchase_order_has_valid_reference(kwargs['reference']):
            return PurchaseOrder()

    if 'status' in kwargs.keys():
        if kwargs['status'] == None or kwargs['status'] == '':
            kwargs['status'] = 'DRF'
        elif kwargs['status'] not in [x for (x, y) in PurchaseOrder.STATUS_CHOICES]:
            return PurchaseOrder()

    purchase_order = PurchaseOrder.objects.create(**kwargs)

    if purchase_order.reference == None or purchase_order.reference == '':
        purchase_order.reference = f'PO-{purchase_order.id}'
    else:
        purchase_order.reference = slugify(purchase_order.reference).upper()

    if purchase_order.status == None or purchase_order.status == '':
        purchase_order.status = 'DRF'

    purchase_order.save()

    return purchase_order

def update_purchase_order(**kwargs) -> PurchaseOrder:
    if 'reference' in kwargs.keys():
        if not _purchase_order_has_valid_reference(kwargs['reference']):
            return PurchaseOrder()

    #purchase_order = _perform_update_purchase_order(**kwargs)

    purchase_order = PurchaseOrder.objects.get(id=kwargs['id'])

    if 'reference' in kwargs.keys():
        if purchase_order.reference == '':
            purchase_order.reference = f'PO-{purchase_order.id}'
        else:
            purchase_order.reference = slugify(kwargs['reference']).upper()

    return purchase_order

def create_purchase_order_line(**kwargs) -> PurchaseOrderLine:
    purchase_order_line = PurchaseOrderLine(**kwargs)

    product = Product.objects.filter(sku=purchase_order_line.sku).first()

    if product != None:
        purchase_order_line.product = product
        purchase_order_line.save()

    return purchase_order_line

def update_purchase_order_line(**kwargs) -> PurchaseOrderLine:
    purchase_order_line = PurchaseOrderLine.objects.get(id=kwargs['id'])
    if Product.objects.filter(sku=kwargs['sku']).count() != 0:
        purchase_order_line.sku = kwargs.get('sku', purchase_order_line.sku)
        purchase_order_line.product = Product.objects.filter(sku=kwargs['sku'])[0]
    
    purchase_order_line.qty = kwargs.get('qty', purchase_order_line.qty)
    purchase_order_line.cost = kwargs.get('cost', purchase_order_line.cost)

    purchase_order_line.save()

    return purchase_order_line

def add_purchase_order_line_to_purchase_order(purchase_order_id, sku, qty, cost):
    try:
        product_id = Product.objects.get(sku=sku).id
        line = PurchaseOrderLine(purchase_order_id=purchase_order_id, sku=sku, qty=qty, cost=cost, product_id=product_id)
        line.save
        return True
    except(Product.DoesNotExist):
        return False

def get_purchase_order_lines_from_purchase_order(purchase_order_id):
    return PurchaseOrderLine.objects.filter(purchase_order_id=purchase_order_id)

def delete_purchase_order_lines_not_present(purchase_order_id, purchase_order_lines_data):
    purchase_order_lines_id = set(po_line.id for po_line in get_purchase_order_lines_from_purchase_order(purchase_order_id))

    purchase_order_lines_data_id = [po_line.get('id', -1) for po_line in purchase_order_lines_data]

    purchase_order_lines_id_del = list(purchase_order_lines_id.symmetric_difference(purchase_order_lines_data_id))

    delete_purchase_order_lines(purchase_order_lines_id_del)

def delete_purchase_order_lines(purchase_order_lines_id):
    PurchaseOrderLine.objects.filter(pk__in=purchase_order_lines_id).delete()


# START Helper #

def _purchase_order_has_valid_reference(reference):
    if PurchaseOrder.objects.filter(reference=reference).first() != None:
        return False
    return True

def _perform_update_purchase_order(**kwargs):
    purchase_order = PurchaseOrder.objects.get(id=kwargs['id'])
    purchase_order.update()

# END   Helper #

# -------------------- END PurchaseOrder services -------------------- #


# -------------------- START Reception services -------------------- #


def receive_purchase_order_line(**kwargs):
    purchase_order_line = PurchaseOrderLine()
    if 'purchase_order_line' in kwargs.keys():
        purchase_order_line = kwargs['purchase_order_line']

    reception = Reception()
    if 'qty' in kwargs.keys() and purchase_order_line.can_receive(kwargs['qty']):
        qty = kwargs['qty']
        _create_reception(purchase_order_line, qty)

    return reception


def update_receive_purchase_order_line(reception, **kwargs):
    #reception = Reception.objects.get(id=kwargs['id'])
    #purchase_order_line = reception.purchase_order_line

    # TODO: add check for purchase_order_line

    print(reception)

    if not reception.batch.has_been_allocated():
        if 'qty' in kwargs.keys() and reception.purchase_order_line.can_receive(kwargs['qty']):
            qty = kwargs['qty']
            reception = _update_reception(reception, qty)

    return reception


# START Helper #

def _create_reception(purchase_order_line, qty):
    batch = Batch.objects.create(sku=purchase_order_line.sku, product=purchase_order_line.product, qty=qty)
    reception = Reception.objects.create(purchase_order_line=purchase_order_line, batch=batch, qty=qty)

def _update_reception(reception, qty):
    reception.qty = qty
    reception.save()

    reception.batch.qty = qty
    reception.batch.save()
    return reception

# END   Helper #


# -------------------- END Reception services -------------------- #


# -------------------- START Customer services -------------------- #


def create_customer(**kwargs):
    if 'status' in kwargs.keys():
        if kwargs['status'] == None or kwargs['status'] == '':
            kwargs['status'] = 'ACT'
        elif kwargs['status'] not in [x for (x, y) in Customer.STATUS_CHOICES]:
            return Customer()

    address_data = kwargs.pop('address')
    customer = Customer.objects.create(**kwargs)
    customer.address = create_address(**address_data)
    customer.save()

    return customer

def update_customer(customer_id, **kwargs):
    customer = Customer.objects.get(id=customer_id)
    if 'status' in kwargs.keys():
        if kwargs['status'] not in [x for (x, y) in Customer.STATUS_CHOICES]:
            kwargs['status'] = customer.status

    address_data = kwargs.pop('address')
    Customer.objects.filter(pk=customer_id).update(**kwargs)

    customer = Customer.objects.get(id=customer_id)
    update_address(customer.address_id, **address_data)
    customer.save()

    return customer


# -------------------- END Customer services -------------------- #


# -------------------- START Supplier services -------------------- #


def create_supplier(**kwargs):
    if 'status' in kwargs.keys():
        if kwargs['status'] == None or kwargs['status'] == '':
            kwargs['status'] = 'ACT'
        elif kwargs['status'] not in [x for (x, y) in Supplier.STATUS_CHOICES]:
            return Supplier()

    address_data = kwargs.pop('address')
    supplier = Supplier.objects.create(**kwargs)
    supplier.address = create_address(**address_data)
    supplier.save()

    return supplier


def update_supplier(supplier_id, **kwargs):
    supplier = Supplier.objects.get(id=supplier_id)
    if 'status' in kwargs.keys():
        if kwargs['status'] not in [x for (x, y) in Supplier.STATUS_CHOICES]:
            kwargs['status'] = supplier.status

    address_data = kwargs.pop('address')
    Supplier.objects.filter(pk=supplier_id).update(**kwargs)

    supplier = Supplier.objects.get(id=supplier_id)
    update_address(supplier.address_id, **address_data)
    supplier.save()

    return supplier


# -------------------- END Supplier services -------------------- #


# -------------------- START Address services -------------------- #


def create_address(**kwargs):
    return Address.objects.create(**kwargs)

def update_address(address_id, **kwargs):
    return Address.objects.update(**kwargs)


# -------------------- END Address services -------------------- #


# -------------------- START InboundShipment services -------------------- #


def create_inbound_shipment(**kwargs) -> InboundShipment:
    if 'reference' in kwargs.keys():
        if not _inbound_shipment_has_valid_reference(kwargs['reference']):
            return InboundShipment()

    if 'status' in kwargs.keys():
        if kwargs['status'] == None or kwargs['status'] == '':
            kwargs['status'] = 'DRF'
        elif kwargs['status'] not in [x for (x, y) in InboundShipment.STATUS_CHOICES]:
            return InboundShipment()

    inbound_shipment = InboundShipment.objects.create(**kwargs)

    if inbound_shipment.reference == None or inbound_shipment.reference == '':
        inbound_shipment.reference = f'PO-{inbound_shipment.id}'
    else:
        inbound_shipment.reference = slugify(inbound_shipment.reference).upper()

    if inbound_shipment.status == None or inbound_shipment.status == '':
        inbound_shipment.status = 'DRF'

    inbound_shipment.save()

    return inbound_shipment

def update_inbound_shipment(**kwargs) -> InboundShipment:
    pass

def create_inbound_shipment_line(**kwargs) -> InboundShipmentLine:
    inbound_shipment_line = InboundShipmentLine(**kwargs)

    #product = Product.objects.filter(sku=purchase_order_line.sku).first()

    #if product != None:
        #purchase_order_line.product = product
        #purchase_order_line.save()

    purchase_order_line = PurchaseOrderLine.objects.filter(id=inbound_shipment_line.id).first()

    if purchase_order_line != None:
        if inbound_shipment_line.is_valid_qty():
            #inbound_shipment_line.purchase_order_line = purchase_order_line
            inbound_shipment_line.save()

    return inbound_shipment_line

def update_inbound_shipment_line(**kwargs) -> InboundShipmentLine:
    inbound_shipment_line = InboundShipmentLine.objects.filter(id=kwargs['id']).first()

    if inbound_shipment_line:
        purchase_order_line = PurchaseOrderLine.objects.filter(id=kwargs['purchase_order_line_id']).first()

        if purchase_order_line:
            if inbound_shipment_line.is_valid_qty():
                inbound_shipment_line.purchase_order_line = purchase_order_line
                inbound_shipment_line.qty = kwargs['qty']
                inbound_shipment_line.save()

    return inbound_shipment_line

def delete_inbound_shipment_lines_not_present(inbound_shipment_id, inbound_shipment_lines_data):
    inbound_shipment_lines_id = set(inbound_shipment_line.id for inbound_shipment_line in get_inbound_shipment_lines_from_inbound_shipment(inbound_shipment_id))

    inbound_shipment_lines_data_id = [inbound_shipment_line_data.get('id', -1) for inbound_shipment_line_data in inbound_shipment_lines_data]

    purchase_order_lines_id_del = list(inbound_shipment_lines_id.symmetric_difference(inbound_shipment_lines_data_id))

    delete_inbound_shipment_lines(purchase_order_lines_id_del)

def delete_inbound_shipment_lines(inbound_shipment_lines_id):
    InboundShipmentLine.objects.filter(pk__in=inbound_shipment_lines_id).delete()

def get_inbound_shipment_lines_from_inbound_shipment(inbound_shipment_id):
    return InboundShipmentLine.objects.filter(inbound_shipment_id=inbound_shipment_id)

def add_inbound_shipment_line_to_shipment(shipment: InboundShipment, inbound_line: InboundShipmentLine):
    pass

def receive_inbound_shipment_line(InboundShipmentLine, int) -> Batch:
    pass


# START Helper #

def _inbound_shipment_has_valid_reference(reference):
    if InboundShipment.objects.filter(reference=reference).first() != None:
        return False
    return True


# END   Helper #


# -------------------- END InboundShipment services -------------------- #

