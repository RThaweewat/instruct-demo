import streamlit as st
import requests
from streamlit_image_comparison import image_comparison
from PIL import Image
import io

# Replicate API import (assuming you have the right setup and authentication)
import replicate

# Main App
st.title("Floor Image Generator Demo")

# Image uploader
uploaded_image = st.file_uploader("Choose an image", type=["jpg", "png"])
if uploaded_image is not None:
    img_path = uploaded_image
    original = Image.open(uploaded_image).convert('RGB')
if uploaded_image is None:
    st.warning("Please upload an image first.")
    st.stop()

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
    response = requests.get(output[0]).content
    with open("output.jpg", "wb") as handler:
    	handler.write(response)
    gen_img = Image.open("output.jpg").convert('RGB')
else:
    st.write("Please upload an image and select a floor type to generate the modified image.")


col1, col2 = st.columns(2)

with col1:
   st.image(original, caption='Before')

with col2:
   st.image(gen_img, caption=f'After with edited {floor_elements}')
    
if __name__ == '__main__':
    pass
