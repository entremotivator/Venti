# app.py
import streamlit as st
import requests
import json
from datetime import datetime

# ------------------------------
# App Configuration
# ------------------------------
st.set_page_config(
    page_title="Venti AI — Social Experience Chatbot",
    page_icon="🌟",
    layout="centered"
)

WEBHOOK_URL = "https://agentonline-u29564.vm.elestio.app/webhook/59097f82-c1e4-44ff-b2c3-09d2f9a2ea20"

# ------------------------------
# Bold Gold Theme Styling
# ------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fff8e1, #ffecb3);
    color: #3b2f0a;
    font-family: 'Inter', sans-serif;
    font-weight: 700;
}

h1, h2, h3, h4, h5, h6, p, div, span {
    font-weight: 800 !important;
    letter-spacing: 0.5px;
}

.stChatInputContainer {
    background: rgba(255,255,255,0.85);
    border-radius: 16px;
    border: 2px solid rgba(232,180,40,0.4);
}

.user-msg {
    background: linear-gradient(90deg, #ffefc1, #ffd54f);
    padding: 16px 20px;
    border-radius: 14px 14px 4px 14px;
    text-align: right;
    margin: 8px 0;
    color: #3b2f0a;
    font-size: 18px;
    font-weight: 800;
    box-shadow: 0 4px 12px rgba(232,180,40,0.15);
}

.ai-msg {
    background: linear-gradient(90deg, #fff, #fff8e1);
    padding: 16px 20px;
    border-left: 6px solid #e5b800;
    border-radius: 14px 14px 14px 4px;
    margin: 8px 0;
    font-size: 18px;
    font-weight: 800;
    box-shadow: 0 4px 12px rgba(232,180,40,0.15);
}

.timestamp {
    font-size: 13px;
    font-weight: 700;
    color: #6d5e3a;
    margin-top: 4px;
}

.stButton>button {
    background: linear-gradient(90deg, #f6d365, #fda085);
    border: none;
    border-radius: 10px;
    font-weight: 800;
    color: #3b2f0a;
    font-size: 16px;
    letter-spacing: 0.4px;
}

.stTextInput>div>div>input, textarea {
    font-size: 16px !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Initialize State
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ------------------------------
# Header
# ------------------------------
st.markdown("<h1 style='text-align:center; font-size:42px;'>🌟 Venti AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:22px;'>Your Bold Social Experience Creator — turn ideas into stunning posts, campaigns, and stories.</p>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------------
# Display Chat
# ------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='timestamp' style='text-align:right;'>{msg['time']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='timestamp'>{msg['time']}</div>", unsafe_allow_html=True)

# ------------------------------
# Chat Input
# ------------------------------
user_input = st.chat_input("Type your message to Venti AI...")

# ------------------------------
# Chat Logic
# ------------------------------
if user_input:
    timestamp = datetime.now().strftime("%I:%M %p")
    st.session_state.messages.append({"role": "user", "content": user_input, "time": timestamp})

    payload = {
        "chatInput": user_input,
        "timestamp": datetime.utcnow().isoformat(),
        "meta": {"source": "VentiAI Streamlit Chatbot"}
    }

    try:
        response = requests.post(WEBHOOK_URL, json=payload, timeout=15)
        if response.status_code == 200:
            data = response.json()
            reply = (
                data.get("reply")
                or data.get("response")
                or data.get("text")
                or data.get("message")
                or json.dumps(data, indent=2)
            )
        else:
            reply = f"⚠️ Webhook returned {response.status_code}."
    except Exception as e:
        reply = f"⚠️ Unable to connect to webhook: {e}"

    st.session_state.messages.append({"role": "assistant", "content": reply, "time": datetime.now().strftime("%I:%M %p")})
    st.rerun()

# ------------------------------
# Footer
# ------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-size:15px; font-weight:800; color:#5c4b1f;'>✨ Venti AI · Bold Conversations for Creative Minds · © 2025</p>",
    unsafe_allow_html=True
)
