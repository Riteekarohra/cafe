import streamlit as st
import json
import os

class CafeApp:
    def __init__(self):
        self.menu = {
            "pizza": {"small": 2000, "medium": 3000, "large": 4000},
            "pasta": 3000, "coffee": 2500, "cookies": 1500,
            "fries": 1500, "softie": 2500, "choco lava cake": 4500
        }
        self.order_items = []
        self.total_order = 0
        self.order_completed = False
        self.order_file_path = os.path.join(os.getcwd(), "order_details.json")
        self.revenue = 0

    def save_order_to_file(self):
        with open(self.order_file_path, "w") as file:
            json.dump({
                "total_order": self.total_order,
                "order_items": self.order_items,
                "order_completed": self.order_completed
            }, file)
    
    def read_order_from_file(self):
        try:
            with open(self.order_file_path, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return None

    def apply_discount(self):
        if self.total_order >= 5000:
            discount = self.total_order * 0.40
            discounted_price = self.total_order - discount
            st.markdown(f"<h3 style='color: crimson;'>You have received a 40% discount!</h3>", unsafe_allow_html=True)
            return discounted_price
        return self.total_order

    def display_welcome_message(self):
        """Improved Welcome Message"""
        st.markdown(
            """
            <div style="background-color: #f4f4f4; padding: 20px; border-radius: 20px; box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);">
                <h1 style="color: #4A90E2; text-align: center; font-family: 'Arial', sans-serif;">Welcome to Riteeka's Cafe</h1>
                <p style="color: #5D3F6A; font-size: 18px; text-align: center; font-family: 'Arial', sans-serif;">Hi there! We're thrilled to serve you today. Check out our delicious menu.</p>
                <h3 style="color: #D94C5C; text-align: center; font-size: 22px;">Get 40% OFF on orders above ₨3000!</h3>
            </div>
            """, unsafe_allow_html=True)

    def reset_order(self):
        self.order_items = []
        self.total_order = 0
        self.order_completed = False
        if os.path.exists(self.order_file_path):
            os.remove(self.order_file_path)

    def start_new_order(self):
        self.reset_order()
        st.write("New order started! Please select your items from the menu.")

    def process_order(self):
        """Improved Order Selection Process"""
        menu_items = [
            ("pizza", ["Small", "Medium", "Large"], ["Margherita", "Pepperoni", "Veg Supreme", "BBQ Chicken"]),
            ("pasta", [], ["white Sauce", "Red sauce"]),
            ("coffee", [], ["Espresso", "Cappuccino", "Latte"]),
            ("cookies", [], []), ("fries", [], []), ("softie", [], []), ("choco lava cake", [], [])
        ]
        for item, sizes, flavors in menu_items:
            col1, col2 = st.columns(2)
            with col1:
                if item == "pizza":
                    pizza_size = st.selectbox(f"Choose your pizza size ({item.capitalize()})", sizes, index=1)
                    pizza_flavor = st.selectbox(f"Choose your pizza flavor ({item.capitalize()})", flavors)
                    if st.button(f"Order {pizza_flavor} Pizza ({pizza_size})"):
                        self.total_order += self.menu["pizza"][pizza_size.lower()]
                        self.order_items.append(f"{pizza_flavor} Pizza ({pizza_size})")
                        self.save_order_to_file()  # Save the order immediately after adding an item
                else:
                    if st.button(f"Order {item.title()}"):
                        self.total_order += self.menu.get(item, 0)
                        self.order_items.append(item.title())
                        self.save_order_to_file()  # Save the order immediately after adding an item

    def finalize_order(self):
        """Finalizes and displays order with payment options and notification"""
        if self.total_order > 0:
            st.markdown(f"### Total Order: ₨{self.total_order}")
            for item in self.order_items:
                st.write(f"- {item}")
            final_total = self.apply_discount()
            st.write(f"### Final Total: ₨{final_total:.2f}")

            # Payment Method selection with modern style
            payment_method = st.selectbox("Select Payment Method", ["Cash", "Credit Card", "Debit Card", "UPI"])
            st.write(f"Selected Payment Method: {payment_method}")

            if st.button("Complete Order", use_container_width=True):
                self.order_completed = True
                self.revenue += final_total
                self.save_order_to_file()
                st.balloons()  # Show balloons when the order is completed
                st.markdown("<h3 style='color: yellow;'>Your order has been completed successfully! Thank you for ordering have a good day. </h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color: dodgerblue;'>Please select something to order before proceeding!</h3>", unsafe_allow_html=True)

    def view_order_history(self):
        """Displays a list of previous orders with styled information."""
        st.write("### Order History:")
        try:
            with open(self.order_file_path, "r") as file:
                prev_order = json.load(file)
                st.markdown(f"**Order Total:** ₨{prev_order['total_order']}")
                st.markdown(f"**Items Ordered:** {', '.join(prev_order['order_items'])}")
                st.markdown(f"**Payment Method:** {prev_order.get('payment_method', 'N/A')}")
                st.markdown(f"**Order Status:** {'Completed' if prev_order['order_completed'] else 'Pending'}")
        except FileNotFoundError:
            st.write("No previous orders found.")

    def admin_panel(self):
        """Admin Panel with stylish buttons and input fields."""
        st.write("### Admin Panel")
        admin_action = st.selectbox("Select Admin Action", ["View Revenue", "Add Item to Menu", "Remove Item from Menu"])
        
        if admin_action == "View Revenue":
            st.markdown(f"**Total Revenue:** ₨{self.revenue}")
        
        if admin_action == "Add Item to Menu":
            item_name = st.text_input("Enter item name:")
            item_price = st.number_input("Enter item price:", min_value=0)
            if st.button("Add Item", use_container_width=True):
                if item_name and item_price > 0:
                    self.menu[item_name.lower()] = item_price
                    st.write(f"Item '{item_name}' added to menu.")
        
        if admin_action == "Remove Item from Menu":
            item_name = st.selectbox("Select item to remove", list(self.menu.keys()))
            if st.button("Remove Item", use_container_width=True):
                del self.menu[item_name]
                st.write(f"Item '{item_name}' removed from menu.")
    
    def main(self):
        """Main function to control the flow of the app."""

        if 'snow_displayed' not in st.session_state:
            st.session_state['snow_displayed'] = False
        if not st.session_state['snow_displayed']:
            st.snow()
            st.session_state['snow_displayed'] = True

        if 'order_completed' not in st.session_state:
            st.session_state['order_completed'] = False

        user_type = st.selectbox("Select User Type", ["Customer", "Admin"])
        
        if user_type == "Admin":
            self.admin_panel()

        if user_type == "Customer":
            if st.button("Start a New Order"):
                self.start_new_order()

            if self.order_completed:
                st.markdown("<h3 style='color: limegreen;'>Your order has been completed successfully!</h3>", unsafe_allow_html=True)
                st.balloons()
            else:
                prev_order = self.read_order_from_file()
                if prev_order:
                    self.total_order = prev_order["total_order"]
                    self.order_items = prev_order["order_items"]
                    self.order_completed = prev_order["order_completed"]
                    st.markdown(f"### Welcome back! Your previous order total was ₨{self.total_order}.")
                self.display_welcome_message()
                self.process_order()
                self.finalize_order()

if __name__ == "__main__":
    app = CafeApp()
    app.main()