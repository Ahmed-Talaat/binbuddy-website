import streamlit as st
import requests
from PIL import Image
import io

# Function to call the prediction API
def call_prediction_api(image):
    url = "https://binbuddymvp-gufk4rxgcq-ew.a.run.app/predict"  # Replace with your API endpoint
    image_bytes = io.BytesIO()
    image.save(image_bytes, format='JPEG')
    image_bytes = image_bytes.getvalue()

    files = {'file': ('image.jpg', image_bytes, 'image/jpeg')}
    response = requests.post(url, files=files)
    return response.json()

# Streamlit app
st.title("🗑️ Bin Buddy 🗑️")
st.subheader("Helping you classify waste items effortlessly!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    st.write("")
    st.write("Classifying...")

    with st.spinner('Processing...'):
        # Call the API and get the prediction
        result = call_prediction_api(image)

    # Display the results
    st.success('Classification Complete!')
    st.write(f"**Prediction Class:** {result['prediction']}")
    st.write(f"**Prediction Score:** {result['score']}")
