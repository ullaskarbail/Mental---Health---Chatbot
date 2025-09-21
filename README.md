# Mental---Health---Chatbot
# 🧠 Mental Health Support Chatbot

A web-based chatbot built using Streamlit and the Google Gemini API, designed to provide compassionate mental health support. The bot offers emotional support, coping strategies, and resources while maintaining professional boundaries. It includes user authentication, conversation history, chat export, and crisis resources.

## Features

💬 Real-time Chat: Users can interact with the chatbot to receive empathetic responses.

🔑 Authentication: Password-protected access to the chatbot for privacy and security.

🧩 Gemini API Integration: Uses Google’s generative language API for intelligent responses.

📝 Conversation History: Keeps track of user and bot messages.

📥 Download Chat: Export the chat history as a .txt file for personal records.

🧰 Configuration Panel: Easily input and manage Gemini API keys.

🚨 Crisis Resources: Quick access to emergency mental health contacts.

🎨 Stylish UI: Smooth animations, message bubbles, and gradients for an engaging interface.

⚡ Chat Management: Clear chat, refresh conversation, and view conversation statistics.

## Installation

### Clone this repository:

git clone https://github.com/ullaskarbail/Mental---Health---Chatbot.git
cd Mental---Health---Chatbot


### Create and activate a virtual environment (optional but recommended):

python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows


#### Install dependencies:

pip install -r requirements.txt


(Required: streamlit, requests)

Usage

### Run the chatbot:

streamlit run mentalhealth.py


### Configure API Key

Enter your Google Gemini API key in the configuration section.

Instructions to get the API key are included in the UI.

### Login

Enter the password mental_health_2024 to access the chatbot.

Start Chatting

Type your messages in the input box and click "Send Message".

The bot responds with empathetic support and guidance.

Additional Options

Clear chat history 🗑️

Refresh conversation 🔄

View chat stats 📊

Download chat history 📝

Crisis Resources

🚑 Emergency: 911

🆘 Suicide Prevention: 988

💬 Crisis Text Line: 741741

📞 SAMHSA: 1-800-662-4357

### Configuration & Security

Password-protected: Default password format is mental_health_YYYY.

Gemini API key required for chatbot responses.

All sensitive information is stored in Streamlit session state.

Customization

Mental Health Prompt: The system prompt for the Gemini API can be edited in the code:

MENTAL_HEALTH_PROMPT = """You are a compassionate mental health support chatbot...
"""


Animations & UI: Customize CSS animations and message bubble styles in the <style> section.

Dependencies

Python 3.9+

Streamlit

Requests

License

This project is open-source for educational and personal use. Do not use it as a substitute for professional mental health services.

Disclaimer

This chatbot is not a replacement for professional therapy or medical advice. If you are in crisis, please contact emergency services immediately.
