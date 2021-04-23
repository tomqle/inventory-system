from __future__ import annotations
from django.db import models, transaction
from django.db.models import fields
from django.db.utils import IntegrityError
from datetime import datetime

# Create your models here.


class Supplier(models.Model):
    ACTIVE = 'ACT'
    INACTIVE = 'INA'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=ACTIVE)
    company_name = models.CharField(max_length=100, blank=True, default='')
    contact_name = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=100, null=True, blank=True, default='')
    phone = models.CharField(max_length=100, null=True, blank=True, default='')
    address1 = models.CharField(max_length=100, null=True, blank=True, default='')
    address2 = models.CharField(max_length=100, null=True, blank=True, default='')
    city = models.CharField(max_length=100, null=True, blank=True, default='')
    state = models.CharField(max_length=100, null=True, blank=True, default='')
    country = models.CharField(max_length=100, null=True, blank=True, default='')
    zipcode = models.CharField(max_length=100, null=True, blank=True, default='')
    payment_terms = models.CharField(max_length=100, null=True, blank=True, default='')


class Customer(models.Model):
    ACTIVE = 'ACT'
    INACTIVE = 'INA'

    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (INACTIVE, 'Inactive'),
    ]

    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=ACTIVE)
    company_name = models.CharField(max_length=100, blank=True, default='')
    contact_name = models.CharField(max_length=100, blank=True, default='')
    email = models.CharField(max_length=100, null=True, blank=True, default='')
    phone = models.CharField(max_length=100, null=True, blank=True, default='')
    address1 = models.CharField(max_length=100, null=True, blank=True, default='')
    address2 = models.CharField(max_length=100, null=True, blank=True, default='')
    city = models.CharField(max_length=100, null=True, blank=True, default='')
    state = models.CharField(max_length=100, null=True, blank=True, default='')
    country = models.CharField(max_length=100, null=True, blank=True, default='')
    zipcode = models.CharField(max_length=100, null=True, blank=True, default='')
    payment_terms = models.CharField(max_length=100, null=True, blank=True, default='')


class Product(models.Model):
    PUBLIC = 'PBL'
    PRIVATE = 'PRV'
    INACTIVE = 'INA'

    STATUS_CHOICES = [
        (PUBLIC, 'Public'),
        (PRIVATE, 'Private'),
        (INACTIVE, 'Inactive'),
    ]

    sku = models.CharField(max_length=100, blank=True, default='', unique=True)
    name = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=PRIVATE)
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT, blank=True, null=True)

    @property
    def qty(self) -> int:
        return sum(batch.available_qty for batch in self.batch_set.all())


class Order(models.Model):
    NEW = 'NEW'
    AWAITING_PAYMENT = "PMT"
    PROCESSING = 'PRC'
    ON_HOLD = 'ONH'
    PARTIALLY_PICKED = 'PPK'
    FULLY_PICKED = 'FPK'
    COMPLETED = 'CMP'
    CANCELED = 'CNC'
    VOID = 'VOI'

    STATUS_CHOICES = [
        (NEW, 'New'),
        (AWAITING_PAYMENT, 'Awaiting Payment'),
        (PROCESSING, 'Processing'),
        (ON_HOLD, 'On Hold'),
        (PARTIALLY_PICKED, 'Partially Picked'),
        (FULLY_PICKED, 'Fully PIcked'),
        (COMPLETED, 'Completed'),
        (CANCELED, 'Canceled'),
        (VOID, 'Void'),
    ]

    order_date = models.DateField(auto_now_add=True, blank=True)
    reference = models.CharField(max_length=100, blank=True, default='')
    #reference = models.CharField(max_length=100, blank=True, null=True, default='', unique=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=NEW)
    customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, blank=True, null=True)

    @property
    def total(self) -> float:
        return sum(order_line.subtotal for order_line in self.orderline_set.all())

    @property
    def quantity(self) -> int:
        return sum(order_line.qty for order_line in self.orderline_set.all())


class OrderLine(models.Model):
    order_ref = models.CharField(max_length=100, blank=True, default='')
    sku = models.CharField(max_length=100, blank=True, default='')
    qty = models.IntegerField()
    price = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.RESTRICT, blank=True, null=True)

    @property
    def allocated_qty(self) -> int:
        return sum(allocation.qty for allocation in self.allocation_set.all())

    @property
    def unallocated_qty(self) -> int:
        return self.qty - self.allocated_qty

    @property
    def allocated(self) -> bool:
        return self.unallocated_qty == 0

    @property
    def subtotal(self) -> float:
        return sum(self.qty * self.price)

    class Meta:
        unique_together = ['order_ref', 'sku', 'qty']


class PurchaseOrder(models.Model):
    AWAITING_APPROVAL = 'AWA'
    APPROVED = 'APV'
    DRAFT = 'DRF'
    ON_HOLD = 'ONH'
    PAID = 'PAI'
    VOID = 'VOI'

    STATUS_CHOICES = [
        (AWAITING_APPROVAL, 'Awaiting Approval'),
        (APPROVED, 'Approved'),
        (DRAFT, 'Draft'),
        (ON_HOLD, 'On Hold'),
        (PAID, 'Paid'),
        (VOID, 'Void'),
    ]

    created_date = models.DateField(auto_now_add=True, blank=True)
    reference = models.CharField(max_length=100, blank=True, null=True, default='', unique=True)
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, blank=True, null=True, default=DRAFT)
    supplier = models.ForeignKey(Supplier, on_delete=models.RESTRICT, blank=True, null=True)

    def clean(self):
        self.reference = self.reference.upper()
    
    def save(self, *args, **kwargs):
        self.full_clean()
        return super(PurchaseOrder, self).save(*args, **kwargs)


class PurchaseOrderLine(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    qty = models.IntegerField(default=1, blank=True)
    cost = models.IntegerField(default=0, blank=True)
    sku = models.CharField(max_length=100, blank=True, default='')

    @property
    def received_qty(self):
        return sum(reception.batch.qty for reception in self.reception_set.all())

    @property
    def incoming_qty(self):
        return self.qty - self.received_qty

    @property
    def allocated_qty(self):
        pass

    @property
    def subtotal(self):
        return self.qty * self.cost

    #def receive(self, qty: int):
        #if self.can_receive(qty):
            #Batch.objects.create(sku=self.sku, product=self.product, purchase_order_line=self, qty=qty)

    def can_receive(self, qty: int):
        if qty <= self.incoming_qty:
            return True
        return False


class Batch(models.Model):
    reference = models.CharField(max_length=100, blank=True, default='')
    sku = models.CharField(max_length=100, blank=True, default='')
    eta = models.DateField(null=True, blank=True)
    order_lines = models.ManyToManyField(OrderLine, through='Allocation')
    qty = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.RESTRICT, null=True)

    @property
    def allocated_qty(self) -> int:
        return sum(allocation.qty for allocation in self.allocation_set.all())

    @property
    def available_qty(self) -> int:
        return self.qty - self.allocated_qty

    def __repr__(self):
        return f'<Batch {self.reference}>'

    def __eq__(self, other):
        if not isinstance(other, Batch):
            return False
        return other.reference == self.reference
    
    def __hash__(self):
        return hash(self.reference)

    def __gt__(self, other):
        if self.eta is None:
            return False
        if other.eta is None:
            return True
        return self.eta > other.eta

    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            Allocation.objects.create(batch=self, order_line=line, qty=min(self.available_qty, line.unallocated_qty))

            #try:
                #with transaction.atomic():
                    #Allocation.objects.create(batch=self, order_line=line)
            #except IntegrityError:
                #pass

    def can_allocate(self, line: OrderLine) -> bool:
        return self.sku == line.sku and self.available_qty > 0

    def has_been_allocated(self) -> bool:
        return self.allocated_qty > 0


class Allocation(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.RESTRICT)
    order_line = models.ForeignKey(OrderLine, on_delete=models.RESTRICT)
    date_allocated = models.DateField(auto_now_add=True, blank=True)
    qty = models.IntegerField(default=0, blank=True)

    class Meta:
        unique_together = ['batch', 'order_line', 'qty']


class Reception(models.Model):
    purchase_order_line = models.ForeignKey(PurchaseOrderLine, on_delete=models.RESTRICT, null=True)
    batch = models.OneToOneField(Batch, on_delete=models.RESTRICT, blank=True, null=True)
    qty = models.IntegerField(default=0, blank=True)


class InboundShipment(models.Model):
    AWAITING_APPROVAL = 'AWA'
    APPROVED = 'APV'
    COMPLETED = 'CMP'
    DRAFT = 'DRF'
    ON_HOLD = 'ONH'
    VOID = 'VOI'

    STATUS_CHOICES = [
        (AWAITING_APPROVAL, 'Public'),
        (APPROVED, 'Private'),
        (COMPLETED, 'Completed'),
        (DRAFT, 'Draft'),
        (ON_HOLD, 'Inactive'),
        (VOID, 'Void'),
    ]

    created_date = models.DateField(auto_now_add=True, blank=True)
    reference = models.CharField(max_length=100, blank=True, default='')
    status = models.CharField(max_length=3, choices=STATUS_CHOICES, default=DRAFT)


class InboundShipmentLine(models.Model):
    inbound_shipment = models.ForeignKey(InboundShipment, on_delete=models.RESTRICT)
    purchase_order_line = models.ForeignKey(PurchaseOrderLine, on_delete=models.RESTRICT)
    qty = models.IntegerField(default=1, blank=True)

    @property
    def qty_received(self) -> int:
        return sum(batch.qty for batch in self.batch_set.all())

    def is_valid_qty(self) -> bool:
        return self.qty <= self.purchase_order_line.qty

