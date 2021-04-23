from django.contrib.auth.models import User, Group
from rest_framework import serializers

from inventory.models import Allocation, Batch, InboundShipment, InboundShipmentLine, Order, OrderLine, Product, PurchaseOrder, PurchaseOrderLine, Reception
from inventory import services


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'url', 'name']

class AllocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Allocation
        fields = ['id', 'batch', 'order_line', 'qty']

class BatchSerializer(serializers.HyperlinkedModelSerializer):
    allocated_qty = serializers.SerializerMethodField()
    available_qty = serializers.SerializerMethodField()

    class Meta:
        model = Batch
        fields = ['id', 'reference', 'product', 'sku', 'eta', 'order_lines', 'qty', 'allocated_qty', 'available_qty']

    def get_allocated_qty(self, instance):
        return instance.allocated_qty

    def get_available_qty(self, instance):
        return instance.available_qty

class OrderLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderLine
        fields = ['id', 'order_ref', 'product', 'sku', 'qty', 'allocated_qty', 'unallocated_qty', 'allocated']
    
    def get_allocated_qty(self, instance):
        return instance.allocated_qty

    def get_unallocated_qty(self, instance):
        return instance.unallocated_qty

    def get_allocated(self, instance):
        return instance.allocated

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'sku', 'name', 'status', 'qty']

    def get_qty(self, instance):
        return instance.qty

class PurchaseOrderLineSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(required=False)
    received_qty = serializers.SerializerMethodField()
    incoming_qty = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseOrderLine
        fields = ['id', 'product', 'sku', 'qty', 'cost', 'subtotal', 'received_qty', 'incoming_qty']
        read_only_fields = ['product']

    def get_subtotal(self, instance):
        return instance.subtotal

    def get_received_qty(self, instance):
        return instance.received_qty

    def get_incoming_qty(self, instance):
        return instance.incoming_qty

class PurchaseOrderSerializer(serializers.HyperlinkedModelSerializer):
    purchase_order_lines = PurchaseOrderLineSerializer(source='purchaseorderline_set', many=True, read_only=False)

    class Meta:
        model = PurchaseOrder
        fields = ['id', 'reference', 'status', 'purchase_order_lines']

    def create(self, validated_data):
        purchase_order_lines_data = validated_data.pop('purchaseorderline_set')
        purchase_order = services.create_purchase_order(**validated_data)

        for purchase_order_line_data in purchase_order_lines_data:
            purchase_order_line_data['purchase_order_id'] = purchase_order.id
            services.create_purchase_order_line(purchase_order_line_data)
            #product = Product.objects.get(sku=purchase_order_line_data['sku'])
            #purchase_order_line_data['product'] = product

            #purchase_order_line_data['purchase_order'] = purchase_order
            #PurchaseOrderLine.objects.create(**purchase_order_line_data)

        return purchase_order

    def update(self, instance, validated_data):
        print(validated_data)
        if validated_data.get('status') in [choice[0] for choice in PurchaseOrder.STATUS_CHOICES]:
            instance.status = validated_data.get('status', instance.status)
        purchase_order_lines_data = validated_data.get('purchaseorderline_set')

        services.delete_purchase_order_lines_not_present(instance.id, purchase_order_lines_data)

        for purchase_order_line_data in purchase_order_lines_data:
            print(purchase_order_line_data)
            purchase_order_line_id = purchase_order_line_data.get('id', None)
            if purchase_order_line_id:
                services.update_purchase_order_line(**purchase_order_line_data)
            else:
                purchase_order_line_data['purchase_order_id'] = instance.id
                services.create_purchase_order_line(**purchase_order_line_data)

        return instance


class ReceptionSerializer(serializers.HyperlinkedModelSerializer):
    #id = serializers.IntegerField(required=False)

    class Meta:
        model = Reception
        fields = ['id', 'purchase_order_line', 'batch', 'qty']
        read_only_fields = ['batch']

    def create(self, validated_data):
        reception = services.receive_purchase_order_line(**validated_data)

        return reception

    def update(self, instance, validated_data):
        #validated_data['id'] = instance.id
        validated_data.pop('purchase_order_line', None)
        reception = services.update_receive_purchase_order_line(instance, **validated_data)

        return reception


class InboundShipmentLineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = InboundShipmentLine
        fields = ['id', 'purchase_order_line', 'qty', 'qty_received']
        #read_only_fields = ['product']

    def get_qty_received(self, instance):
        return instance.qty_received


class InboundShipmentSerializer(serializers.HyperlinkedModelSerializer):
    inbound_shipment_lines = InboundShipmentLineSerializer(source='inboundshipmentline_set', many=True, read_only=False)

    class Meta:
        model = InboundShipment
        fields = ['id', 'reference', 'status', 'inbound_shipment_lines']

    def create(self, validated_data):
        inbound_shipment_lines_data = validated_data.pop('inboundshipmentline_set')
        inbound_shipment = services.create_inbound_shipment(**validated_data)

        for inbound_shipment_line_data in inbound_shipment_lines_data:
            inbound_shipment_line_data['inbound_shipment_id'] = inbound_shipment.id
            services.create_inbound_shipment_line(inbound_shipment_line_data)

        return inbound_shipment

    def update(self, instance, validated_data):
        if validated_data.get('status') in [choice[0] for choice in PurchaseOrder.STATUS_CHOICES]:
            instance.status = validated_data.get('status', instance.status)
        inbound_shipment_lines_data = validated_data.get('inboundshipmentline_set')

        services.delete_inbound_shipment_lines_not_present(instance.id, inbound_shipment_lines_data)

        for inbound_shipment_line_data in inbound_shipment_lines_data:
            print(inbound_shipment_line_data)
            inbound_shipment_line_id = inbound_shipment_line_data.get('id', None)
            if inbound_shipment_line_id:
                services.update_inbound_shipment_line(**inbound_shipment_line_data)
            else:
                inbound_shipment_line_data['inbound_shipment_id'] = instance.id
                services.create_inbound_shipment_line(**inbound_shipment_line_data)

        return instance

