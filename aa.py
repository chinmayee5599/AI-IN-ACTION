import streamlit as st
import pandas as pd
import random

# 🎨 RED UI
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(135deg, #ff4d4d, #990000);
    }
    h1, h2, h3, label {
        color: white !important;
    }
    .chat {
        background: white;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🏷️ TITLE
st.title("🤖 GenScam: AI Scam Scenario Generator")

# 📊 LOAD DATASET
try:
    df = pd.read_json("train.json", lines=True)
    df = df.dropna(subset=["text"])
    texts = df["text"].astype(str).tolist()
    st.success("✅ Dataset Loaded")
except:
    texts = []
    st.error("❌ Dataset not found")

# ⚙️ CONFIG
st.subheader("⚙️ Configure Scenario")

name = st.text_input("Enter Name (optional)")

scam_type = st.selectbox(
    "Scam Type",
    ["Internship", "Banking", "Lottery", "Job Offer"]
)

difficulty = st.selectbox(
    "Difficulty",
    ["Easy", "Medium", "Hard"]
)

format_type = st.selectbox(
    "Format",
    ["Email", "Chat", "SMS"]
)

# 🚦 RISK LEVEL
if difficulty == "Easy":
    st.success("🟢 Low Risk")
elif difficulty == "Medium":
    st.warning("🟡 Medium Risk")
else:
    st.error("🔴 High Risk")

# 🎲 GENERATE
if st.button("🚀 Generate Scam"):

    if not texts:
        st.warning("No dataset available")
    else:
        sample = random.choice(texts)
        user = name if name else "User"

        # 🚨 Highlight keywords
        keywords = ["click", "urgent", "verify", "password"]
        for word in keywords:
            sample = sample.replace(word, f"🔴{word.upper()}")

        # ✉️ FORMAT
        if format_type == "Email":
            output = f"""
Subject: {scam_type} Opportunity

Dear {user},

{sample[:150]}

Click below to proceed.

Regards,
Support Team
"""

        elif format_type == "Chat":
            output = f"Hey {user}! {sample[:100]} Reply ASAP!"

        else:
            output = f"URGENT: {sample[:80]} Click now!"

        # 📧 OUTPUT
        st.subheader("📧 Generated Scam")
        st.text_area("Output", output, height=200)

        # 💬 CHAT UI
        if format_type == "Chat":
            st.subheader("💬 Chat Simulation")
            st.markdown(f'<div class="chat">👤 You: Hello?</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="chat">🤖 Scammer: {sample[:80]}</div>', unsafe_allow_html=True)

        # 🔐 FAKE LOGIN
        if st.button("🔗 Open Verification Page"):
            st.subheader("🔐 Secure Login")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                st.error("⚠️ This is a phishing simulation!")

        # 📥 DOWNLOAD
        st.download_button("⬇️ Download", output, file_name="scam.txt")

        # 🧠 EXPLANATION
        st.subheader("🧠 Why this is a scam?")
        st.write("This message uses urgency, social engineering, and manipulation tactics.")

# 📊 DATA INFO
st.subheader("📊 Dataset Info")
if texts:
    st.write("Total Samples:", len(texts))