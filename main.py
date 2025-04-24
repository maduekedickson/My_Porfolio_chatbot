import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import time

# Configure Gemini Pro API
genai.configure(api_key="AIzaSyC19s5ue_E4Qt1DDTomHMWuqCinIISzNBc")

# Web scraping the content of the URL
def get_website_content(url):
    try:
        response = requests.get(url, timeout=10)  # Add a timeout to handle hanging requests
        response.raise_for_status()  # Raise an error for HTTP error responses

        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract headings, paragraphs, and lists
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        paragraphs = soup.find_all('p')
        lists = soup.find_all(['ul', 'ol'])

        # Combine headings, paragraphs, and list items into a single string
        content = '\n'.join([heading.get_text() for heading in headings])
        content += '\n'.join([para.get_text() for para in paragraphs])
        content += '\n'.join([li.get_text() for list_tag in lists for li in list_tag.find_all('li')])

        if not content.strip():
            return None, "The website does not contain any valid content to extract."
        
        return content, None  # Return content and no error
    except requests.exceptions.RequestException as e:
        return None, f"Network error: {e}"  # Handle network-related errors
    except Exception as e:
        return None, f"Unexpected error: {e}"  # Handle other exceptions


# Initialize the chatbot with content
def initialize_chat(content):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[
                {"role": "user", "parts": ["Hello, I would like to know about the courses offered at Schoolville."]},
                {"role": "model", "parts": ["Sure! Based on the content from Schoolville, here's what I found:"]},
                {"role": "model", "parts": [content]},  # Feed content as part of chat history
            ]
        )
        return chat
    except Exception as e:
        st.error(f"Failed to initialize chatbot: {e}")
        return None


# Streamlit App
st.title("💬 My Portfolio Content-Based Chatbot 💬")

# Display website link in an appealing way
st.markdown(
    """
    **Portfolio Link:**  
    👉 [Madueke Portfolio](https://madueke-portfolio.web.app)
    """
)

# Fetch content from the portfolio website
url = "https://madueke-portfolio.web.app"
content, error_message = get_website_content(url)

if content:
    st.success("Content successfully retrieved from Madueke Portfolio.")
else:
    st.error(error_message)

# Input Section
if content:
    st.write("### Ask a question about the portfolio content:")
    user_input = st.text_input("Type your question here:")
else:
    st.write("No content available for chatbot interaction due to an error in retrieval.")

# Chatbot interaction
if content and user_input:
    response_placeholder = st.empty()
    with response_placeholder:
        st.write("🤖 Typing...")

    # Simulate delay
    time.sleep(2)

    # Initialize chat
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
