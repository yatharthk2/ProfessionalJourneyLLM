import os
import streamlit as st
from chat import query_chatbot_with_prompt, load_model

# Load the model on startup
load_model()

# Custom CSS for styling
st.markdown(
    """
    <style>
    .main {
        background-color: #f7f9fc;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        color: #000000;  /* Set text color to black */
        border-left: 5px solid #800080;  /* Purple accent for the introductory block */
    }
    .stTextInput, .stButton {
        margin-top: 20px;
    }
    .stTextInput input {
        border-radius: 10px;
        padding: 10px;
    }
    .stButton button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 10px;
    }
    .response {
        margin-top: 20px;
        padding: 15px;
        background-color: #ffffff;
        border-radius: 10px;
        color: #333333;
        font-size: 16px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .you {
        border-left: 5px solid #FF0000;  /* Red accent for the 'You' block */
    }
    .assistant {
        border-left: 5px solid #4CAF50;  /* Green accent for the 'Assistant' block */
    }
    body {
        background-color: #e6e6e6;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize session state for storing conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# App title and description
st.title("LLM Assistant for Recruiters")
st.markdown("""
    <div class="main">
        <p> Hi, This is Yatharth ask any question about my professional journey to the LLM assistant :)</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header("Configuration")
st.sidebar.markdown("Use the options below to configure your query.")
question = st.sidebar.text_input("Enter your question:")

if st.sidebar.button("Ask"):
    if question:
        with st.spinner('Processing...'):
            try:
                response = query_chatbot_with_prompt(question)
                st.session_state.conversation.append({"role": "You", "message": question})
                st.session_state.conversation.append({"role": "Assistant", "message": response})
            except Exception as e:
                st.sidebar.error(f"No response from the assistant. Error: {e}")
    else:
        st.sidebar.error("Please enter a question.")

# Display conversation history only if there are responses
if st.session_state.conversation:
    for entry in st.session_state.conversation:
        if entry["role"] == "You":
            st.markdown(f'<div class="response you"><strong>{entry["role"]}:</strong> {entry["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="response assistant"><strong>{entry["role"]}:</strong> {entry["message"]}</div>', unsafe_allow_html=True)
