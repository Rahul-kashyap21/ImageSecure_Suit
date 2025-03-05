import streamlit as st
from PIL import Image, ImageDraw, ImageFont
import io
import numpy as np
def watermark_():
# Function to create a visible watermark on an image
    def add_visible_watermark(image, watermark_text, size, opacity):
        width, height = image.size
        font_size = int(size)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except IOError:
            font = ImageFont.load_default()

    # Create watermark layer
    # Create watermark layer
        watermark_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
        watermark_draw = ImageDraw.Draw(watermark_layer)

        # Calculate center position
        text_width, text_height = watermark_draw.textbbox((0, 0), watermark_text, font=font)[2:]
        x = (width - text_width) / 2
        y = (height - text_height) / 2

        # Add shadow
        shadow_color = (0, 0, 0, int(opacity * 0.3))
        watermark_draw.text((x + 3, y + 3), watermark_text, font=font, fill=shadow_color)

        # Add main watermark in a slant line
        watermark_color = (255, 255, 255, int(opacity))
        for i in range(-width, width, text_width + 20):
            watermark_draw.text((x + i, y + i), watermark_text, font=font, fill=watermark_color)


        # Combine the watermark layer with the original image
        combined_image = Image.alpha_composite(image.convert("RGBA"), watermark_layer).convert("RGB")
        return combined_image

    # Function to embed an invisible watermark in an image
    def add_invisible_watermark(image, watermark_text):
        binary_watermark = ''.join(format(ord(char), '08b') for char in watermark_text)
        img_array = np.array(image)
        flat_image = img_array.flatten()

        for i in range(len(binary_watermark)):
            flat_image[i] = flat_image[i] & ~1 | int(binary_watermark[i])

        watermarked_image = flat_image.reshape(img_array.shape)
        return Image.fromarray(watermarked_image.astype(np.uint8))

    # Function to detect an invisible watermark in an image
    def detect_invisible_watermark(image, watermark_length):
        img_array = np.array(image)
        flat_image = img_array.flatten()
        binary_watermark = ''.join(str(flat_image[i] & 1) for i in range(watermark_length * 8))
        watermark = ''.join(chr(int(binary_watermark[i:i + 8], 2)) for i in range(0, len(binary_watermark), 8))
        return watermark

    # Streamlit UI
    
    st.header("Visible and Invisible Watermarking Tool")

    col1, col2 = st.tabs(["Visible","Invisible"])

    with col1:
        st.header("Visible Watermark")
        watermark_text = st.text_input("Enter Watermark Text", key="visible_text")

        uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"], key="visible_upload")

        if uploaded_file and (watermark_text):
            image = Image.open(uploaded_file).convert("RGB")

            size = st.slider("Select Font Size", 10, 200, 50, key="font_size")
            opacity = st.slider("Select Opacity", 0, 255, 128, key="opacity")
                

            watermarked_image = add_visible_watermark(
                image, watermark_text, size, opacity
                )

            st.image(watermarked_image, caption="Watermarked Image")
            buffer = io.BytesIO()
            watermarked_image.save(buffer, format="PNG")
            st.download_button("Download Watermarked Image", buffer.getvalue(), "visible_watermarked_image.png")

    with col2:
        st.header("Invisible Watermark")

        watermark_text = st.text_input("Enter Invisible Watermark Text", key="invisible_text")
        uploaded_file = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"], key="invisible_upload")

        if uploaded_file and watermark_text:
            image = Image.open(uploaded_file).convert("RGB")
            watermarked_image = add_invisible_watermark(image, watermark_text)

            st.image(watermarked_image, caption="Image with Invisible Watermark")
            buffer = io.BytesIO()
            watermarked_image.save(buffer, format="PNG")
            st.download_button("Download Image with Invisible Watermark", buffer.getvalue(), "invisible_watermarked_image.png")

        if st.header("Check Invisible Watermark"):
            uploaded_file = st.file_uploader("Upload an Image to Check Watermark", type=["png", "jpg", "jpeg"], key="check_upload")
            watermark_length = st.number_input("Enter Watermark Length", min_value=1, step=1, key="watermark_length")

            if uploaded_file and watermark_length:
                image = Image.open(uploaded_file).convert("RGB")
                extracted_watermark = detect_invisible_watermark(image, watermark_length)
                st.write("Extracted Watermark:", extracted_watermark)

if __name__ == "__main__":
     watermark_()
