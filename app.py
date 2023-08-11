import streamlit as st
import requests
from PIL import Image
import io

# Replicate API import (assuming you have the right setup and authentication)
import replicate

# Image comparison function
def image_comparison(img1, img2):
    # Add functionality to compare img1 and img2.
    # Placeholder for now: Simply display both.
    col1, col2 = st.beta_columns(2)
    with col1:
        st.image(img1, caption='Original Image', use_column_width=True)
    with col2:
        st.image(img2, caption='Generated Image', use_column_width=True)

# Main App
st.title("Floor Image Generator")

# Image uploader
uploaded_image = st.file_uploader("Choose an image", type=["jpg", "png"])
if uploaded_image is not None:
    img_path = uploaded_image
    original = Image.open(uploaded_image).convert('RGB')
else:
    original = Image.new("RGB", (512, 512), color="white")  # default white image

# Dropdown for floor elements
floor_elements = [
    "wood", 
    "red carpet", 
    "blue carpet", 
    "norwegian wood", 
    "marble", 
    "ceramic tiles", 
    "laminate"
]
selected_floor = st.selectbox("Select a floor type:", floor_elements)

# Button to generate image
if st.button('Generate Image'):
    # Call to replicate
    output = replicate.run(
        "timothybrooks/instruct-pix2pix:30c1d0b916a6f8efce20493f5d61ee27491ab2a60437c13c588468b9810ec23f",
        input={"image": img_path,
               "prompt": f"Change floor to {selected_floor}"}
    )
    # Fetch the generated image
    response = requests.get(output[0])
    generated_image = Image.open(io.BytesIO(response.content)).convert('RGB')
    
    # Compare original and generated images
    image_comparison(original, generated_image)
else:
    st.write("Please upload an image and select a floor type to generate the modified image.")

if __name__ == '__main__':
    pass
