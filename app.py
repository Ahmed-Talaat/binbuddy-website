import streamlit as st
import requests
from PIL import Image
import io
import streamlit.components.v1 as components

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
st.markdown("""
    <style>
    body {
        background-color: #FFA500;  /* Orange background */
    }
    .main {
        background-color: white;  /* White background for the main content */
        padding: 10px;
        border-radius: 10px;
        text-align: center; /* Center all content */
    }
    .center {
        text-align: center;
        font-size: 26px;
        margin-top: 20px; /* Increase spacing between lines */
    }
    .underline {
        text-decoration: underline;
    }
    /* Customize file uploader frame */
    .stFileUploader > div > div {
        background-color: #e67215; /* Background color */
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="main">
        <h1 style="font-size: 48px;">🗑️
            <span style="color: orange;">B</span>
            <span style="color: brown;">i</span>
            <span style="color: green;">n</span>
            <span style="color: yellow;"> </span>
            <span style="color: blue;">B</span>
            <span style="color: black;">u</span>
            <span style="color: orange;">d</span>
            <span style="color: brown;">d</span>
            <span style="color: green;">y</span>
        🗑️</h1>
    </div>
""", unsafe_allow_html=True)

st.subheader("Helping you classify waste items effortlessly!")

uploaded_file = st.file_uploader("Choose your garbage...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Add enlarged UI gif after subheader and before processing
    giphy_embed = """
    <div style="display: flex; justify-content: center;">
        <iframe src="https://giphy.com/embed/7Zgj8WBkzmaeqxQmZM" width="640" height="336" style="border:none;" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
    </div>
    """
    components.html(giphy_embed, width=800, height=400)

    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)

    status_placeholder = st.empty()
    status_placeholder.write("Classifying...")

    with st.spinner('Processing...'):
        # Call the API and get the prediction
        result = call_prediction_api(image)

    # Update the status placeholder with the results
    status_placeholder.success('Classification Complete!')

    # Display the results with confetti
    confetti_embed = """
    <div style="display: flex; justify-content: center;">
        <iframe src="https://giphy.com/embed/lPoOHG39XAlV4it61H" width="800" height="400" style="border:none;" frameBorder="0" class="giphy-embed" allowFullScreen></iframe>
    </div>
    """
    components.html(confetti_embed, width=800, height=200)

    prediction_score = result['score'] * 100  # Convert to percentage

    prediction_class = result['prediction']
    if prediction_class == "trash":
        prediction_class = f"This is <span class='underline'>Restmüll</span> at {round(prediction_score, 1)}%...<br><div class='center'>If I were you, I'd head to the <span style='color:black; font-size:26px'><strong>BLACK</strong></span> bin!</div>"
    elif prediction_class == "paper":
        prediction_class = f"Looks like <span class='underline'>Papier</span> ({round(prediction_score, 1)}% likely).<br><div class='center'><span style='color:blue; font-size:26px'><strong>BLUE</strong></span> is the bin color you're looking for.</div>"
    elif prediction_class == "biological":
        prediction_class = f"<span class='underline'>Biomüll</span>, easy one ({round(prediction_score, 1)}% likely)!<br><div class='center'>Either the <span style='color:brown; font-size:26px'><strong>BROWN</strong></span> or the <span style='color:green; font-size:26px'><strong>GREEN</strong></span> bin</div>"
    elif prediction_class == "glass":
        prediction_class = f"<span class='underline'>Glas</span>, I'm {round(prediction_score, 1)}% sure!<br><div class='center'>Look for the <span style='color:white; background-color:black; font-size:26px'><strong>WHITE</strong></span> bin and <span style='font-weight:bold;'>remember</span> to separate <em>Weiß</em> (transparent) and <em>Grün/Braunglass</em> (colored) glass.</div>"
    elif prediction_class == "plastic":
        prediction_class = f"<span class='underline'>Wertstoffe</span>, {round(prediction_score, 1)}% sure!<br><div class='center'><span style='color:#b3b300; font-size:26px'><strong>YELLOW</strong></span> or <span style='color:orange; font-size:26px'><strong>ORANGE</strong></span> bin, please ;)</div>"

    st.markdown(f"""
    <div class="center">
        {prediction_class}
    </div>
    """, unsafe_allow_html=True)
