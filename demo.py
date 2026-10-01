from food_delivery import Customer, DeliveryPartner, Restaurant, MenuItem


# 1. Register customer Priya
customer = Customer(
    "Priya",
    "9876543210",
    "Bangalore"
)

print("=== Customer Registered ===")
customer.display_profile()


# 2. Register delivery partner Rajesh
partner = DeliveryPartner(
    "Rajesh",
    "9999999999",
    "Bike"
)

print("\n=== Delivery Partner Registered ===")
partner.display_profile()


# 3. Create Bawarchi restaurant and add Biryani and Kebab
restaurant = Restaurant(
    "Bawarchi",
    "MG Road"
)

biryani = MenuItem(
    "Biryani",
    250,
    False
)

kebab = MenuItem(
    "Kebab",
    200,
    False
)

restaurant.add_item(biryani)
restaurant.add_item(kebab)

print("\n=== Restaurant Menu ===")
for item in restaurant.get_menu():
    food_type = "Veg" if item.is_veg else "Non-Veg"
    print(f"{item.name} - ₹{item.price} - {food_type}")


# 4. Top up Priya's wallet by 500
print("\n=== Wallet Top-up ===")

customer.add_to_wallet(500)
print(f"Wallet after ₹500 top-up: ₹{customer._wallet_balance}")

# Attempt to top up by -100
customer.add_to_wallet(-100)
print(f"Wallet after -₹100 top-up attempt: ₹{customer._wallet_balance}")


# 5. Priya places an order for Biryani and Kebab
print("\n=== Place Order ===")

order = customer.place_order(
    restaurant,
    [biryani, kebab]
)

print(f"Order ID: {order._order_id}")
print(f"Order Status: {order._status}")


# 6. Print subtotal, GST, packaging fee, total and estimated time
print("\n=== Order Bill ===")

subtotal = sum(item.price for item in order._items)
gst = subtotal * 0.05
packaging_fee = 20
total = order.calculate_bill()

print(f"Subtotal: ₹{subtotal:.2f}")
print(f"GST (5%): ₹{gst:.2f}")
print(f"Packaging Fee: ₹{packaging_fee:.2f}")
print(f"Total: ₹{total:.2f}")
print(f"Estimated Delivery Time: {order.estimated_time()} minutes")


# 7. Rajesh accepts the order, try wrong OTP, then use 1234
print("\n=== Delivery ===")

partner.accept_order(order)

print(f"Order Status after acceptance: {order._status}")

# Try wrong OTP
wrong_otp = 9999

print(f"Trying wrong OTP: {wrong_otp}")

if partner.deliver(order, wrong_otp):
    print("Delivery completed.")
else:
    print("Wrong OTP. Delivery not completed.")

print(f"Order Status: {order._status}")

# Demo requirement: use OTP 1234
# Since the generated OTP is random, set it to 1234 for this demo.
order._otp = 1234

print("Trying correct OTP: 1234")

if partner.deliver(order, 1234):
    print("Delivery completed successfully.")
else:
    print("Invalid OTP. Delivery not completed.")

print(f"Order Status: {order._status}")


# 8. Notify Priya and Rajesh
print("\n=== Notifications ===")

customer.notify("Order delivered")
partner.notify("Order delivered")
