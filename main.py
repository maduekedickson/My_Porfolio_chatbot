import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import time

# Configure Gemini Pro API
genai.configure(api_key="AIzaSyDnLRWR5q1Wdcdj1PmZXqKhuypwsrsKGb8")

# Web scraping the content of the URL
def get_website_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract headings, paragraphs, and lists
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraphs = soup.find_all('p')
        lists = soup.find_all(['ul', 'ol'])

        # Combine headings, paragraphs, and list items into a single string
        content = '\n'.join([heading.get_text() for heading in headings])
        content += '\n'.join([para.get_text() for para in paragraphs])
        content += '\n'.join([li.get_text() for list_tag in lists for li in list_tag.find_all('li')])

        return content
    except Exception as e:
        return f"Error fetching content from the URL: {e}"

# Initialize the chatbot with content
def initialize_chat(content):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                {"role": "user", "content": "Hello, I would like to know about the courses offered at Schoolville."},
                {"role": "model", "content": "Sure! Based on the content from Schoolville, here's what I found:"},
                {"role": "model", "content": content},  # Feed content as part of chat history
            ]
        )
        return chat
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        return None

# Streamlit App
st.title("💬 My Portfolio Content-Based Chatbot 💬")
st.text("https://madueke-portfolio.web.app")

# Fetch content from the portfolio website
url = "https://madueke-portfolio.web.app"
content = get_website_content(url)

if "Error" not in content:
    st.success("Content successfully retrieved from Madueke Portfolio.")
else:
    st.error(content)

# Input Section
user_input = st.text_input("Ask a question about the portfolio:")

# Chatbot interaction
if user_input:
    response_placeholder = st.empty()
    with response_placeholder:
        st.write("🤖 Typing...")

    # Simulate delay
    time.sleep(2)

    # Initialize chat if not already done
    if "Error" not in content:
        chat = initialize_chat(content)
        if chat:
            try:
                # Get response from Gemini API
                response = chat.send_message(user_input)
                response_placeholder.write(f"🤖: {response.text}")
            except Exception as e:
                response_placeholder.write(f"Error during chatbot interaction: {e}")
        else:
            response_placeholder.write("Chatbot initialization failed.")
    else:
        response_placeholder.write("No content available for chatbot interaction.")
