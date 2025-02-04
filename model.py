import asyncio
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from groq import AsyncGroq

# Hardcoded API Key
GROQ_API_KEY = "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"

async def get_response(messages):
    client = AsyncGroq(api_key=GROQ_API_KEY)  # Pass API key directly

    chat_completion = await client.chat.completions.create(
        messages=messages,  # Send full chat history
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        max_completion_tokens=1024,
        top_p=1,
        stop=None,
        stream=False,
    )

    return chat_completion.choices[0].message.content

# Streamlit UI
st.title("Chat with Tejas.ai 🤖")
st.write("Have a continuous conversation with AI!")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are a helpful assistant."}
    ]

# Initialize session state for storing questions separately
if "questions" not in st.session_state:
    st.session_state.questions = []

# Display chat history
for msg in st.session_state.messages[1:]:  # Skip system message
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Append user question to a separate list
    st.session_state.questions.append(user_input)

    # Append user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Show loading animation
    with st.spinner("dakutejas.ai 🤔"):
        response = asyncio.run(get_response(st.session_state.messages))

    # Append AI response
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display AI response
    with st.chat_message("assistant"):
        st.write(response)

# Sidebar for additional features
st.sidebar.header("📌 Stored Questions")
for q in st.session_state.questions:
    st.sidebar.write(f"- {q}")

# 🔽 Download Questions as TXT
if st.sidebar.button("Download Questions (TXT)"):
    questions_text = "\n".join(st.session_state.questions)
    st.sidebar.download_button("📥 Download TXT", questions_text, "questions.txt", "text/plain")

# 🔽 Download Questions as CSV
if st.sidebar.button("Download Questions (CSV)"):
    questions_df = pd.DataFrame({"Questions": st.session_state.questions})
    csv_data = questions_df.to_csv(index=False).encode("utf-8")
    st.sidebar.download_button("📥 Download CSV", csv_data, "questions.csv", "text/csv")

# 📊 Generate a Chart (Message Count per Role)
if st.sidebar.button("Generate Chat Stats 📈"):
    roles = [msg["role"] for msg in st.session_state.messages if msg["role"] != "system"]
    role_counts = pd.Series(roles).value_counts()

    fig, ax = plt.subplots()
    role_counts.plot(kind="bar", color=["blue", "green"], ax=ax)
    ax.set_xlabel("Role")
    ax.set_ylabel("Message Count")
    ax.set_title("Chat Messages Breakdown")
    st.sidebar.pyplot(fig)
