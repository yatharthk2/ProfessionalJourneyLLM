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
        color: #000000;
        border-left: 5px solid #800080;
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
        border-left: 5px solid #FF0000;
    }
    .assistant {
        border-left: 5px solid #4CAF50;
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
st.markdown("<h2 style='color: black;'>Yatharth's Professional Journey Guide</h2>", unsafe_allow_html=True)
st.markdown("""
    <div class="main">
        <p> Hi, This is Yatharth. Feel free to ask any question about my professional journey :) </p>
    </div>
    """, unsafe_allow_html=True)

# Add Refresh Conversation button below the introductory message
if st.button("Refresh Conversation"):
    st.session_state.conversation = []
    st.experimental_rerun()

# Sidebar for user input
st.sidebar.header("Ask Your Own Question")
question = st.sidebar.text_input("Enter your question here:")
if st.sidebar.button("Submit Question"):
    if question:
        with st.spinner('Processing...'):
            try:
                response = query_chatbot_with_prompt(question)
                st.session_state.conversation.append({"role": "You", "message": question})
                st.session_state.conversation.append({"role": "Yatharth", "message": response})
            except Exception as e:
                st.sidebar.error(f"No response from the assistant. Error: {e}")
    else:
        st.sidebar.error("Please enter a question.")

# Display Quick Questions as buttons
st.sidebar.header("Quick Questions")
quick_questions = ["What is your current role?", "What projects have you worked on?", "Can you explain your experience with machine learning?"]
for q in quick_questions:
    if st.sidebar.button(q):
        with st.spinner('Processing...'):
            try:
                response = query_chatbot_with_prompt(q)
                st.session_state.conversation.append({"role": "You", "message": q})
                st.session_state.conversation.append({"role": "Yatharth", "message": response})
            except Exception as e:
                st.sidebar.error(f"No response from the assistant. Error: {e}")

# Display conversation history only if there are responses
if st.session_state.conversation:
    for entry in st.session_state.conversation:
        if entry["role"] == "You":
            st.markdown(f'<div class="response you"><strong>{entry["role"]}:</strong> {entry["message"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="response assistant"><strong>{entry["role"]}:</strong> {entry["message"]}</div>', unsafe_allow_html=True)
