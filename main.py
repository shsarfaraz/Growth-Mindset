import streamlit as st
import json
import pandas as pd
from datetime import datetime
from io import BytesIO

# Initialize session state
if 'cart' not in st.session_state:
    st.session_state.cart = []

# Configure page
st.set_page_config(
    page_title="T-Shirt Store",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Add custom CSS
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e3eeff 100%);
        padding: 2rem;
    }
    
    /* Hero section */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.5rem;
        opacity: 0.9;
        margin-bottom: 2rem;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        height: 100%;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .feature-title {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    .feature-description {
        color: #666;
        font-size: 1.1rem;
        line-height: 1.6;
    }
    
    /* CTA button */
    .cta-button {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5253 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 50px;
        font-size: 1.2rem;
        font-weight: bold;
        text-decoration: none;
        display: inline-block;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 15px rgba(238, 82, 83, 0.3);
    }
    
    .cta-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(238, 82, 83, 0.4);
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Hero Section with button instead of link
st.markdown("""
    <div class="hero-section">
        <div class="hero-title">👕 Welcome to T-Shirt Store</div>
        <div class="hero-subtitle">Discover Your Perfect Style</div>
    </div>
""", unsafe_allow_html=True)

# Shop Now button using Streamlit
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🛍️ Shop Now", type="primary", use_container_width=True):
        st.switch_page("pages/products.py")

# Features Section
st.markdown("<h2 style='text-align: center; color: #2c3e50; margin: 2rem 0;'>Why Choose Us?</h2>", unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">👕</div>
            <div class="feature-title">Premium Quality</div>
            <div class="feature-description">
                High-quality materials and expert craftsmanship ensure lasting comfort and style.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💰</div>
            <div class="feature-title">Best Prices</div>
            <div class="feature-description">
                Competitive prices without compromising on quality. Great value for your money.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🚚</div>
            <div class="feature-title">Fast Delivery</div>
            <div class="feature-description">
                Quick and reliable shipping to get your favorite t-shirts to you as soon as possible.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🎨</div>
            <div class="feature-title">Wide Selection</div>
            <div class="feature-description">
                Various styles, colors, and sizes to match your unique personality.
            </div>
        </div>
    """, unsafe_allow_html=True)

# Latest Collection Section with button
st.markdown("""
    <div style='text-align: center; margin: 4rem 0;'>
        <h2 style='color: #2c3e50; margin-bottom: 2rem;'>🌟 Latest Collection</h2>
        <p style='color: #666; font-size: 1.2rem; margin-bottom: 2rem;'>
            Explore our newest arrivals and trending designs. Find the perfect t-shirt that matches your style.
        </p>
    </div>
""", unsafe_allow_html=True)

# View Collection button using Streamlit
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if st.button("🎯 View Collection", type="primary", use_container_width=True):
        st.switch_page("pages/products.py")

# Contact Section
st.markdown("""
    <div style='background: #f8f9fa; padding: 3rem; border-radius: 20px; margin-top: 3rem; text-align: center;'>
        <h2 style='color: #2c3e50; margin-bottom: 1rem;'>📞 Need Help?</h2>
        <p style='color: #666; font-size: 1.1rem;'>
            Our customer support team is here to assist you. Contact us anytime!
        </p>
        <p style='color: #2c3e50; font-size: 1.2rem; font-weight: bold; margin-top: 1rem;'>
            📧 support@tshirtstore.com<br>
            📱 +92 300 1234567
        </p>
    </div>
""", unsafe_allow_html=True)

# Load products
with open('data/products.json', 'r', encoding='utf-8') as f:
    products_data = json.load(f)

st.title("🛍️ Welcome - T-Shirt Store")

st.write("""
### Our Features:
- Premium Quality T-shirts
- Affordable Prices
- Multiple Sizes and Colors
- Fast Delivery
""")

st.markdown("---")
st.write("👈 Please select 'Products' page from the sidebar to view our products")

def create_order_excel(order_details):
    # Create DataFrame for order
    df = pd.DataFrame({
        'Order ID': [order_details['order_id']],
        'Customer Name': [order_details['name']],
        'Email': [order_details['email']],
        'Phone': [order_details['phone']],
        'Products': [', '.join(order_details['products'])],
        'Total Amount': [order_details['total']],
        'Order Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    })
    
    # Create BytesIO object to store Excel file
    buffer = BytesIO()
    
    # Save DataFrame to Excel in memory
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    
    # Get the Excel data
    excel_data = buffer.getvalue()
    
    return excel_data, f"order_{order_details['order_id']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

# Add this where you handle order submission
if st.button("Place Order"):
    if st.session_state.cart:
        # Collect order details
        order_details = {
            'order_id': f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}",
            'name': st.session_state.get('customer_name', ''),
            'email': st.session_state.get('customer_email', ''),
            'phone': st.session_state.get('customer_phone', ''),
            'products': [item['name'] for item in st.session_state.cart],
            'total': sum(item['price'] * item.get('quantity', 1) for item in st.session_state.cart)
        }
        
        # Create Excel file in memory
        excel_data, file_name = create_order_excel(order_details)
        
        # Provide download button
        st.download_button(
            label="📥 Download Order Details",
            data=excel_data,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        
        st.success("✅ Order placed successfully!")
        st.session_state.cart = []  # Clear cart after order
    else:
        st.warning("Your cart is empty!") 