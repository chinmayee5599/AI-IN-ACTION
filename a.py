import streamlit as st
import pandas as pd
import random
import time
# 🎨 UI STYLE
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
st.title("🤖 GenScam: AI Scam Simulator")

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

# 🚦 RISK LEVEL
if difficulty == "Easy":
    st.success("🟢 Low Risk")
elif difficulty == "Medium":
    st.warning("🟡 Medium Risk")
else:
    st.error("🔴 High Risk")

# 🧠 SESSION STATE
if "score" not in st.session_state:
    st.session_state.score = 0

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# 🤖 AI RESPONSE FUNCTION
def generate_scammer_reply(user_input, scam_type, difficulty):
    prompt = f"""
You are an expert scammer targeting students.

Scam Type: {scam_type}
Difficulty: {difficulty}

Victim says: "{user_input}"

Rules:
- Be persuasive and realistic
- Create urgency
- Try to get sensitive info (login, OTP, password)
- If user hesitates → increase pressure
- If user agrees → push for credentials
- Never reveal you are a scam

Keep response short and conversational.
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You simulate scam conversations for cybersecurity training."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.9
        )

        return response.choices[0].message.content

    except Exception as e:
        return "⚠️ AI Error. Check API key or internet."

# 🚀 START SIMULATION
if st.button("🚀 Start Simulation"):

    user = name if name else "User"

    if texts:
        sample = random.choice(texts)
    else:
        sample = "We have an exclusive opportunity for you."

    st.session_state.chat_history = [
        f"🤖 Scammer: Hello {user}, {sample[:150]}"
    ]

    st.session_state.score = 0

# 💬 CHAT DISPLAY
st.subheader("💬 Live Scam Simulation")

for msg in st.session_state.chat_history:
    st.markdown(f'<div class="chat">{msg}</div>', unsafe_allow_html=True)

# 💬 CHAT INPUT
with st.form("chat_form"):
    user_reply = st.text_input("Your Reply")
    submitted = st.form_submit_button("Send Reply")

if submitted and user_reply:
    st.session_state.chat_history.append(f"👤 You: {user_reply}")

    # 🤖 AI GENERATED RESPONSE
    ai_reply = generate_scammer_reply(user_reply, scam_type, difficulty)

    st.session_state.chat_history.append(f"🤖 Scammer: {ai_reply}")

    # 🎯 SCORING SYSTEM
    risky_words = ["password", "otp", "bank", "login", "verify"]

    if any(word in user_reply.lower() for word in risky_words):
        st.session_state.score += 15
    else:
        st.session_state.score += 5

# 🎯 SCORE DISPLAY
st.subheader("🎯 Your Risk Score")

if st.session_state.score < 15:
    st.success("🟢 Safe User")
elif st.session_state.score < 40:
    st.warning("🟡 Moderate Risk")
else:
    st.error("🔴 High Risk - Vulnerable to scams!")

# 🔗 FAKE LINK
st.markdown("🔗 https://secure-verification-login.com")

# 🔐 PHISHING PAGE
st.subheader("🔐 Verification Portal")

username = st.text_input("Email / Username")
password = st.text_input("Password", type="password")

if st.button("Login Securely"):
    st.session_state.score += 25
    st.error("⚠️ This is a phishing simulation! Credentials stolen.")

# ⏳ URGENCY TIMER
st.subheader("⏳ Limited Time Offer")

placeholder = st.empty()
for i in range(5, 0, -1):
    placeholder.warning(f"⏳ Offer expires in {i} seconds!")
    time.sleep(1)

# 📊 ANALYTICS
st.subheader("📊 Simulation Stats")

st.metric("Risk Score", st.session_state.score)
st.metric("Messages Exchanged", len(st.session_state.chat_history))

# 🧠 EXPLANATION
st.subheader("🧠 Why this is a scam?")

st.write("""
- Uses urgency and pressure tactics  
- Requests sensitive data  
- Mimics trusted authority  
- Manipulates emotions  
""")

# 📊 DATA INFO
st.subheader("📊 Dataset Info")

if texts:
    st.write("Total Samples:", len(texts))