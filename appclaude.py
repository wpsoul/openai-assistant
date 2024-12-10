# Importing required packages
import streamlit as st
import time
from anthropic import Anthropic

# Load instructions from file
def load_instructions():
    try:
        with open('instruction.txt', 'r') as file:
            return file.read()
    except FileNotFoundError:
        return "Default instructions if file not found."

# Set your Claude API key
api_key = st.secrets["claude_apikey"]
instructions = load_instructions()

# Set Claude client
def load_claude_client():
    return Anthropic(api_key=api_key)

client = load_claude_client()

# Get response from Claude
def get_assistant_response(user_input=""):
    system_prompt = f"""You are a GS Builder Assistant. Use these instructions as your knowledge base:
    {instructions}
    
    When building code for Greenshift, ensure blocks with text have textContent attribute."""
    
    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=4096,
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": user_input
        }]
    )
    
    return message.content[0].text

if 'user_input' not in st.session_state:
    st.session_state.user_input = ''

def submit():
    st.session_state.user_input = st.session_state.query
    st.session_state.query = ''


st.title("GS Builder Assistant")

st.text_input("Ask me to build blocks for GreenShift:", key='query', on_change=submit)

user_input = st.session_state.user_input

st.write("Please, wait for the assistant to respond. You entered: ", user_input)

if user_input:
    result = get_assistant_response(user_input + " Please, build code for Greenshift according to instructions in retrieved database. Make sure that blocks with text also have textContent attribute.")
    st.header('Assistant :green[GreenLight] ', divider='rainbow')
    st.markdown(result)

