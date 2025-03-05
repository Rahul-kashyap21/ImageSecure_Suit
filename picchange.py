import streamlit as st
from PIL import Image
import numpy as np
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from io import BytesIO
def img_cryptography():
    
    # Function to add padding to the image bytes
    def pad_data(data):
        try:
            padder = padding.PKCS7(128).padder()  # AES block size is 128 bits (16 bytes)
            padded_data = padder.update(data) + padder.finalize()
            return padded_data
        except Exception as e:
            raise ValueError(f"Padding Error: {e}")

    # Function to remove padding after decryption
    def unpad_data(data):
        try:
            unpadder = padding.PKCS7(128).unpadder()
            unpadded_data = unpadder.update(data) + unpadder.finalize()
            return unpadded_data
        except Exception as e:
            raise ValueError(f"Unpadding Error: {e}")

    # Function to encrypt image using AES with a user-provided key
    def encrypt_image(image_bytes, key):
        try:
            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            encryptor = cipher.encryptor()

            # Pad the image bytes before encryption
            padded_bytes = pad_data(image_bytes)
            encrypted_bytes = encryptor.update(padded_bytes) + encryptor.finalize()
            return encrypted_bytes
        except Exception as e:
            raise ValueError(f"Encryption Error: {e}")

    # Function to decrypt image using AES with a user-provided key
    def decrypt_image(encrypted_bytes, key):
        try:
            cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
            decryptor = cipher.decryptor()
            decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()

            # Remove padding after decryption
            unpadded_bytes = unpad_data(decrypted_bytes)
            return unpadded_bytes
        except ValueError as e:
            raise ValueError(f"Decryption Error: Invalid padding or incorrect key - {e}")
        except Exception as e:
            raise ValueError(f"Decryption Error: {e}")

    # Streamlit user interface
    st.header("Image Encryption and Decryption using AES")

    # Option for selecting key length
    key_length = st.selectbox("Choose AES key length:", [16, 24, 32])

    # Function to generate the AES key based on user input
    def generate_key(key_input, length):
        try:
            key = key_input.encode('utf-8')
            if len(key) < length:
                # Pad the key with null bytes if it's shorter than the selected length
                key = key.ljust(length, b'\0')
            elif len(key) > length:
                # Truncate the key if it's longer than the selected length
                key = key[:length]
            return key
        except Exception as e:
            raise ValueError(f"Key Generation Error: {e}")

    # Input for AES Key
    key_input = st.text_input(f"Enter AES encryption key (up to {key_length} characters):", type="password")

    # Ensure the key is of the correct length after processing
    if key_input and key_length:
        key = generate_key(key_input, key_length)
    else:
        st.warning(f"Please enter a key of length {key_length} characters for encryption and decryption.")
        key = None

    # Create two columns for encryption and decryption sections
    col1, col2 = st.tabs(["Encryption","Decryption"])

    # ENCRYPTION SECTION (Left Column)
    with col1:
        st.header("Encryption")

        # Option to upload image for encryption
        uploaded_file = st.file_uploader("Choose an image to encrypt...", type=["jpg", "jpeg", "png"])

        if uploaded_file is not None and key:
            # Display the original image
            image = Image.open(uploaded_file)
            st.image(image, caption=f"Original Image - Dimensions: {image.size[0]}x{image.size[1]}", use_column_width=True)
            if st.button("Encrypt"):
                # Convert image to bytes for encryption
                image_bytes = BytesIO()
                image.save(image_bytes, format="PNG")
                image_bytes = image_bytes.getvalue()

                # Encrypt the image bytes
                encrypted_bytes = encrypt_image(image_bytes, key)

                # Save the encrypted bytes as a .bin file
                encrypted_bin_file = "encrypted_image.bin"
                with open(encrypted_bin_file, "wb") as f:
                    f.write(encrypted_bytes)

                # To visualize encrypted data, truncate or pad it to match the original size
                # Use numpy to create a grayscale view of the encrypted data
                encrypted_array = np.frombuffer(encrypted_bytes, dtype=np.uint8)
                padded_array = np.zeros(image.size[0] * image.size[1], dtype=np.uint8)
                padded_array[:len(encrypted_array)] = encrypted_array[:len(padded_array)]

                # Reshape to match image dimensions and visualize as a grayscale image
                encrypted_image_array = padded_array.reshape(image.size[1], image.size[0])
                encrypted_image = Image.fromarray(encrypted_image_array, mode="L")
                encrypted_image_file = "encrypted_image.png"
                encrypted_image.save(encrypted_image_file, format="PNG")

                # Success message and download buttons
                st.success("Image Encrypted Successfully!")
                st.download_button(label="Download Encrypted BIN File", data=encrypted_bytes, file_name="encrypted_image.bin")
                st.download_button(label="Download Encrypted PNG File", data=open(encrypted_image_file, "rb").read(), file_name="encrypted_image.png")
                st.image(encrypted_image, caption="Encrypted Image (PNG)", use_column_width=True)


    # DECRYPTION SECTION (Right Column)
    with col2:
        st.header("Decryption")

        # Option to upload encrypted file for decryption (.bin only)
        encrypted_file = st.file_uploader("Upload an encrypted file to decrypt (.bin only)...", type=["bin"])

        if encrypted_file is not None and key:
            try:
                # Read encrypted binary data
                encrypted_bytes = encrypted_file.read()

                # Decrypt the image
                decrypted_bytes = decrypt_image(encrypted_bytes, key)

                # Convert decrypted bytes back to image
                decrypted_image = Image.open(BytesIO(decrypted_bytes))
                st.image(decrypted_image, caption="Decrypted Image", use_column_width=True)

                # Save decrypted image as JPG
                decrypted_image_file = "decrypted_image.jpg"
                decrypted_image.save(decrypted_image_file, format="JPEG")

                st.success("Image Decrypted Successfully!")
                st.download_button(label="Download Decrypted Image (JPG)", data=open(decrypted_image_file, "rb").read(), file_name="decrypted_image.jpg")

            except ValueError as e:
                st.error(f"Error in decryption: {e}. This may indicate mismatched padding or incorrect decryption keys.")
            except Exception as e:
                st.error(f"Unexpected error: {e}")

if __name__=="__main__":
    img_cryptography()
