import streamlit as st
from PIL import Image
import numpy as np
import io
def steganography_function():
    # Steganography functions
    def encode_image(input_image, secret_message):
        """Encodes a secret message into an image."""
        img = Image.open(input_image)
        encoded = img.copy()
        width, height = img.size
        pixels = encoded.load()

        # Convert the message into binary and add a delimiter
        binary_message = ''.join(format(ord(char), '08b') for char in secret_message) + '1111111111111110'
        data_index = 0

        for y in range(height):
            for x in range(width):
                if data_index < len(binary_message):
                    pixel = list(pixels[x, y])
                    # Modify the LSB of each RGB value
                    for i in range(3):  # Process R, G, B channels
                        if data_index < len(binary_message):
                            pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                            data_index += 1
                    pixels[x, y] = tuple(pixel)

        output = io.BytesIO()
        encoded.save(output, format='PNG')
        output.seek(0)
        return output

    def decode_image(encoded_image):
        """Decodes a secret message from an image."""
        img = Image.open(encoded_image)
        width, height = img.size
        pixels = img.load()

        binary_message = ""
        for y in range(height):
            for x in range(width):
                pixel = pixels[x, y]
                for i in range(3):  # Process R, G, B channels
                    binary_message += str(pixel[i] & 1)

        # Split binary string into 8-bit chunks
        message = ""
        for i in range(0, len(binary_message), 8):
            byte = binary_message[i:i+8]
            if byte == '11111110':  # Stop at the delimiter
                break
            message += chr(int(byte, 2))

        return message
    
    def lsb_analysis(image):
        """
        Analyzes the Least Significant Bits (LSB) of the image pixels
        and checks for irregularities that might indicate hidden data.
        """
        img = Image.open(image)
        img = img.convert('RGB')  # Ensure RGB mode
        pixels = np.array(img)  # Convert image to numpy array

        if len(pixels.shape) != 3 or pixels.shape[2] != 3:
            raise ValueError("Unsupported image format. Please use RGB images.")

        height, width, _ = pixels.shape

        lsb_count = [0, 0]  # Count of 0s and 1s in the LSB
        lsb_distribution = []

            # Loop through each pixel and channel
        for y in range(height):
            for x in range(width):
                pixel = pixels[y, x]
                for channel in range(3):  # Process R, G, B channels
                    lsb = pixel[channel] & 1
                    lsb_count[lsb] += 1
                    lsb_distribution.append(lsb)

        total_lsb = sum(lsb_count)
        if total_lsb == 0:
            return None, None

            # Compute percentage distribution
        lsb_percentage = [count / total_lsb * 100 for count in lsb_count]
        return lsb_percentage, lsb_distribution    

    # Streamlit App
    st.header("Steganography Tool")
    st.subheader("Hide and retrieve secret messages in images")

    # Tabs for Encode and Decode
    tab1, tab2, tab3 = st.tabs(["🔒 Encode Message", "🔓 Decode Message", "Detection"])

    with tab1:
        st.header("Encode a Secret Message")
        uploaded_image = st.file_uploader("Upload an image to encode", type=["png", "jpg", "jpeg"])
        if uploaded_image:
            st.image(uploaded_image, caption="Selected Image for Encoding", use_column_width=True)
        secret_message = st.text_area("Enter the secret message to hide")
        encode_button = st.button("Apply Encoding")

        if encode_button:
            if uploaded_image and secret_message:
                try:
                    encoded_image = encode_image(uploaded_image, secret_message)
                    st.success("Message encoded successfully!")
                    st.image(encoded_image, caption="Encoded Image", use_column_width=True)
                    st.download_button(
                        label="Download Encoded Image",
                        data=encoded_image,
                        file_name="encoded_image.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please upload an image and enter a secret message.")

    with tab2:
        st.header("Decode a Secret Message")
        encoded_image = st.file_uploader("Upload an image to decode", type=["png", "jpg", "jpeg"], key="decode")
        if encoded_image:
            st.image(encoded_image, caption="Selected Image for Decoding", use_column_width=True)
        decode_button = st.button("Apply Decoding")

        if decode_button:
            if encoded_image:
                try:
                    decoded_message = decode_image(encoded_image)
                    st.success("Message decoded successfully!")
                    st.text_area("Decoded Message", decoded_message, height=100)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
            else:
                st.error("Please upload an image to decode.")
    
    with tab3:
        st.header("Steganography Detection Tool")
        st.subheader("Analyze images for hidden messages based on LSB irregularities")

        uploaded_image = st.file_uploader("Upload an image to analyze", type=["png", "jpg", "jpeg"])
        analyze_button = st.button("Analyze Image")

        if analyze_button:
            if uploaded_image:
                try:
                    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
                    lsb_percentage, lsb_distribution = lsb_analysis(uploaded_image)

                    if lsb_percentage is None:
                        st.error("Unable to analyze the image.")
                    else:
                        st.write("### LSB Distribution Analysis")
                        st.write(f"**Percentage of LSBs:**\n- 0s: {lsb_percentage[0]:.2f}%\n- 1s: {lsb_percentage[1]:.2f}%")

                            # Visualization
                        st.write("### Visualization of LSB Distribution")
                        st.bar_chart({
                            "LSB Values": ["0s", "1s"],
                            "Percentage": lsb_percentage
                            })

                            # Detection threshold
                        threshold = 50  # Typically, natural images have an approximately equal distribution of 0s and 1s
                        if abs(lsb_percentage[0] - lsb_percentage[1]) > 5:
                            st.warning("The image shows irregular LSB distribution, suggesting possible steganographic modification.")
                        else:
                            st.success("The LSB distribution appears normal, with no clear indication of hidden data.")

                except Exception as e:
                    st.error(f"An error occurred while analyzing the image: {e}")
            else:
                st.error("Please upload an image for analysis.")

if __name__=="__main__":
    steganography_function()
