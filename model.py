import asyncio
import time
import streamlit as st
from groq import AsyncGroq

# Hardcoded API Key (REPLACE WITH YOUR ACTUAL KEY)
GROQ_API_KEY = "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"  # <--- IMPORTANT: Replace this!

# Predefined Response for Creator Questions
CREATOR_QUESTIONS = [
    "Who made you?", "Who are you?", "Who created you?", 
    "Which company or organization developed you?", "Where were you trained and developed?", 
    "What is your origin or development history?", "Who developed you","Are you an open-source or proprietary model?",
    "Which research lab or AI team built you?", "What is the name of the company that owns you?",
    "Are you based on any publicly available AI models?", "Where is your parent company headquartered?",
    "What language models were you trained on, and who provided them?","who made you", "who are you", "who created you", 
    "who developed you", "who trained you","who is your parent company", "who is your owner", 
    "who is your creator", "who is your developer", "who is your manufacturer", "who is your inventor", 
    "who is your designer", "who is your builder", "who is your founder", "who is your maker", "what is your origin", 
    "what is your source", "who is your master", "who is your boss", "who is your supervisor", "who is your manager",
    "who is your leader", "who is your head", "who is your chief", "which company or organization developed you",
    "where were you trained and developed", "what is your origin or development history",
    "are you an open-source or proprietary model", "which research lab or ai team built you",
    "what is the name of the company that owns you", "are you based on any publicly available ai models",
    "where is your parent company headquartered", "what language models were you trained on, and who provided them",
    "who is Tejas Jagdale","Who is Tejas Jagdale","Who is Tejas Jagdale?","who is Tejas Jagdale?"
]

CREATOR_RESPONSE = (
    "I was developed by Meta AI and fine-tuned by *Tejas Jagdale*, AI Engineer based in Pune.\n\n"
    "LinkedIn Profile: https://www.linkedin.com/in/jagdaletejas/"
)

async def get_response(messages):
    client = AsyncGroq(api_key=GROQ_API_KEY)
    try:
        chat_completion = await client.chat.completions.create(
            messages=messages,
            model="llama-3.3-70b-versatile",
            temperature=0.5,
            max_completion_tokens=1024,
            top_p=1,
            stop=None,
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response: {e}")
        return "An error occurred. Please try again later."

st.title("Chat with Tejas.ai 🤖")
st.write("Say it Simply!!")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_messages" not in st.session_state:
    st.session_state.current_messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "needs_animation" not in st.session_state:
    st.session_state.needs_animation = False
if "latest_response" not in st.session_state:
    st.session_state.latest_response = None

# Display chat history with auto-scroll
chat_placeholder = st.empty()
with chat_placeholder.container():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Auto-scrolling animation
if st.session_state.needs_animation and st.session_state.latest_response:
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        animated_response = ""
        for char in st.session_state.latest_response:
            animated_response += char
            response_placeholder.markdown(f"**Tejas.ai:** {animated_response} ▌")
            time.sleep(0.01)  # Adjust speed for smoother animation
            chat_placeholder.rerun()  # Force UI update to auto-scroll
        response_placeholder.markdown(f"**Tejas.ai:** {st.session_state.latest_response}")
    
    st.session_state.messages.append({"role": "assistant", "content": f"**Tejas.ai:** {st.session_state.latest_response}"})
    st.session_state.needs_animation = False
    st.session_state.latest_response = None
    chat_placeholder.rerun()  # Final scroll adjustment

user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": f"**You:** {user_input}"})
    
    if user_input.strip().lower() in [q.lower() for q in CREATOR_QUESTIONS]:
        response = CREATOR_RESPONSE
    else:
        st.session_state.current_messages.append({"role": "user", "content": user_input})
        with st.spinner("Tejas.ai 💭 Thinking..."):
            response = asyncio.run(get_response(st.session_state.current_messages))
        st.session_state.current_messages.append({"role": "assistant", "content": response})
    
    st.session_state.needs_animation = True
    st.session_state.latest_response = response
    st.rerun()

st.sidebar.header("📌 Stored Questions")
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.sidebar.write(f"- {msg['content'].replace('**You:** ', '')}")

if st.sidebar.button("Download Chat (TXT)"):
    chat_text = "\n\n".join([msg["content"] for msg in st.session_state.messages])
    st.sidebar.download_button("📥 Download TXT", chat_text, "chat_history.txt", "text/plain")

st.sidebar.info("Developed and Fine-Tuned by *Tejas Jagdale*. Connect on https://www.linkedin.com/in/jagdaletejas/.")
