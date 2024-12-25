import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import os
import time

# Initialize Gemini Pro API
api_key = os.getenv("AIzaSyCbknlcRQiRQ5B1JtodNeCFHJeAxYJFD0E")
if not api_key:
    st.error("API key not found! Please set it as an environment variable.")
else:
    genai.configure(api_key=api_key)

# Web scraping the content of the URL
def get_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraphs = soup.find_all('p')
        lists = soup.find_all(['ul', 'ol'])

        content = ''
        content += '\n'.join([heading.get_text() for heading in headings]) + "\n\n"
        content += '\n'.join([para.get_text() for para in paragraphs]) + "\n\n"
        content += '\n'.join([li.get_text() for list_tag in lists for li in list_tag.find_all('li')])

        return content
    except Exception as e:
        return f"Error fetching content from the URL: {e}"

# Generate response from Gemini API
def generate_response(prompt, content):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        full_prompt = f"{content}\n\nUser: {prompt}\nBot:"
        response = model.generate_text(prompt=full_prompt)
        return response.candidates[0]["output"] if response and response.candidates else "No response generated."
    except Exception as e:
        return f"Error generating response: {e}"

# Streamlit App
st.title("💬 Madueke Portfolio Chatbot")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Fetch website content
url = "https://madueke-portfolio.web.app/"
content = get_website_content(url)

if "Error" in content:
    st.write("Failed to fetch content from the website.")
else:
    st.write("Website content successfully retrieved.")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"**🧑 You:** {message['text']}")
        elif message["role"] == "bot":
            st.markdown(f"**🤖 Bot:** {message['text']}")

# Input Section
user_input = st.text_input("Type your message here:")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Simulate typing
    with st.spinner("🤖 Bot is typing..."):
        time.sleep(2)

        # Generate bot response
        bot_response = generate_response(user_input, content)

        # Add bot response to chat history
        st.session_state.chat_history.append({"role": "bot", "text": bot_response})

    # Clear the input box after sending the message
    st.experimental_set_query_params(message="")
