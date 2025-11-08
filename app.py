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
# Custom Gold Theme Styling
# ------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #fff8e1, #ffecb3);
    color: #3b2f0a;
    font-family: 'Inter', sans-serif;
}
.stChatInputContainer {
    background: rgba(255,255,255,0.85);
    border-radius: 16px;
    border: 1px solid rgba(232,180,40,0.2);
}
.stChatMessage {
    font-size: 16px;
    padding: 10px;
}
.user-msg {
    background: linear-gradient(90deg, #ffefc1, #ffe082);
    padding: 10px 16px;
    border-radius: 12px 12px 2px 12px;
    text-align: right;
    margin: 6px 0;
    color: #3b2f0a;
}
.ai-msg {
    background: linear-gradient(90deg, #ffffff, #fff8e1);
    padding: 10px 16px;
    border-left: 4px solid #e5b800;
    border-radius: 12px 12px 12px 2px;
    margin: 6px 0;
}
.timestamp {
    font-size: 11px;
    color: #7d6b3f;
    margin-top: 3px;
}
.stButton>button {
    background: linear-gradient(90deg, #f6d365, #fda085);
    border: none;
    border-radius: 8px;
    font-weight: 600;
    color: #3b2f0a;
}
</style>
""", unsafe_allow_html=True)

# ------------------------------
# Initialize Session State
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "last_reply" not in st.session_state:
    st.session_state.last_reply = None

# ------------------------------
# Header
# ------------------------------
st.markdown("<h1 style='text-align:center;'>🌟 Venti AI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:17px;'>Your Personal Social Experience Creator — designed to help you craft engaging posts, campaigns, and brand conversations.</p>", unsafe_allow_html=True)
st.markdown("---")

# ------------------------------
# Display Chat History
# ------------------------------
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='timestamp' style='text-align:right;'>{msg['time']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-msg'>{msg['content']}</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='timestamp'>{msg['time']}</div>", unsafe_allow_html=True)

# ------------------------------
# User Input
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
    "<p style='text-align:center; font-size:13px; color:#6d5e3a;'>✨ Venti AI · Crafted for creative social storytelling · © 2025</p>",
    unsafe_allow_html=True
)
