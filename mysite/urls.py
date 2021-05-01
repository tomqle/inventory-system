"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from inventory import views


router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'allocations', views.AllocationViewSet)
router.register(r'batches', views.BatchViewSet)
router.register(r'sales_orders', views.SalesOrderViewSet)
router.register(r'sales_order_lines', views.SalesOrderLineViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'purchase_orders', views.PurchaseOrderViewSet)
router.register(r'purchase_order_lines', views.PurchaseOrderLineViewSet)
router.register(r'receptions', views.ReceptionViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'suppliers', views.SupplierViewSet)
#router.register(r'inbound_shipments', views.InboundShipmentViewSet)
#router.register(r'inbound_shipment_lines', views.InboundShipmentLineViewSet)

purchase_order_list = views.PurchaseOrderViewSet.as_view({
    'get': 'list',
    'post': 'create',
})

# Wire up our API using automatic URL routing
# Additionally, we include login URLs for the browsable API
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #path('purchase_orders/', purchase_order_list, name='purchase-order-list'),
]
