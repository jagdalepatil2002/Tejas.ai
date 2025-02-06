import asyncio
import time
import streamlit as st
import fitz  # PyMuPDF for PDF Processing
from groq import AsyncGroq

# Hardcoded API Key (REPLACE WITH YOUR ACTUAL KEY)
GROQ_API_KEY = "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"

# Predefined Response for Creator Questions
CREATOR_QUESTIONS = {...}  # Same as before (keeping it concise)
CREATOR_RESPONSE = (
    "I was developed by Meta AI and fine-tuned by **Tejas Jagdale**, AI Engineer based in Pune.\n\n"
    "LinkedIn Profile: [Tejas Jagdale](https://www.linkedin.com/in/jagdaletejas/)"
)

# Function to get AI response
async def get_response(messages):
    client = AsyncGroq(api_key=GROQ_API_KEY)
    try:
        chat_completion = await client.chat.completions.create(
            messages=messages, model="llama-3.3-70b-versatile",
            temperature=0.5, max_completion_tokens=1024, top_p=1,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error getting response: {e}")
        return "An error occurred. Please try again later."

# Extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
        text = "\n".join([page.get_text() for page in doc])
        return text[:5000]  # Limit to prevent overload
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return ""

# Streamlit UI
st.title("Chat with Tejas.ai 🤖")
st.write("Say it Simply!!")

# Initialize session states
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
if "questions" not in st.session_state:
    st.session_state.questions = []
if "responses" not in st.session_state:
    st.session_state.responses = []

# PDF Upload Feature
st.sidebar.header("📄 Upload a PDF")
uploaded_pdf = st.sidebar.file_uploader("Upload PDF", type=["pdf"])

extracted_text = ""
if uploaded_pdf:
    extracted_text = extract_text_from_pdf(uploaded_pdf)
    if extracted_text:
        st.sidebar.write("✅ PDF Loaded Successfully!")
        st.session_state.messages.append({"role": "user", "content": f"Context from uploaded PDF: {extracted_text}"})

# Display chat history
for i in range(len(st.session_state.questions)):
    with st.chat_message("user"):
        st.write(f"**You:** {st.session_state.questions[i]}")
    with st.chat_message("assistant"):
        st.write(f"**Tejas.ai:** {st.session_state.responses[i]}")

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    if user_input.strip().lower() in [q.lower() for q in CREATOR_QUESTIONS]:
        response = CREATOR_RESPONSE
    else:
        if len(st.session_state.questions) == 0:
            st.session_state.messages = [{"role": "system", "content": "You are a helpful assistant."}]
        st.session_state.questions.append(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.spinner("Tejas.ai 💭 Thinking..."):
            response = asyncio.run(get_response(st.session_state.messages))

    with st.chat_message("user"):
        st.write(f"**You:** {user_input}")

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        animated_response = ""
        for char in response:
            animated_response += char
            response_placeholder.markdown(f"**Tejas.ai:** {animated_response} ▌")
            time.sleep(0.003)
        response_placeholder.markdown(f"**Tejas.ai:** {response}")
        st.session_state.responses.append(response)

# Sidebar - Stored Questions
st.sidebar.header("📌 Stored Questions")
for q in st.session_state.questions:
    st.sidebar.write(f"- {q}")

# Download Questions & Responses
if st.sidebar.button("Download Chat (TXT)"):
    chat_text = "\n\n".join(
        [f"Q: {q}\nA: {r}" for q, r in zip(st.session_state.questions, st.session_state.responses)]
    )
    st.sidebar.download_button("📥 Download TXT", chat_text, "chat_history.txt", "text/plain")

st.sidebar.info("Developed and Fine-Tuned by **Tejas Jagdale**. Connect on [LinkedIn](https://www.linkedin.com/in/jagdaletejas/).")
