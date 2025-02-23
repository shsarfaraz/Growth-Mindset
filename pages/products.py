import streamlit as st
import json

# Initialize session state if not already initialized
if 'cart' not in st.session_state:
    st.session_state.cart = []

def view_cart():
    st.switch_page("pages/cart.py")

# Updated CSS with more colors and beautiful design
st.markdown("""
    <style>
    /* Page background */
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #e3eeff 100%);
        padding: 1rem;
    }
    
    /* Product card styling */
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e1e8f0;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.15);
    }
    
    /* Image styling */
    .stImage {
        max-width: 200px !important;
        margin: 0 auto !important;
        display: block !important;
        border-radius: 10px;
        padding: 10px;
        background: #f8f9fa;
    }
    
    .stImage > img {
        max-height: 250px !important;
        object-fit: contain !important;
        transition: transform 0.3s ease;
    }
    
    .stImage > img:hover {
        transform: scale(1.05);
    }
    
    /* Product details styling */
    .product-details {
        padding: 1rem 0;
    }
    
    .product-title {
        color: #2c3e50;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .product-description {
        color: #666;
        font-size: 1rem;
        line-height: 1.5;
        margin-bottom: 1rem;
    }
    
    .price-tag {
        background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 25px;
        font-size: 1.1rem;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem 0;
    }
    
    /* Size selector styling */
    .stSelectbox {
        margin: 1rem 0;
    }
    
    .stSelectbox > div > div {
        background: #f8f9fa;
        border-radius: 8px;
        border: 2px solid #e9ecef;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.5rem 2rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 15px rgba(52, 152, 219, 0.4) !important;
    }
    
    /* Success message styling */
    .stSuccess {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%) !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        animation: slideIn 0.5s ease-out !important;
    }
    
    @keyframes slideIn {
        from {
            transform: translateY(-10px);
            opacity: 0;
        }
        to {
            transform: translateY(0);
            opacity: 1;
        }
    }
    
    /* Responsive design */
    @media (max-width: 768px) {
        .product-card {
            padding: 1rem;
        }
        .stImage {
            max-width: 150px !important;
        }
        .stImage > img {
            max-height: 200px !important;
        }
        .product-title {
            font-size: 1.2rem;
        }
    }
    </style>
""", unsafe_allow_html=True)

def show_products():
    # Calculate cart count
    cart_count = len(st.session_state.cart) if 'cart' in st.session_state else 0

    # Page title
    st.markdown("""
        <h1 style='text-align: center; color: #2c3e50; margin-bottom: 2rem; 
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);'>
        🛍️ Our Premium T-Shirts Collection
        </h1>
    """, unsafe_allow_html=True)
    
    # Add cart summary to sidebar
    if cart_count > 0:
        with st.sidebar:
            total = sum(item['price'] * item.get('quantity', 1) for item in st.session_state.cart)
            st.markdown(f"""
                <div class="cart-summary">
                    <strong>🛒 Cart Summary</strong><br>
                    Items: {cart_count}<br>
                    Total: Rs. {total}<br>
                    <br>
                </div>
            """, unsafe_allow_html=True)
            
            if st.button("🛒 Checkout", key="sidebar_cart"):
                view_cart()
    
    # Load products data
    with open('data/products.json', 'r', encoding='utf-8') as f:
        products_data = json.load(f)
    
    # Display products in a grid
    for product in products_data['products']:
        with st.container():
            st.markdown('<div class="product-card">', unsafe_allow_html=True)
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image(product['image'], use_container_width=True)
            
            with col2:
                st.markdown(f"""
                    <div class="product-details">
                        <h2 class="product-title">{product['name']}</h2>
                        <p class="product-description">{product['description']}</p>
                        <div class="price-tag">Rs. {product['price']}</div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown('<p style="color: #666; margin-bottom: 0.5rem;">Select Your Size:</p>', 
                          unsafe_allow_html=True)
                size = st.selectbox('', product['sizes'], key=f"size_{product['id']}")
                
                if st.button('🛒 Add to Cart', key=f"add_{product['id']}"):
                    if 'cart' not in st.session_state:
                        st.session_state.cart = []
                    
                    cart_item = {
                        'id': product['id'],
                        'name': product['name'],
                        'price': product['price'],
                        'size': size,
                        'quantity': 1
                    }
                    st.session_state.cart.append(cart_item)
                    st.success("✨ Successfully added to cart!")
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    show_products() 