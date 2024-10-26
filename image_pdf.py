import streamlit as st
from PIL import Image
from io import BytesIO

# Setting up the page configuration
st.set_page_config(page_title="Image to PDF Converter", page_icon="🖼️", layout="centered")

# Main app title and description
st.title("🖼️ JPEG/JPG to PDF Converter")
st.subheader("Convert your images to a PDF file in just a few clicks!")
st.write("Upload one or more JPEG or JPG images, and click **Convert** to generate a PDF file.")

# File upload section with expanded instructions
uploaded_images = st.file_uploader(
    "Choose JPEG or JPG Images to Upload", 
    type=["jpeg", "jpg"], 
    accept_multiple_files=True,
    help="Select one or more JPEG or JPG images to convert to PDF."
)

# Check if images are uploaded
if uploaded_images:
    st.success(f"{len(uploaded_images)} image(s) uploaded successfully!", icon="✅")
    # Display thumbnails of uploaded images
    st.write("**Preview of Uploaded Images:**")
    cols = st.columns(min(len(uploaded_images), 3))
    for i, uploaded_image in enumerate(uploaded_images):
        with cols[i % 3]:
            image = Image.open(uploaded_image)
            st.image(image, use_column_width=True)

    # Button to start conversion process
    if st.button("Convert to PDF"):
        st.info("Converting images, please wait...", icon="⏳")

        # List to store converted images
        image_list = []
        for uploaded_image in uploaded_images:
            image = Image.open(uploaded_image)
            if image.mode != "RGB":
                image = image.convert("RGB")
            image_list.append(image)

        # Save images to PDF if list is not empty
        if image_list:
            pdf_buffer = BytesIO()
            image_list[0].save(pdf_buffer, format="PDF", save_all=True, append_images=image_list[1:])
            pdf_buffer.seek(0)

            # Display the download button
            st.success("Conversion successful! Download your PDF below.", icon="📄")
            st.download_button(
                "📥 Download PDF",
                data=pdf_buffer,
                file_name="converted_images.pdf",
                mime="application/pdf"
            )
        else:
            st.error("No valid images found.")
else:
    st.info("Please upload JPEG or JPG images to start the conversion.")
