import streamlit as st
from mira_sdk import MiraClient, Flow
import os
from dotenv import load_dotenv


st.set_page_config(page_title="Client Project Q&A", page_icon="❓")

# Custom CSS for styling
st.markdown(
    """
    <style>
    body {
        font-family: 'Arial', sans-serif; /* Modern font */
        background-color: #f4f4f4; /* Light background */
        color: #333;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1 {
        color: #007bff; /* Primary color */
        text-align: center;
        margin-bottom: 2rem;
    }
    .stTextArea textarea, .stTextInput input{
        border-radius: 8px;
        border: 1px solid #ddd;
        padding: 10px;
        width: 100%;
        box-sizing: border-box;
    }
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        border: none;
        cursor: pointer;
        width: 100%; /* Full width button */
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    .stAlert {
        border-radius: 8px;
        padding: 15px;
        margin-top: 1rem;
    }
    .stSuccess {
      border-radius: 8px;
        padding: 15px;
        margin-top: 1rem;
        background-color: #d4edda;
        border-color: #c3e6cb;
        color: #155724;
    }
    .stExpander {
        border-radius: 8px;
        border: 1px solid #ddd;
        margin-top: 1rem;
        padding: 10px;
    }
    .stExpanderHeader {
        font-weight: bold;
    }
    hr {
        margin-top: 2rem;
        margin-bottom: 1rem;
        border: 0;
        border-top: 1px solid #ddd;
    }
    footer {
        text-align: center;
        color: grey;
        margin-top: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Client Project Knowledge Hub")
st.markdown("Ask questions about your completed projects or how to tackle a new project")

load_dotenv()

API_KEY = os.getenv("MIRA_API_KEY")

if not API_KEY:
    st.error("MIRA_API_KEY environment variable not set. Please set it.")
else:
    question = st.text_area("Enter your question about a project:")
    version = st.text_input("Enter Flow Version (Optional, leave as it is for latest)", value="0.0.3")

    if st.button("Get Answer"):
        if not question:
            st.warning("Please enter a question.")
        else:
            try:
                with st.spinner("Fetching answer..."):
                    client = MiraClient(config={"API_KEY": API_KEY})
                    input_data = {"question": question}
                    if version:
                        flow_name = f"@mayank/client-based-company-qna/{version}"
                    else:
                        flow_name = "@mayank/cliet-based-company-qna"

                    result = client.flow.execute(flow_name, input_data)

                    if result:
                        if "result" in result:  # Correctly check for "result" key
                            st.subheader("Answer:")
                            st.write(result["result"])  # Access the value using result["result"]
                        elif "error" in result:
                            st.error(f"Error from Mira API: {result['error']}")
                        else:
                            st.error(f"Unexpected response structure from Mira API: {result}")
                            st.json(result)
                    else:
                        st.error("No response received from Mira API.")

            except Exception as e:
                st.error(f"An error occurred: {e}")

st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<footer style='text-align: center; color: grey;'>Powered by Mira/Made by Mayank</footer>", unsafe_allow_html=True)