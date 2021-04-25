# inventory-system

This project is a simple inventory system in the form of a REST API. It is built using the Django Rest Framework and is for educational purposes only.

Click [here](https://tomqle.github.io/inventory-system/) to view the API documentation.

## Resources
#### Users
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "url": "http://example.com/users/1/",
      "username": "admin",
      "email": "admin@example.com",
      "groups": []
    }
  ]
}
```
* GET /users returns a paginated list of Users
* POST /users Creates a new User
* GET /users/{id} Retreives a User by ID
* PUT /users/{id} Updates an existing User by ID
* DELETE /users/{id} Deletes a User by ID
#### Products
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "sku": "MOUSE-WL",
      "name": "Wireless USB Mouse",
      "status": "Private",
      "qty": 3,
      "supplier": null
    }
  ]
}
```
* GET /products Returns a paginated list of Products
* POST /products Creates a new Product
* GET /products/{id} Retreives a Product by ID
* PUT /products/{id} Updates an existing Product by ID
* DELETE /products/{id} Deletes a Product by ID
#### Purchase Orders
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "reference": "PO-1",
      "status": "DRF",
      "purchase_order_lines": [
        {
          "id": 1,
          "product": "http://example.com/products/1/",
          "sku": "",
          "qty": 7,
          "cost": 5,
          "subtotal": 35,
          "received_qty": 3,
          "incoming_qty": 4
        },
      ]
      "supplier": null
    }
  ]
}
```
* GET /purchase_orders Returns a paginated list of Purchase Orders
* POST /purchase_orders Creates a new Purchase Order
* GET /purchase_orders/{id} Retreives a Purchase Order by ID
* PUT /purchase_orders/{id} Updates an existing Purchase Order by ID
* DELETE /purchase_orders/{id} Deletes a Purchase Order by ID
#### Purchase Order Lines
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "product": "http://example.com/products/1/",
      "sku": "PRODUCT-1",
      "qty": 7,
      "cost": 5,
      "subtotal": 35,
      "received_qty": 3,
      "incoming_qty": 4
    }
  ]
}
```
* GET /purchase_order_lines Returns a paginated list of Purchase Order Lines
* POST /purchase_order_lines Creates a new Purchase Order Line
* GET /purchase_order_lines/{id} Retreives a Purchase Order Line by ID
* PUT /purchase_order_lines/{id} Updates an existing Purchase Order Line by ID
* DELETE /purchase_order_lines/{id} Deletes a Purchase Order Line by ID
#### Receptions
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "purchase_order_line": "http://example.com/purchase_order_lines/1/",
      "batch": "http://example.com/batches/4/",
      "qty": 2
    }
  ]
}
```
* GET /receptions Returns a paginated list of Receptions
* POST /receptions Creates a new Reception
* GET /receptions/{id} Retreives a Reception by ID
* PUT /receptions/{id} Updates an existing Reception by ID
* DELETE /receptions/{id} Deletes a Reception by ID
#### Batches
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "reference": "BATCH-1",
      "product": null,
      "sku": "SKU-1",
      "eta": null,
      "order_lines": [
        "http://example.com/order_lines/1/"
      ],
      "qty": 20,
      "allocated_qty": 5,
      "available_qty": 15
    }
  ]
}
```
* GET /batches Returns a paginated list of Batches
* POST /batches Creates a new Batch
* GET /batches/{id} Retreives a Batch by ID
* PUT /batches/{id} Updates an existing Batch by ID
* DELETE /batches/{id} Deletes a Batch by ID
#### Allocations
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "batch": "http://example.com/batches/1/",
      "order_line": "http://example.com/order_lines/1/",
      "qty": 5
    }
  ]
}
```
* GET /allocations Returns a paginated list of Batches
* POST /allocations Creates a new Batch
* GET /allocations/{id} Retreives a Batch by ID
* PUT /allocations/{id} Updates an existing Batch by ID
* DELETE /allocations/{id} Deletes a Batch by ID
#### Sales Orders
```
{
  "count" 0,
  "next": null,
  "previous": null,
  "results": []
}
```
* GET /sales_orders Returns a paginated list of Sales Orders
* POST /sales_orders Creates a new Sales Order
* GET /sales_orders/{id} Retreives a Sales Order by ID
* PUT /sales_orders/{id} Updates an existing Sales Order by ID
* DELETE /sales_orders/{id} Deletes a Sales Order by ID
#### Sales Order Lines
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "order_ref": "ORDER-1",
      "product": http://example.com/products/1,
      "sku": "SKU-1",
      "qty": 5,
      "allocated_qty": 5,
      "unallocated_qty": 0,
      "allocated": true,
      "cost": 1.0,
      "price": 2.0
    },
  ]
}
```
* GET /sales_order_lines Returns a paginated list of Sales Order Lines
* POST /sales_order_lines Creates a new Sales Order Line
* GET /sales_order_lines/{id} Retreives a Sales Order Line by ID
* PUT /sales_order_lines/{id} Updates an existing Sales Order Line by ID
* DELETE /sales_order_lines/{id} Deletes a Sales Order Line by ID
#### Suppliers
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "status": "ACT",
      "company": "Bland Co.",
      "name": "Bill Bland",
      "email": "bill@blandco.com",
      "phone": "800-222-2222",
      "payment_terms": "Consignment",
      "address": {
        "id": 3,
        "address1": "8921 Enterprise Drive",
        "address2": "Suite A",
        "city": "Charlotte",
        "state": "NC",
        "country": "US",
        "postal_code": "28105"
      }
    }
  ]
}
```
* GET /suppliers Returns a paginated list of Suppliers
* POST /suppliers Creates a new Supplier
* GET /suppliers/{id} Retreives a Supplier by ID
* PUT /suppliers/{id} Updates an existing Supplier by ID
* DELETE /suppliers/{id} Deletes a Supplier by ID
#### Customers
```
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 4,
      "status": "ACT",
      "company": "Prism Tech",
      "name": "John Hammer",
      "email": "john.hammer@prismtech.com",
      "phone": "800-100-1000",
      "payment_terms": "NET30",
      "address": {
        "id": 2,
        "address1": "567 Eagle Lane",
        "address2": "",
        "city": "Glendale",
        "state": "AZ",
        "country": "US",
        "postal_code": "85031"
      }
    }
  ]
}
```
* GET /customers Returns a paginated list of Customers
* POST /customers Creates a new Customer
* GET /customers/{id} Retreives a Customer by ID
* PUT /customers/{id} Updates an existing Customer by ID
* DELETE /customers/{id} Deletes a Customer by ID

### Todos:
- [ ] Build an admin front-end that will consume this API and provide a simple user interface to access the inventory system
- [ ] Build a shopping front-end that will allow customers to register and place orders that enter the inventory system as a sales order
- [ ] Build integrations with ecommerce platforms, online marketplaces, shipping providers and accounting software
