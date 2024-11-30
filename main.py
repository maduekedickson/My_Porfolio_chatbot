import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import time

# Initialize Gemini Pro API
genai.configure(api_key="AIzaSyCbknlcRQiRQ5B1JtodNeCFHJeAxYJFD0E")

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
        content += '\n'.join([heading.get_text() for heading in headings])
        content += '\n'.join([para.get_text() for para in paragraphs])
        content += '\n'.join([li.get_text() for list_tag in lists for li in list_tag.find_all('li')])

        return content
    except Exception as e:
        return f"Error fetching content from the URL: {e}"

# Chatbot setup
def initialize_chat(content):
    model = genai.GenerativeModel("gemini-1.5-flash")
    chat = model.start_chat(
        history=[
            {"role": "user", "parts": "Hello, I would like to know about the courses offered at Schoolville."},
            {"role": "model", "parts": "Sure! Based on the content from Schoolville, here's what I found:"},
            {"role": "model", "parts": content},  # Feed content as part of chat history
        ]
    )
    return chat

# Streamlit App
st.title("💬 Schoolville Content-Based Chatbot")

# Get content from URL
url = "https://www.schoolville.com"
content = get_website_content(url)

if content:
    st.write("Content successfully retrieved from Schoolville.")
else:
    st.write("Failed to fetch content from Schoolville.")

# Input Section
user_input = st.text_input("Ask a question about the content above:")

# Placeholder for chatbot response
response_placeholder = st.empty()

# Process input and get chatbot response
if user_input:
    # Display "Typing..." message
    with response_placeholder:
        st.write("🤖 Typing...")
    
    # Simulate delay
    time.sleep(2)
    
    # Initialize chat with content
    chat = initialize_chat(content)
    
    # Get response from Gemini API based on the user's question and website content
    response = chat.send_message(user_input)
    
    # Display the response
    response_placeholder.write(f"🤖: {response.text}")
