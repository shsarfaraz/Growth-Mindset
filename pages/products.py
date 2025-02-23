import streamlit as st
import json
import os

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
    st.title("👕 Our Products")
    
    # Show cart summary in sidebar
    with st.sidebar:
        st.markdown("### 🛒 Cart Summary")
        cart_count = len(st.session_state.cart)
        total = sum(item['price'] * item.get('quantity', 1) for item in st.session_state.cart)
        
        st.markdown("""
            <style>
            .cart-summary {
                background-color: #f0f2f6;
                padding: 20px;
                border-radius: 10px;
                margin-bottom: 20px;
            }
            </style>
            """, unsafe_allow_html=True)
            
        st.markdown(f"""
            <div class="cart-summary">
                <p>Items in Cart: {cart_count}</p>
                <p>Total Amount: Rs. {total}</p>
            </div>
        """, unsafe_allow_html=True)
        
        if cart_count > 0:
            if st.button("View Cart 🛒", type="primary"):
                st.switch_page("pages/cart.py")
    
    try:
        # Load products data
        with open('data/products.json', 'r', encoding='utf-8') as f:
            products_data = json.load(f)
            
        # Display products in a grid
        for product in products_data['products']:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                image_path = product.get('image', '')
                try:
                    st.image(image_path)
                except Exception as e:
                    st.error(f"Error loading image: {image_path}")
                    st.error(str(e))
            
            with col2:
                st.markdown(f"### {product['name']}")
                st.markdown(f"**Price:** Rs. {product['price']}")
                st.markdown(f"**Description:** {product.get('description', 'No description available')}")
                
                sizes = product.get('sizes', ['S', 'M', 'L', 'XL'])
                selected_size = st.selectbox(
                    "Select Size",
                    sizes,
                    key=f"size_{product['name']}"
                )
                
                if st.button("Add to Cart", key=f"add_{product['name']}"):
                    add_to_cart(product, selected_size)
                    st.success(f"Added {product['name']} (Size: {selected_size}) to cart!")
                    st.rerun()
                    
    except Exception as e:
        st.error(f"Error loading products: {str(e)}")

def add_to_cart(product, selected_size):
    if 'cart' not in st.session_state:
        st.session_state.cart = []
    
    # Add product with size to cart
    cart_item = {
        'name': product['name'],
        'price': product['price'],
        'size': selected_size,  # Add size to cart item
        'quantity': 1
    }
    st.session_state.cart.append(cart_item)

if __name__ == "__main__":
    show_products() 