import streamlit as st

# Set up the page
def home_():
    
    st.title("Image Security Suite")
    st.write("#### The Image Secure Suite is an integrated system designed to ensure the confidentiality, authenticity, and integrity of digital images. This project focuses on advanced image security techniques, including encryption, steganography, and watermarking, to address critical challenges in digital media protection.")

    # Section 1: Image Encryption
    with st.container():
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image("Data-Encryption-Descryption-1024x631.jpg", use_column_width=True, caption="Image Encryption Illustration")

        with col2:
            st.subheader("Image Encryption & Decryption")
            st.write(
                """
                Image encryption is the process of converting an image into an unreadable format to protect its content from unauthorized access, using cryptographic techniques. Image decryption is the reverse process of restoring the encrypted image back to its original form, making it viewable and understandable again using the correct decryption key.
                """
            )

    # Section 2: Steganography
    with st.container():
        col1, col2 = st.columns([1, 1])

        with col1:
            st.subheader("Steganography")
            st.write(
                """
                Steganography is the practice of concealing a message or information within another medium, such as an image, audio, or text, in a way that prevents detection. The goal is to hide the existence of the message itself.
                """
            )

        with col2:
            st.image("steganography-malware-hidden-in-source-code.jpg", use_column_width=True, caption="Steganography Illustration")

    # Section 3: Watermarking
    with st.container():
        col1, col2 = st.columns([1, 1])

        with col1:
            st.image("images.jpg", use_column_width=True, caption="Watermarking Illlustration")

        with col2:
            st.subheader("Watermarking")
            st.write(
                """
                Watermarking is the process of embedding a visible or invisible mark or pattern into a digital file (such as an image, video, or document) to indicate ownership, authenticity, or to protect against unauthorized use.
                """
            )

if __name__ == "__main__":
    home_()
