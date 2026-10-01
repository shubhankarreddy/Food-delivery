import streamlit as st

from food_delivery import Customer, DeliveryPartner, MenuItem, Restaurant


st.set_page_config(
    page_title="Food Delivery OOP",
    page_icon="🍔",
    layout="wide",
)


# -----------------------------
# Session state
# -----------------------------
if "customer" not in st.session_state:
    st.session_state.customer = None

if "delivery_partner" not in st.session_state:
    st.session_state.delivery_partner = None

if "restaurant" not in st.session_state:
    restaurant = Restaurant("Food Corner", "Aurangabad")

    restaurant.add_item(MenuItem("Veg Burger", 120, True))
    restaurant.add_item(MenuItem("Pizza", 250, True))
    restaurant.add_item(MenuItem("Paneer Wrap", 150, True))
    restaurant.add_item(MenuItem("Chicken Biryani", 220, False))
    restaurant.add_item(MenuItem("French Fries", 100, True))

    st.session_state.restaurant = restaurant

if "order" not in st.session_state:
    st.session_state.order = None


restaurant = st.session_state.restaurant


# -----------------------------
# Helper functions
# -----------------------------
def get_status():
    if st.session_state.order is None:
        return "No order placed"
    return st.session_state.order._status


# -----------------------------
# Header
# -----------------------------
st.title("🍔 Food Delivery System")
st.caption("Simple Streamlit interface for the OOP food delivery project")

st.divider()


# -----------------------------
# Customer section
# -----------------------------
st.header("1. Create Customer")

col1, col2, col3 = st.columns(3)

with col1:
    customer_name = st.text_input("Customer Name")

with col2:
    customer_phone = st.text_input("Phone")

with col3:
    customer_address = st.text_input("Address")

if st.button("Create Customer", type="primary"):
    if customer_name and customer_phone and customer_address:
        st.session_state.customer = Customer(
            customer_name,
            customer_phone,
            customer_address,
        )
        st.success(f"Customer '{customer_name}' created.")
    else:
        st.warning("Please enter name, phone and address.")

if st.session_state.customer:
    customer = st.session_state.customer
    st.info(
        f"Customer: {customer._name} | "
        f"Wallet: ₹{customer._wallet_balance:.2f}"
    )


st.divider()


# -----------------------------
# Wallet
# -----------------------------
st.header("2. Add Wallet Balance")

wallet_amount = st.number_input(
    "Amount",
    min_value=0.0,
    step=100.0,
)

if st.button("Add Money"):
    if st.session_state.customer is None:
        st.warning("Create a customer first.")
    elif wallet_amount <= 0:
        st.warning("Enter an amount greater than 0.")
    else:
        st.session_state.customer.add_to_wallet(wallet_amount)
        st.success(
            f"₹{wallet_amount:.2f} added to wallet."
        )

if st.session_state.customer:
    st.metric(
        "Current Wallet Balance",
        f"₹{st.session_state.customer._wallet_balance:.2f}",
    )


st.divider()


# -----------------------------
# Restaurant menu
# -----------------------------
st.header("3. Restaurant Menu")

st.write(
    f"**{restaurant.name}** — {restaurant.location}"
)

menu_data = []

for item in restaurant.get_menu():
    menu_data.append(
        {
            "Item": item.name,
            "Price": f"₹{item.price:.2f}",
            "Type": "Veg" if item.is_veg else "Non-Veg",
        }
    )

st.table(menu_data)


st.divider()


# -----------------------------
# Place order
# -----------------------------
st.header("4. Place Order")

item_names = [item.name for item in restaurant.get_menu()]

selected_items = st.multiselect(
    "Select food items",
    item_names,
)

if selected_items:
    selected_objects = [
        item
        for item in restaurant.get_menu()
        if item.name in selected_items
    ]

    subtotal = sum(item.price for item in selected_objects)
    gst = subtotal * 0.05
    packaging = 20
    total = subtotal + gst + packaging

    st.write(f"Subtotal: ₹{subtotal:.2f}")
    st.write(f"GST (5%): ₹{gst:.2f}")
    st.write(f"Packaging Fee: ₹{packaging:.2f}")
    st.write(f"**Total: ₹{total:.2f}**")

if st.button("Place Order", type="primary"):
    if st.session_state.customer is None:
        st.warning("Create a customer first.")
    elif not selected_items:
        st.warning("Select at least one food item.")
    else:
        selected_objects = [
            item
            for item in restaurant.get_menu()
            if item.name in selected_items
        ]

        order = st.session_state.customer.place_order(
            restaurant,
            selected_objects,
        )

        st.session_state.order = order

        st.success(
            f"Order #{order._order_id} placed successfully!"
        )
        st.warning(
            f"Delivery OTP: {order._otp} "
            "(shown here for project/demo purposes)"
        )


st.divider()


# -----------------------------
# Order status
# -----------------------------
st.header("5. Order Status")

if st.session_state.order:
    order = st.session_state.order

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric("Order ID", order._order_id)

    with c2:
        st.metric("Status", order._status)

    with c3:
        st.metric("Estimated Time", f"{order.estimated_time()} min")

    st.write(f"**Bill:** ₹{order.calculate_bill():.2f}")
else:
    st.info("No order has been placed yet.")


st.divider()


# -----------------------------
# Delivery partner
# -----------------------------
st.header("6. Create Delivery Partner")

col1, col2, col3 = st.columns(3)

with col1:
    partner_name = st.text_input("Partner Name")

with col2:
    partner_phone = st.text_input("Partner Phone")

with col3:
    vehicle = st.selectbox(
        "Vehicle",
        ["Bike", "Scooter", "Cycle"],
    )

if st.button("Create Delivery Partner"):
    if partner_name and partner_phone:
        st.session_state.delivery_partner = DeliveryPartner(
            partner_name,
            partner_phone,
            vehicle,
        )
        st.success(
            f"Delivery partner '{partner_name}' created."
        )
    else:
        st.warning("Enter partner name and phone.")

if st.session_state.delivery_partner:
    partner = st.session_state.delivery_partner

    st.info(
        f"Partner: {partner._name} | "
        f"Vehicle: {partner.vehicle} | "
        f"Available: {partner.is_available}"
    )


st.divider()


# -----------------------------
# Accept order
# -----------------------------
st.header("7. Accept Order")

if st.button("Accept Order"):
    if st.session_state.order is None:
        st.warning("Place an order first.")
    elif st.session_state.delivery_partner is None:
        st.warning("Create a delivery partner first.")
    elif not st.session_state.delivery_partner.is_available:
        st.warning("Delivery partner is already busy.")
    else:
        st.session_state.delivery_partner.accept_order(
            st.session_state.order
        )

        st.success("Order accepted by delivery partner.")


st.divider()


# -----------------------------
# OTP and delivery
# -----------------------------
st.header("8. Enter OTP & Complete Delivery")

otp = st.number_input(
    "Enter 4-digit OTP",
    min_value=1000,
    max_value=9999,
    step=1,
)

if st.button("Complete Delivery", type="primary"):
    if st.session_state.order is None:
        st.warning("No order available.")
    elif st.session_state.delivery_partner is None:
        st.warning("Create a delivery partner first.")
    elif st.session_state.order._status != "Order Accepted":
        st.warning("The order must be accepted before delivery.")
    else:
        success = st.session_state.delivery_partner.deliver(
            st.session_state.order,
            int(otp),
        )

        if success:
            st.success(
                f"Order #{st.session_state.order._order_id} "
                "delivered successfully! 🎉"
            )
        else:
            st.error("Invalid OTP. Delivery not completed.")


st.divider()


# -----------------------------
# Final summary
# -----------------------------
st.header("9. Delivery Summary")

if st.session_state.order:
    order = st.session_state.order

    st.write(f"**Order ID:** {order._order_id}")
    st.write(f"**Status:** {order._status}")
    st.write(f"**Total Bill:** ₹{order.calculate_bill():.2f}")

    if st.session_state.delivery_partner:
        partner = st.session_state.delivery_partner
        st.write(f"**Delivery Partner:** {partner._name}")
        st.write(f"**Vehicle:** {partner.vehicle}")
else:
    st.info("Complete the order flow to see the final summary.")
