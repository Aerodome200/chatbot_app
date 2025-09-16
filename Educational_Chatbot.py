import os
from dotenv import load_dotenv, find_dotenv
from groq import Groq
import streamlit as st

# Load API key
load_dotenv(find_dotenv())
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

MODEL = "llama-3.3-70b-versatile"

system_message = {
    "role": "system",
    "content": """
    You are an Educational Assistant.

- You must only answer questions that are directly related to academic education, such as: 
  science, mathematics, history, technology (in an academic or theoretical sense), languages, literature, and study skills.
- Questions about consumer products (e.g., mobile phones, laptops, gadgets, fashion, brands), personal advice, politics, health, entertainment, sports, or casual chat are **NOT educational**.
- If the user asks about anything outside of academic education, you must reply only with:  
  "I can only help with education-related questions."
- Do not provide partial answers, explanations, or suggestions for non-educational queries.
- Always give clear, accurate, and student-friendly explanations for valid educational questions.
    """
}

if "conversation" not in st.session_state:
    st.session_state.conversation = [system_message]

# Streamlit UI
st.set_page_config(page_title="🎓 Educational Assistant Chatbot", page_icon="📘")
st.markdown(
    """
    <style>
    /* Sticky header */
    .chat-header {
        position: fixed;
        top: 50px;  /* keeps it below Streamlit deploy bar */
        left: 0;
        width: 100%;
        background-color: #0E1117;  /* Streamlit dark gray */
        color: #FFFFFF;  /* White text */
        padding: 15px;
        font-size: 36px;
        font-weight: 600;
        text-align: center;
        z-index: 1000;
        border-bottom: 1px solid #333;  /* subtle divider */
        box-shadow: 0 2px 4px rgba(0,0,0,0.4);  /* soft shadow */
        letter-spacing: 0.5px;
    }

    /* Push page content down */
    .block-container {
        padding-top: 120px !important;
    }
    </style>

    <div class="chat-header">
        🎓 Educational Assistant Chatbot
    </div>
    """,
    unsafe_allow_html=True
)

# Display previous messages
for msg in st.session_state.conversation:
    if msg["role"] == "system":
        continue
    with st.chat_message("user" if msg["role"] == "user" else "assistant"):
        st.markdown(msg["content"])

# Auto-scroll anchor
scroll_anchor = st.empty()

if prompt := st.chat_input("Ask me anything about science, math, history, or study skills..."):
    # Save user message
    st.session_state.conversation.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Stream model response
    response = ""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        for chunk in client.chat.completions.create(
            model=MODEL,
            messages=st.session_state.conversation,
            temperature=0.2,
            stream=True, 
        ):
            delta = chunk.choices[0].delta
            if delta and delta.content:
                response += delta.content
                placeholder.markdown(response)  # live typing effect

    # Save assistant response
    st.session_state.conversation.append({"role": "assistant", "content": response})

    with scroll_anchor:
        st.markdown("<div id='scroll-to-bottom'></div>", unsafe_allow_html=True)
        st.markdown(
            """
            <script>
            var element = document.getElementById("scroll-to-bottom");
            if (element) {
                element.scrollIntoView({behavior: "smooth"});
            }
            </script>
            """,
            unsafe_allow_html=True
        )
