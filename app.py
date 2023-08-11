import streamlit as st
import requests
from streamlit_image_comparison import image_comparison
from PIL import Image
import io
import os
import replicate

# Main App
st.title("Floor Image Generator Demo")
st.set_page_config(page_title="Floor Demo", layout="wide")

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
        os.environ["URL"],
        input={"image": img_path,
               "prompt": f"Change floor to {selected_floor}"}
    )
    # Fetch the generated image
    response = requests.get(output[0]).content
    with open("output.jpg", "wb") as handler:
    	handler.write(response)
    gen_img = Image.open("output.jpg").convert('RGB')
    col1, col2 = st.columns(2)

    with col1:
       st.image(original, caption='Before')
    
    with col2:
       st.image(gen_img, caption=f'After with edited {selected_floor}')
else:
    st.write("Please upload an image and select a floor type to generate the modified image.")



    
if __name__ == '__main__':
    pass
