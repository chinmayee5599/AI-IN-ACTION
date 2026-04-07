import streamlit as st
import pandas as pd
import random

# 🎨 UI Styling
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff4d4d, #990000);
    }
    h1, h2, h3 {
        color: white !important;
    }
    .chat-box {
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        color: black;
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🤖 GenScam: Advanced Scam Simulator")

# 📊 Load Dataset
try:
    df = pd.read_json("train.json", lines=True)
    if "text" in df.columns:
        df = df.dropna(subset=["text"])
        texts = df["text"].astype(str).tolist()
    else:
        st.error("❌ 'text' column missing")
        texts = []
except:
    st.error("❌ Dataset not found")
    texts = []

# ⚙️ Inputs
st.subheader("⚙️ Configure Scenario")

name = st.text_input("Enter Name")
scam_type = st.selectbox("Scam Type", ["Internship", "Banking", "Lottery"])
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
format_type = st.selectbox("Format", ["Email", "Chat", "SMS"])

# 🚦 Risk Indicator
if difficulty == "Easy":
    st.success("🟢 Low Risk")
elif difficulty == "Medium":
    st.warning("🟡 Medium Risk")
else:
    st.error("🔴 High Risk")

# 🎲 Generate
if st.button("🚀 Generate Scam"):

    if not texts:
        st.warning("No data available")
    else:
        sample = random.choice(texts)
        user = name if name else "User"

        # Highlight keywords
        keywords = ["click", "urgent", "verify", "password"]
        for word in keywords:
            sample = sample.replace(word, f"🔴{word.upper()}")

        # Format Output
        if format_type == "Email":
            output = f"""
Subject: {scam_type} Opportunity

Dear {user},

{sample[:150]}

Click below to proceed.

Regards,
Team
"""
        elif format_type == "Chat":
            output = f"Hey {user}! {sample[:100]} Reply ASAP!"
        else:
            output = f"URGENT: {sample[:80]} Click now!"

        st.subheader("📧 Generated Scam")
        st.text_area("Output", output, height=200)

        # 📥 Download
        st.download_button("⬇️ Download", output, file_name="scam.txt")

        # 💬 WhatsApp Style Chat
        if format_type == "Chat":
            st.subheader("💬 Chat Simulation")
            st.markdown(f'<div class="chat-box">👤 You: Hello?</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat-box">🤖 Scammer: {sample[:80]}</div>', unsafe_allow_html=True)

        # 🔗 Fake Login Page
        if st.button("🔗 Open Verification Page"):
            st.subheader("🔐 Secure Login")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                st.error("⚠️ This is a phishing simulation!")

        # 🧠 Explanation
        st.subheader("🧠 Why this is a scam?")
        st.write("This message uses urgency, fake authority, and manipulation tactics.")

# 📊 Dataset Info
st.subheader("📊 Dataset Info")
if texts:
    st.write("Total Samples:", len(texts))