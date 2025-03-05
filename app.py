import streamlit as st
from picchange import img_cryptography
from stegnography import steganography_function
from watermark import watermark_
from home import home_

# Set the page configuration at the very top of the script

# Sidebar Title
st.sidebar.title("ImageSecure Suite")
st.sidebar.write("Choose a feature to proceed:")

# Add a selectbox in the sidebar for selecting the functionality
feature_choice = st.sidebar.selectbox(
    "Select the functionality:",
    ("Home", "Cryptography", "Steganography", "Watermarking")
)

# Main App Title
st.title("ImageSecure Suite: Your Ultimate Image Security Solution.")

# Trigger the corresponding function based on the selected option
if feature_choice == "Home":
    home_()
elif feature_choice == "Cryptography":
    img_cryptography()
elif feature_choice == "Steganography":
    steganography_function()
else:
    watermark_()
