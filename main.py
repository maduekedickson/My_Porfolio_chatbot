import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import os
import time

# Initialize Gemini Pro API
genai.configure(api_key=os.getenv("AIzaSyCbknlcRQiRQ5B1JtodNeCFHJeAxYJFD0E"))  # Replace with your environment variable

# Web scraping the content of the URL
def get_website_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract headings, paragraphs, and lists
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraphs = soup.find_all('p')
        lists = soup.find_all(['ul', 'ol'])

        # Combine headings, paragraphs, and list items into a single string
        content = ''
        content += '\n'.join([heading.get_text() for heading in headings]) + "\n\n"
        content += '\n'.join([para.get_text() for para in paragraphs]) + "\n\n"
        content += '\n'.join([li.get_text() for list_tag in lists for li in list_tag.find_all('li')])

        return content
    except Exception as e:
        return f"Error fetching content from the URL: {e}"

# Streamlit App
st.title("💬 Madueke Portfolio Chatbot")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Get content from URL
url = "https://madueke-portfolio.web.app/"
content = get_website_content(url)

if "Error" in content:
    st.write("Failed to fetch content from the website.")
else:
    st.write("Website content successfully retrieved.")

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.markdown(f"**🧑 You:** {message['text']}")
    elif message["role"] == "bot":
        st.markdown(f"**🤖 Bot:** {message['text']}")

# Input Section
user_input = st.text_input("Type your message here:")

# Process input and get chatbot response
if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "text": user_input})

    # Display "Typing..." message
    with st.spinner("🤖 Bot is typing..."):
        time.sleep(2)  # Simulate delay

        # Initialize Gemini Pro Chat API
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Here's some content to guide the conversation:"},
               {"role": "model", "parts": content},
                {"role": "user", "parts": user_input},
            ]
        )

        # Generate response
        response = chat.send_message(user_input)
        bot_response = response.text if response else "Sorry, I couldn't process that."

        # Add bot response to chat history
        st.session_state.chat_history.append({"role": "bot", "text": bot_response})

    # Refresh the chat interface
    st.experimental_rerun()
