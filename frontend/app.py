import base64
from pathlib import Path

import requests
import streamlit as st

# Add API configuration
API_URL = "http://backend:8000"  # This will be the service name in docker-compose


def load_image(image_path):
    """Load and encode image for HTML display"""
    return base64.b64encode(Path(image_path).read_bytes()).decode()


# load assets
root = "."  # "frontend"
logo_path = f"{root}/Waggel-Primary-Logos/png/waggel-blue.png"
badge_path = f"{root}/Waggel-Primary-Logos/png/waggel-badge-blue.png"
dog_coin_path = f"{root}/Waggel-Primary-Logos/png/icon-dog-coin-blue.png.avif"
logo_base64 = load_image(logo_path)
badge_base64 = load_image(badge_path)
dog_coin_base64 = load_image(dog_coin_path)

# Configure the page
st.set_page_config(page_title="Waggel Line Items", page_icon=badge_path, layout="wide", initial_sidebar_state="expanded")


# Load and display the Waggel logos
SHOW_BADGE = False
if SHOW_BADGE:
    try:
        st.markdown(
            (
                f'<div style="text-align: center; padding: 2rem 0;">'
                f'<img src="data:image/png;base64,{badge_base64}" width="100" style="margin-right: 20px">'
                if SHOW_BADGE
                else "" f'<img src="data:image/png;base64,{logo_base64}" width="300">' f"</div>"
            ),
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Could not load logo or badge - Exception: {e}")
else:
    try:
        st.markdown(
            f'<div style="text-align: center; padding: 2rem 0;">' f'<img src="data:image/png;base64,{logo_base64}" width="300">' f"</div>",
            unsafe_allow_html=True,
        )
    except Exception as e:
        st.error(f"Could not load logo - Exception: {e}")

# Main app layout
st.title("Line Items Extraction")

# Create two columns for the main content
col1, col2 = st.columns(2)


def _process_extract_text(extracted_text: str):
    return extracted_text.replace("```Markdown", "").replace("```", "")


with col1:
    with st.container():
        st.subheader("Upload Documents")
        uploaded_files = st.file_uploader("Upload your documents here", type=["pdf", "png", "jpg"], accept_multiple_files=True)
        submit_button = st.button("Submit", type="primary", use_container_width=False)

with col2:
    with st.container():
        st.subheader("Results")
        if submit_button and uploaded_files:
            try:
                files = [("files", file) for file in uploaded_files]
                response = requests.post(f"{API_URL}/upload/", files=files)

                if response.status_code == 200:
                    EXTRACTED_TEXT = response.json()["results"][0]["extracted_text"]
                    EXTRACTED_TEXT = _process_extract_text(EXTRACTED_TEXT)
                    print(EXTRACTED_TEXT)
                    st.success("Files processed successfully!")
                    # st.text(EXTRACTED_TEXT)
                    st.markdown(EXTRACTED_TEXT)
                else:
                    st.error(f"Error processing files: {response.text}")
            except Exception as e:
                st.error(f"Error communicating with the backend: {str(e)}")
        else:
            st.write("Upload files and click Submit to process them...")

# Footer
st.markdown(
    f"""
    <div style="text-align: center; position: fixed; bottom: 0; left: 0; right: 0; padding: 2rem 0; background-color: transparent;">
        <img src="data:image/png;base64,{dog_coin_base64}" width="90">
        <p style='font-size: 0.8rem; opacity: 0.7;'>© 2025 Waggel. All rights reserved.</p>
    </div>
""",
    unsafe_allow_html=True,
)
