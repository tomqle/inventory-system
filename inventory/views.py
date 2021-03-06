from django.contrib.auth.models import Group, User
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from inventory import services
from inventory import serializers
from inventory.models import Address, Allocation, Batch, Customer, InboundShipment, InboundShipmentLine, SalesOrder, SalesOrderLine, Product, PurchaseOrder, PurchaseOrderLine, Reception, Supplier
from inventory.serializers import GroupSerializer, UserSerializer, AddressSerializer, AllocationSerializer, BatchSerializer, CustomerSerializer, InboundShipmentSerializer, InboundShipmentLineSerializer, SalesOrderSerializer, SalesOrderLineSerializer, ProductSerializer, PurchaseOrderSerializer, PurchaseOrderLineSerializer, ReceptionSerializer, SupplierSerializer


class UserViewSet(viewsets.ModelViewSet):
    # API endpoint that allows users to be viewed or edited
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    # API endpoint that allows groups to be viewed or edited
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class AllocationViewSet(viewsets.ModelViewSet):
    queryset = Allocation.objects.all()
    serializer_class = AllocationSerializer
    permissions = [permissions.IsAuthenticated]


class BatchViewSet(viewsets.ModelViewSet):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    permission_classes = [permissions.IsAuthenticated]


class SalesOrderViewSet(viewsets.ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


class SalesOrderLineViewSet(viewsets.ModelViewSet):
    queryset = SalesOrderLine.objects.all()
    serializer_class = SalesOrderLineSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        #request.data['reference'] = request.data['reference'].upper()
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        reference = ''
        if 'reference' in self.request.data:
            reference = self.request.data['reference']

        serializer.save(reference=reference)

    #def update(self, request, pk=None):
        #pass


class PurchaseOrderLineViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrderLine.objects.all()
    serializer_class = PurchaseOrderLineSerializer
    permission_classes = [permissions.IsAuthenticated]


class ReceptionViewSet(viewsets.ModelViewSet):
    queryset = Reception.objects.all()
    serializer_class = ReceptionSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]


class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permissions_classes = [permissions.IsAuthenticated]


class InboundShipmentViewSet(viewsets.ModelViewSet):
    queryset = InboundShipment.objects.all()
    serializer_class = InboundShipmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        #request.data['reference'] = request.data['reference'].upper()
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        reference = ''
        if 'reference' in self.request.data:
            reference = self.request.data['reference']

        serializer.save(reference=reference)

class InboundShipmentLineViewSet(viewsets.ModelViewSet):
    queryset = InboundShipmentLine.objects.all()
    serializer_class = InboundShipmentLineSerializer
    permission_classes = [permissions.IsAuthenticated]

@csrf_exempt
def allocate(request, pk):
    if request.method == 'POST':
        pass

