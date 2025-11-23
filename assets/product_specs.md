# Product Specifications

## Product Catalog
- **Wireless Headphones**: Premium noise-cancelling headphones, priced at $100.00
- **Smart Watch**: Fitness tracker with heart rate monitor, priced at $250.00
- **Bluetooth Speaker**: Portable speaker with 360° sound, priced at $75.00
- All prices are in USD

## Shopping Cart Features
- Users can add multiple items to the cart
- Each cart item displays: product name, unit price, quantity input, subtotal, and remove button
- Quantity can be adjusted using number input (minimum 1)
- Cart displays total amount including discounts and shipping
- Empty cart shows message "Your cart is empty"

## Shipping Methods
- **Standard Shipping**: Free of charge (default option)
- **Express Shipping**: Additional $10.00 charge
- Shipping cost is added to the final total

## Payment Methods
- **Credit Card**: Requires card number validation (default option)
- **PayPal**: Alternative payment method (no additional validation in this version)

## Discount Codes
- Code "SAVE15" grants a 15% discount on subtotal
- Code "SAVE20" grants a 20% discount on subtotal
- Code "FREESHIP" is valid but applies no discount (reserved for future shipping discount feature)
- Any other code is considered invalid
- Discount is applied before shipping cost

## Form Validation Rules
- **Full Name**: Required, minimum 2 characters
- **Email Address**: Required, must contain "@" and "."
- **Shipping Address**: Required, minimum 5 characters
- **Card Number**: Required, must be at least 16 digits
- All validation errors display in red text below the respective field
- Cart must not be empty to proceed with checkout

## Checkout Flow
1. User adds products to cart from product catalog
2. User can adjust quantities or remove items
3. User selects shipping method (Standard or Express)
4. User enters customer information (Name, Email, Address)
5. User selects payment method (Credit Card or PayPal)
6. User enters card details
7. User optionally applies discount code
8. User clicks "Pay Now" button
9. Form validates all inputs
10. If valid, success message displays: "Payment Successful! Order confirmed."
