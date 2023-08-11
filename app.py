import streamlit as st
import requests
from streamlit_image_comparison import image_comparison
from PIL import Image
import io

# Replicate API import (assuming you have the right setup and authentication)
import replicate

# Image comparison function
def image_comparison(image1, image2):
    # pil image
    # image = Image.open("image.jpg")
    # render image-comparison
    image_comparison(
        img1=image1,
        img2=image2,
    )
    
# Main App
st.title("Floor Image Generator")

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
    response = requests.get(output[0])
    with open("output.jpg", "wb") as handler:
    	handler.write(response)
    gen_img = Image.open("output.jpg").convert('RGB')
    # Compare original and generated images
    image_comparison(original, gen_img)
else:
    st.write("Please upload an image and select a floor type to generate the modified image.")

if __name__ == '__main__':
    pass
