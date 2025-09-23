import streamlit as st
from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import datetime

# -------------------- Page Config --------------------
st.set_page_config(
    page_title="🧠 AI Global Brain",
    page_icon="🌐",
    layout="wide"
)

# -------------------- Custom CSS --------------------
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
/* Chat bubbles */
.user-bubble {
    background: #1f4068;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: #f1f1f1;
}
.ai-bubble {
    background: #162447;
    padding: 12px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: #eeeeee;
}
/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d1b2a;
}
/* Titles */
h1, h2, h3 {
    color: #00d4ff !important;
    text-shadow: 0px 0px 10px rgba(0,212,255,0.8);
}
/* Metric Card */
[data-testid="stMetric"] {
    background: rgba(0, 212, 255, 0.15);
    padding: 10px;
    border-radius: 12px;
}
/* Input box */
.stTextInput>div>div>input {
    background-color: #1b1b2f;
    color: #fff;
    border-radius: 8px;
}
/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00c6ff, #0072ff);
    color: white;
    border-radius: 10px;
    border: none;
    padding: 10px 20px;
    font-weight: bold;
    transition: 0.3s;
}
.stButton>button:hover {
    transform: scale(1.05);
    background: linear-gradient(90deg, #0072ff, #00c6ff);
}
/* Footer */
.footer {
    text-align: center;
    padding: 10px;
    color: #00d4ff;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -------------------- Sidebar --------------------
st.sidebar.title("🌐 AI Global Brain")
st.sidebar.markdown("Enter your Groq API Key to start:")
api_key_input = st.sidebar.text_input("🔑 Groq API Key", type="password")

# -------------------- Initialize Memory --------------------
memory = ConversationBufferMemory()

# -------------------- Sidebar AI Modes --------------------
st.sidebar.markdown("---")
st.sidebar.markdown("Choose AI Mode:")
brain_mode = st.sidebar.radio(
    "AI Mode",
    ["🧑‍🔬 Scientist Brain", "📊 Analyst Brain", "🎨 Creative Brain"]
)

st.sidebar.markdown("---")
st.sidebar.metric("🕒 Current Time", datetime.datetime.now().strftime("%H:%M:%S"))
st.sidebar.write("✨ Powered by LangChain + Groq")

# -------------------- Chat System --------------------
if "history" not in st.session_state:
    st.session_state.history = []

st.title("🧠 AI Global Brain")
st.markdown("Welcome to the **Next-Gen Pro AI Brain**. Ask me anything!")

user_input = st.text_input("💬 Type your question here...")

col1, col2 = st.columns([1,1])
with col1:
    ask_button = st.button("🚀 Ask Brain")
with col2:
    clear_button = st.button("🗑️ Clear Chat")

# Clear chat
if clear_button:
    st.session_state.history = []
    st.success("Chat cleared!")

# Handle ask button
if ask_button and user_input.strip() != "":
    if not api_key_input:
        st.warning("⚠️ Please enter your Groq API Key to get a response.")
    else:
        with st.spinner("🤖 AI is thinking..."):
            # Initialize LLM
            llm = ChatGroq(model="llama-3.3-70b-versatile", api_key=api_key_input)
            conversation = ConversationChain(llm=llm, memory=memory)

            # Personality Prompts
            if brain_mode == "🧑‍🔬 Scientist Brain":
                system_prompt = "You are a highly intelligent scientist. Provide detailed, clear explanations with references if possible."
            elif brain_mode == "📊 Analyst Brain":
                system_prompt = "You are a data-driven analyst. Provide logical answers with examples, numbers, and trends."
            else:
                system_prompt = "You are a creative thinker. Provide imaginative, innovative, and engaging answers."

            prompt = ChatPromptTemplate.from_messages([
                ("system", system_prompt),
                ("human", "{question}")
            ])
            final_prompt = prompt.format(question=user_input)
            response = llm.invoke(final_prompt)

            # Save to history
            st.session_state.history.append(("user", user_input))
            st.session_state.history.append(("ai", response.content))

# -------------------- Chat Display --------------------
st.subheader("🗨️ Conversation")
for role, text in st.session_state.history:
    if role == "user":
        st.markdown(f"<div class='user-bubble'>👤 {text}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='ai-bubble'>🤖 {text}</div>", unsafe_allow_html=True)

# -------------------- Download Chat --------------------
if st.session_state.history:
    chat_text = "\n".join([f"{role.upper()}: {txt}" for role, txt in st.session_state.history])
    st.download_button("💾 Download Chat", chat_text, file_name="AI_Global_Brain_Chat.txt")

# -------------------- Footer --------------------
st.markdown("<div class='footer'>📧 ahmadpacer456h@gmail.com | AhmadXAi</div>", unsafe_allow_html=True)


