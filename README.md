# inventory-system

This project is a simple inventory system in the form of a REST API. It is built using the Django Rest Framework and is for educational purposes only.

Click [here](https://tomqle.github.io/inventory-system/) to view the API documentation.

## Resources:
#### Users
* GET /users returns a list of Users
* POST /users Creates a new User
* GET /users/{id} Retreives a User by ID
* PUT /users/{id} Updates an existing User by ID
* DELETE /users/{id} Deletes a User by ID
#### Products
* GET /products Returns a list of Products
* POST /products Creates a new Product
* GET /products/{id} Retreives a Product by ID
* PUT /products/{id} Updates an existing Product by ID
* DELETE /products/{id} Deletes a Product by ID
#### Purchase Orders
* GET /purchase_orders Returns a list of Purchase Orders
* POST /purchase_orders Creates a new Purchase Order
* GET /purchase_orders/{id} Retreives a Purchase Order by ID
* PUT /purchase_orders/{id} Updates an existing Purchase Order by ID
* DELETE /purchase_orders/{id} Deletes a Purchase Order by ID
#### Purchase Order Lines
* GET /purchase_order_lines Returns a list of Purchase Order Lines
* POST /purchase_order_lines Creates a new Purchase Order Line
* GET /purchase_order_lines/{id} Retreives a Purchase Order Line by ID
* PUT /purchase_order_lines/{id} Updates an existing Purchase Order Line by ID
* DELETE /purchase_order_lines/{id} Deletes a Purchase Order Line by ID
#### Receptions
* GET /receptions Returns a list of Receptions
* POST /receptions Creates a new Reception
* GET /receptions/{id} Retreives a Reception by ID
* PUT /receptions/{id} Updates an existing Reception by ID
* DELETE /receptions/{id} Deletes a Reception by ID
#### Batches
* GET /batches Returns a list of Batches
* POST /batches Creates a new Batch
* GET /batches/{id} Retreives a Batch by ID
* PUT /batches/{id} Updates an existing Batch by ID
* DELETE /batches/{id} Deletes a Batch by ID
#### Allocations
* GET /allocations Returns a list of Batches
* POST /allocations Creates a new Batch
* GET /allocations/{id} Retreives a Batch by ID
* PUT /allocations/{id} Updates an existing Batch by ID
* DELETE /allocations/{id} Deletes a Batch by ID
#### Sales Orders
* GET /sales_orders Returns a list of Sales Orders
* POST /sales_orders Creates a new Sales Order
* GET /sales_orders/{id} Retreives a Sales Order by ID
* PUT /sales_orders/{id} Updates an existing Sales Order by ID
* DELETE /sales_orders/{id} Deletes a Sales Order by ID
#### Sales Order Lines
* GET /sales_order_lines Returns a list of Sales Order Lines
* POST /sales_order_lines Creates a new Sales Order Line
* GET /sales_order_lines/{id} Retreives a Sales Order Line by ID
* PUT /sales_order_lines/{id} Updates an existing Sales Order Line by ID
* DELETE /sales_order_lines/{id} Deletes a Sales Order Line by ID
#### Suppliers
* GET /suppliers Returns a list of Suppliers
* POST /suppliers Creates a new Supplier
* GET /suppliers/{id} Retreives a Supplier by ID
* PUT /suppliers/{id} Updates an existing Supplier by ID
* DELETE /suppliers/{id} Deletes a Supplier by ID
#### Customers
* GET /customers Returns a list of Customers
* POST /customers Creates a new Customer
* GET /customers/{id} Retreives a Customer by ID
* PUT /customers/{id} Updates an existing Customer by ID
* DELETE /customers/{id} Deletes a Customer by ID

### Todos:
- [ ] Build an admin front-end that will consume this API and provide a simple user interface to access the inventory system
- [ ] Build a shopping front-end that will allow customers to register and place orders that enter the inventory system as a sales order
- [ ] Build integrations with ecommerce platforms, online marketplaces, shipping providers and accounting software
