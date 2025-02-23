import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Hide the default menu and footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none;}
        .css-eh5xgm {visibility: hidden;}
        .css-1dp5vir {visibility: hidden;}
        .css-1d391kg {padding-top: 0;}
    </style>
""", unsafe_allow_html=True)

def show_order_confirmation():
    if 'last_order' not in st.session_state:
        st.error("No order found!")
        if st.button("← Return to Products"):
            st.switch_page("pages/products.py")
        return
    
    order = st.session_state.last_order
    
    # Show order confirmation
    st.title("🎉 Order Confirmed!")
    st.markdown(f"""
    ### Order #{order['order_id']}
    **Date:** {order['date']}
    
    ### Customer Information
    **Name:** {order['customer_name']}  
    **Phone:** {order['customer_phone']}  
    **Address:** {order['customer_address']}
    """)
    
    # Show ordered items
    st.markdown("### Ordered Items")
    for item in order['items']:
        st.markdown(f"""
        - **{item['name']}**  
          Size: {item.get('size', 'N/A')}  
          Quantity: {item.get('quantity', 1)}  
          Price: Rs. {item['price']}  
          Subtotal: Rs. {item['price'] * item.get('quantity', 1)}
        """)
    
    st.markdown(f"### Total Amount: Rs. {order['total_amount']}")
    
    # Add download button for existing Excel file
    try:
        with open(order['excel_path'], 'rb') as file:
            excel_bytes = file.read()
            st.download_button(
                label="📥 Download Invoice",
                data=excel_bytes,
                file_name=f"order_{order['order_id']}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                key="download_invoice_button"
            )
    except Exception as e:
        st.error(f"Error loading invoice: {str(e)}")
    
    # Continue shopping button
    if st.button("← Continue Shopping", type="primary"):
        # Clear last order from session
        del st.session_state.last_order
        st.switch_page("pages/products.py")

# Show order confirmation when page loads
show_order_confirmation() 