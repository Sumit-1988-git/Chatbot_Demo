# furniture_chatbot.py

import streamlit as st
import openai
import re
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Guardrails: Define restricted topics or commands
def violates_guardrails(user_input):
    restricted_patterns = [
        r"(?i)refund",  # prevent refund queries
        r"(?i)politics|religion",  # off-topic sensitive subjects
        r"(?i)abuse|hate|violence"  # harmful content
    ]
    return any(re.search(pattern, user_input) for pattern in restricted_patterns)

# Furniture domain-specific system prompt
SYSTEM_PROMPT = """
You are a helpful assistant for a furniture retail store.
Answer only furniture-related questions like:
- Product availability
- Types of furniture
- Material & design queries
- Store hours, delivery options, assembly support
Do not engage in refund, abusive or off-topic content.
"""

# Function to get OpenAI response
def get_bot_response(user_input):
    if violates_guardrails(user_input):
        return "I'm sorry, I can't assist with that request. Please ask about our furniture products or services."

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        temperature=0.5,
        max_tokens=200
    )
    return response.choices[0].message.content

# Streamlit UI
st.set_page_config(page_title="Furniture Store Chatbot", page_icon="🛋️")
st.title("🛋️ Furniture Store Chatbot")
st.markdown("Ask me about our products, designs, store hours, delivery and more!")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "input_text" not in st.session_state:
    st.session_state.input_text = ""

user_input = st.text_input("You:", value=st.session_state.input_text, key="input")

if user_input:
    st.session_state.chat_history.append(("user", user_input))
    bot_reply = get_bot_response(user_input)
    st.session_state.chat_history.append(("bot", bot_reply))
    st.session_state.input_text = ""
    #st.rerun()  # Prevent duplicate processing during rerender

# Display conversation
for role, msg in st.session_state.chat_history:
    if role == "user":
        st.markdown(f"**You:** {msg}")
    else:
        st.markdown(f"**Bot:** {msg}")
