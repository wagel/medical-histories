import streamlit as st
from pathlib import Path
import base64
import requests
import json
# config
FILE_NAME = "file_5062418c-c7d2-4493-8a05-3a39485318c4.pdf"
CLAIM_ID = "clm-f1d461ce-4e6c-433a-ab93-c7eba7b9c49c"
CLAIM_URL = "https://admin.waggel.co.uk/claim/attachment?id=clm-f1d461ce-4e6c-433a-ab93-c7eba7b9c49c"
MEDICAL_HISTORY_URL = "https://admin.waggel.co.uk/claim/attachment?id=clm-f1d461ce-4e6c-433a-ab93-c7eba7b9c49c&attachmentId=5062418c-c7d2-4493-8a05-3a39485318c4"
POLICY_WORDING_URL = "https://www.waggel.co.uk/latest-policy-documents"
BACKEND_URL = "http://localhost:8000"
MOCK_RESPONSE = True

if MOCK_RESPONSE:
    with open("mock_response.json", "r") as f:
        MOCK_RESPONSE = json.load(f)


def extract_mock_response():
    return MOCK_RESPONSE["output"][0]["content"][0]["text"]


def extract_response(response):
    return response.json()["output"][0]["content"][0]["text"]


# Load and encode image for HTML display
def load_image(image_path):
    return base64.b64encode(Path(image_path).read_bytes()).decode()


# Load header image
header_image_path = "../assets/Waggel-Primary-Logos/header.png"
header_image_base64 = load_image(header_image_path)

welcome_text = """
Hello! I'm Klaimzy, your AI claims assistant. I'm here to get through nasty medical histories FAST. ⚡️⚡️⚡️
"""
# Configure the page
st.set_page_config(page_title="KLAIMZY by Waggel", layout="wide")


def show_error(message: str):
    st.error(f"⚠️ {message} ⚠️ ‼️😵‍💫", icon="🚨")



def assert_pet_data_on_record_match(test: bool = True):
    if test:
        show_error("Pet data in medical history does not match data on record.")

def assert_user_data_on_record_match(test: bool = True):
    if test:
        show_error("User data in medical history does not match data on record.")

def assert_no_pre_existing_condition(test: bool = True):
    if test:
        show_error("No pre-existing condition found.")



def document_section():
    st.subheader("Documents")
    if st.button("Medical History", key="medical", help="Navigate to Medical History", use_container_width=True, type="secondary"):
        js = f"window.open('{MEDICAL_HISTORY_URL}', '_blank')"
        st.components.v1.html(f"<script>{js}</script>")
    if st.button("Policy Wording", key="policy", help="Navigate to Policy Wording", use_container_width=True, type="secondary"):
        js = f"window.open('{POLICY_WORDING_URL}', '_blank')"
        st.components.v1.html(f"<script>{js}</script>")
    if st.button("Claim Profile", key="claim", help="Navigate to Claim Profile", use_container_width=True, type="secondary"):
        js = f"window.open('{CLAIM_URL}', '_blank')"
        st.components.v1.html(f"<script>{js}</script>")
    if st.button("Data on Record", key="data", help="Show Data on Record", use_container_width=True, type="secondary"):
        st.json({
            "file_name": FILE_NAME,
            "claim_id": CLAIM_ID,
            "claim_url": CLAIM_URL,
            "medical_history_url": MEDICAL_HISTORY_URL,
            "policy_wording_url": POLICY_WORDING_URL
        })


def klaimzy_header():
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; margin-top: -20px;">
            <img src="data:image/png;base64,{header_image_base64}" width="700" style="margin-right: 20px">
        </div>
        <div>
            <p>{welcome_text}</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.markdown(f"##### ClaimID: {CLAIM_ID}")

def analyze_claim_section():
    analyze_button = st.button("Analyze Claim", key="analyze", help="Analyze the claim data", use_container_width=True, type="primary")
    st.markdown(
        """
        <style>
        div[data-testid="stButton"] button[kind="primary"] {
            background-color: #ff6b00;
            color: white;
            padding: 0.5rem 1rem;
            font-size: 1.2rem;
            height: 3rem;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    # Initialize session state for analysis result
    if "analysis_result" not in st.session_state:
        st.session_state.analysis_result = None

    message_placeholder_ac = st.empty()
    if analyze_button:
        if MOCK_RESPONSE:
            extracted_response = extract_mock_response()
        else:
            message_placeholder_ac.markdown("<div style='text-align: center'>🔄 Analyzing claim...</div>", unsafe_allow_html=True)
            response = requests.post(f"{BACKEND_URL}/launch-analysis", json={"initial_message": "Hello, I need help with a claim"})
            extracted_response = extract_response(response)
        # Store the result in session state
        # message_placeholder.empty()
        st.session_state.analysis_result = extracted_response

    # Display analysis result if it exists (this will persist across reruns)
    if st.session_state.analysis_result:
        message_placeholder_ac.markdown(st.session_state.analysis_result, unsafe_allow_html=True)


# Create two columns for layout with col1 slightly larger
col1, col2 = st.columns([3, 2])

# Header and description on the left
with col1:
    klaimzy_header()
    assert_pet_data_on_record_match(False)
    assert_user_data_on_record_match(False)
    assert_no_pre_existing_condition(False)
    analyze_claim_section()
    document_section()

    if st.button("Check backend health", key="health", help="Check backend health", use_container_width=True, type="secondary"):
        response = requests.get(f"{BACKEND_URL}/healthz")
        st.write(response.json())

    if st.button("List conversation thread", key="conversation", help="List conversation thread", use_container_width=True, type="secondary"):
        response = requests.get(f"{BACKEND_URL}/list-conversation-thread")
        st.write(response.json())
    

# Chat on the right
with col2:
    st.title("Ask Klaimzy!")

    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Create a container for the chat history
    chat_container = st.container()
    
    # Create a container for the input at the bottom
    input_container = st.container()
    
    # Load avatars
    klaimzy_avatar = "../assets/Waggel-Primary-Logos/svg/waggel-badge-blue.svg"
    user_avatar = "../assets/Waggel-Primary-Logos/svg/waggel-badge-black.svg"

    # Display chat messages from history in the chat container
    with chat_container:
        for message in st.session_state.messages:
            avatar = klaimzy_avatar if message["role"] == "assistant" else user_avatar
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

    # Add some spacing to push the input to the bottom
    st.markdown("<br>" * 5, unsafe_allow_html=True)
    
    # Accept user input at the bottom
    with input_container:
        if prompt := st.chat_input("How can I help you with this claim?"):
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Display user message in chat message container
            with chat_container:
                with st.chat_message("user", avatar=user_avatar):
                    st.markdown(prompt)
                
                # Display assistant response in chat message container
                with st.chat_message("assistant", avatar=klaimzy_avatar):

                    # assert that the analysis result is not None
                    if st.session_state.analysis_result is None:
                        st.error("😵‍💫‼️ Please analyze the claim first")
                        st.stop()

                    message_placeholder = st.empty()
                    message_placeholder.markdown("Thinking... 🤔")
                    
                    response = requests.post(f"{BACKEND_URL}/add-message", json={"message": prompt})
                    message_placeholder.empty()
                    # st.write(response.json())
                    _extracted_response = extract_response(response)
                    st.markdown(_extracted_response)
                    # message_placeholder.markdown(_extracted_response, unsafe_allow_html=True)
                
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
            
    # Add custom CSS to style the chat interface
    st.markdown("""
        <style>
        .stChatFloatingInputContainer {
            position: fixed;
            bottom: 0;
            right: 0;
            width: 33%;  /* Adjust based on your column width */
            padding: 1rem;
            background: white;
        }
        </style>
    """, unsafe_allow_html=True)
