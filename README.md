# inventory-system

This project is a simple inventory system in the form of a REST API. It is built using the Django Rest Framework and is for educational purposes only.

Click [here](https://tomqle.github.io/inventory-system/) to view the API documentation.

### Resources:
* Purchase Orders
  * GET /purchase_orders Returns a list of Purchase Orders
  * POST /purchase_orders Creates a new Purchase Order
  * GET /purchase_orders/{id} Retreives Purchase Order by ID
  * PUT /purchase_orders/{id} Updates an existing Purchase Order by ID
  * DELETE /purchase_orders/{id} Deletes a Purchase Order by ID
* Purchase Order Lines
* Products
* Receptions
* Batches
* Allocations
* Sales Orders
* Sales Order Lines

### Todos:
- [ ] Build an admin front-end that will consume this API and provide a simple user interface to access the inventory system
- [ ] Build a shopping front-end that will allow customers to register and place orders that enter the inventory system as a sales order
- [ ] Build integrations with ecommerce platforms, online marketplaces, shipping providers and accounting software
