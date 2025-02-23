import streamlit as st
import pandas as pd
from datetime import datetime
import os
import uuid

# Initialize session state for cart
if 'cart' not in st.session_state:
    st.session_state.cart = []

def save_to_excel(order_data):
    # Create DataFrame for order
    order_items = []
    for item in order_data['items']:
        order_items.append({
            'Order Date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'Customer Name': order_data['customer_details']['name'],
            'Phone': order_data['customer_details']['phone'],
            'Address': order_data['customer_details']['address'],
            'Product': item['name'],
            'Size': item['size'],
            'Quantity': item.get('quantity', 1),
            'Price': item['price'],
            'Total': item['price'] * item.get('quantity', 1)
        })
    
    df = pd.DataFrame(order_items)
    
    # Create 'orders' directory if it doesn't exist
    if not os.path.exists('orders'):
        os.makedirs('orders')
    
    # Save to Excel
    file_path = f"orders/orders_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    if os.path.exists(file_path):
        # If file exists, read it and append new data
        existing_df = pd.read_excel(file_path)
        df = pd.concat([existing_df, df], ignore_index=True)
    
    df.to_excel(file_path, index=False)
    return file_path

def place_order():
    if not st.session_state.cart:
        st.error("Your cart is empty!")
        return False
    
    # Customer Information Form
    st.markdown("### 📋 Customer Information")
    customer_name = st.text_input("Full Name", key="customer_name_input")
    customer_phone = st.text_input("Phone Number", key="customer_phone_input")
    customer_address = st.text_area("Delivery Address", key="customer_address_input")
    
    # Calculate total before placing order
    total_amount = sum(item['price'] * item.get('quantity', 1) for item in st.session_state.cart)
    st.markdown(f"### Total Amount: Rs. {total_amount}")
    
    # Add Place Order button with unique key
    if st.button("Place Order", type="primary", key="place_order_button"):
        if not all([customer_name, customer_phone, customer_address]):
            st.warning("Please fill all customer information to place order.")
            return False
            
        try:
            # Generate unique order ID and timestamp
            order_id = str(uuid.uuid4())[:8]
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Create order data
            excel_data = []
            for item in st.session_state.cart:
                excel_data.append({
                    'Order ID': order_id,
                    'Date': current_date,
                    'Customer Name': customer_name,
                    'Phone Number': customer_phone,
                    'Delivery Address': customer_address,
                    'Product Name': item['name'],
                    'Size': item.get('size', 'N/A'),
                    'Quantity': item.get('quantity', 1),
                    'Price': item['price'],
                    'Subtotal': item['price'] * item.get('quantity', 1),
                    'Total Amount': total_amount
                })
            
            # Create DataFrame
            df_order = pd.DataFrame(excel_data)
            
            # Ensure orders directory exists
            os.makedirs('orders', exist_ok=True)
            
            # Save to Excel
            filename = f"order_{order_id}.xlsx"
            filepath = os.path.join('orders', filename)
            df_order.to_excel(filepath, index=False)
            
            # Save order details in session state
            st.session_state.last_order = {
                'order_id': order_id,
                'date': current_date,
                'customer_name': customer_name,
                'customer_phone': customer_phone,
                'customer_address': customer_address,
                'items': st.session_state.cart.copy(),
                'total_amount': total_amount,
                'excel_path': filepath  # Save Excel file path
            }
            
            # Clear the cart
            st.session_state.cart = []
            
            # Redirect to order confirmation page
            st.switch_page("pages/order.py")
            
            return True
            
        except Exception as e:
            st.error(f"Error placing order: {str(e)}")
            st.error("Please try again or contact support.")
            return False
    
    return False

def show_cart():
    st.title("🛒 Your Shopping Cart")
    
    # Add Continue Shopping button
    if st.button("← Continue Shopping", type="secondary", key="continue_shopping_button"):
        st.switch_page("pages/products.py")
    
    if not st.session_state.cart:
        st.info("Your cart is empty. Start shopping!")
        return
    
    # Display cart items
    for i, item in enumerate(st.session_state.cart):
        col1, col2, col3, col4, col5, col6 = st.columns([2, 1, 1, 1, 1, 1])
        
        with col1:
            st.write(f"**{item['name']}**")
        with col2:
            st.write(f"Size: {item.get('size', 'N/A')}")
        with col3:
            st.write(f"Rs. {item['price']}")
        with col4:
            if st.button("➕", key=f"plus_button_{i}"):
                item['quantity'] = item.get('quantity', 1) + 1
                st.rerun()
            
            st.write(f"{item.get('quantity', 1)}")
            
            if st.button("➖", key=f"minus_button_{i}"):
                if item.get('quantity', 1) > 1:
                    item['quantity'] = item.get('quantity', 1) - 1
                    st.rerun()
        with col5:
            st.write(f"Rs. {item['price'] * item.get('quantity', 1)}")
        with col6:
            if st.button("🗑️", key=f"remove_button_{i}"):
                st.session_state.cart.pop(i)
                st.rerun()
    
    # Show place order form
    st.markdown("---")
    place_order()

# Add a section for downloading all orders (for admin)
with st.sidebar:
    st.markdown("---")
    st.markdown("### 📊 Admin Section")
    if os.path.exists('data/orders.xlsx'):
        with open('data/orders.xlsx', 'rb') as file:
            all_orders_data = file.read()
        
        st.download_button(
            label="📥 Download All Orders",
            data=all_orders_data,
            file_name="all_orders.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

# Show cart when page loads
show_cart() 