import streamlit as st
import requests
import json
import time

st.set_page_config(page_title="Mental Health Chatbot", page_icon="🧠", layout="wide")

def init_session_state():
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []
    if 'gemini_api_key' not in st.session_state:
        st.session_state.gemini_api_key = ""
    if 'access_password' not in st.session_state:
        st.session_state.access_password = ""
    if 'is_authenticated' not in st.session_state:
        st.session_state.is_authenticated = False

init_session_state()

st.markdown("""
<style>
    @keyframes fadeIn {
        0% { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }
    
    .fade-in {
        animation: fadeIn 0.8s ease-in-out;
    }
    
    .slide-in {
        animation: slideIn 0.6s ease-out;
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    .chat-container {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        max-height: 500px;
        overflow-y: auto;
    }
    
    .crisis-alert {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        color: white;
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        animation: pulse 2s infinite;
        text-align: center;
        font-weight: bold;
    }
    
    .welcome-header {
        text-align: center;
        padding: 20px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 20px;
        animation: fadeIn 1s ease-in-out;
    }
    
    .config-section {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        animation: slideIn 0.8s ease-out;
    }
    
    .password-section {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 20px;
        border-radius: 15px;
        margin: 10px 0;
        animation: slideIn 1s ease-out;
    }
    
    .message-bubble {
        padding: 15px;
        border-radius: 20px;
        margin: 10px 0;
        animation: fadeIn 0.5s ease-in-out;
    }
    
    .user-message {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-left: 15%;
    }
    
    .bot-message {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        margin-right: 15%;
    }
    
    .success-box {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%);
        color: white;
        padding: 10px;
        border-radius: 10px;
        text-align: center;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

# --- Configuration Constants ---
CORRECT_PASSWORD = "mental_health_2024"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# --- Mental Health System Prompt ---
MENTAL_HEALTH_PROMPT = """You are a compassionate mental health support chatbot. Your role is to:
- Provide emotional support and active listening
- Offer evidence-based coping strategies and techniques
- Encourage professional help when appropriate
- Be empathetic, non-judgmental, and supportive
- Never provide medical diagnoses or replace professional therapy
- Recognize crisis situations and provide appropriate resources
- Keep responses concise but meaningful (2-3 paragraphs maximum)

Please respond in a caring, supportive manner while maintaining professional boundaries."""

# --- Gemini API call function ---
def call_gemini(prompt, conversation_history=None):
    try:
        if not st.session_state.gemini_api_key:
            return "Please configure your Gemini API key first."
        
        contents = []
        
        contents.append({"role": "user", "parts": [{"text": MENTAL_HEALTH_PROMPT}]})
        contents.append({"role": "model", "parts": [{"text": "I understand. I'm here to provide compassionate mental health support while maintaining appropriate boundaries. How can I help you today?"}]})
        
        if conversation_history:
            for msg in conversation_history[-6:]:
                if msg["role"] in ["user", "assistant"]:
                    role = "user" if msg["role"] == "user" else "model"
                    contents.append({"role": role, "parts": [{"text": msg["content"]}]})
        
        contents.append({"role": "user", "parts": [{"text": prompt}]})

        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": st.session_state.gemini_api_key
        }

        data = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 800,
                "topP": 0.8,
                "topK": 40
            },
            "safetySettings": [
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"}
            ]
        }

        response = requests.post(GEMINI_URL, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "I'm sorry, I couldn't generate a response. Please try again or rephrase your message."
            
    except requests.exceptions.RequestException as e:
        return f"Connection error: Please check your internet connection and API key. Error: {str(e)}"
    except Exception as e:
        return f"An error occurred: {str(e)}. Please try again."

col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.markdown('<div class="config-section">', unsafe_allow_html=True)
    st.markdown("## 🔧 Configuration")
    
    new_api_key = st.text_input(
        "🔑 Gemini API Key",
        value=st.session_state.gemini_api_key,
        type="password",
        help="Get your key from Google AI Studio",
        placeholder="Enter your API key here..."
    )
    
    if new_api_key != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = new_api_key
    
    if st.session_state.gemini_api_key:
        st.markdown('<div class="success-box">✅ API Key Configured!</div>', unsafe_allow_html=True)
    else:
        st.warning("⚠️ Please enter your Gemini API key")
    
    # Instructions
    with st.expander("📋 How to get API Key"):
        st.markdown("""
        1. Visit [Google AI Studio](https://ai.google.dev)
        2. Sign in with Google account
        3. Click "Get API Key"
        4. Create new API key
        5. Copy and paste above
        """)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="password-section">', unsafe_allow_html=True)
    st.markdown("## 🔐 Access Control")
    
    password_input = st.text_input(
        "🔒 Enter Password",
        type="password",
        help="Password required for access",
        placeholder="Enter password..."
    )
    
    if st.button("🚀 Login"):
        if password_input == CORRECT_PASSWORD:
            st.session_state.is_authenticated = True
            st.session_state.access_password = password_input
            st.success("✅ Access Granted!")
            st.balloons()
            time.sleep(1)
            st.experimental_rerun()
        else:
            st.session_state.is_authenticated = False
            st.error("❌ Incorrect Password")
    
    if st.session_state.is_authenticated:
        st.markdown('<div class="success-box">🎉 Welcome! You are logged in.</div>', unsafe_allow_html=True)
        
        if st.button("🚪 Logout"):
            st.session_state.is_authenticated = False
            st.session_state.access_password = ""
            st.experimental_rerun()
    
    with st.expander("💡 Password Hint"):
        st.info("Format: mental_health_YYYY")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="crisis-alert">', unsafe_allow_html=True)
    st.markdown("### 🚨 Crisis Resources")
    st.markdown("""
    **Emergency Help:**
    - 🚑 Emergency: 911
    - 🆘 Suicide Prevention: 988
    - 💬 Crisis Text: 741741
    - 📞 SAMHSA: 1-800-662-4357
    """)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    if not st.session_state.gemini_api_key:
        st.markdown('<div class="welcome-header">', unsafe_allow_html=True)
        st.markdown("## 🧠 Mental Health Support Chatbot")
        st.markdown("### Please configure your API key to continue")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    
    if not st.session_state.is_authenticated:
        st.markdown('<div class="welcome-header">', unsafe_allow_html=True)
        st.markdown("## 🔐 Authentication Required")
        st.markdown("### Please enter the password to access the chatbot")
        st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    st.markdown('<div class="welcome-header">', unsafe_allow_html=True)
    st.markdown("## 🧠 Mental Health Support Chatbot")
    st.markdown("### I'm here to listen and provide support")
    st.markdown("*Remember: I'm not a replacement for professional therapy*")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.conversation_history:
        for message in st.session_state.conversation_history:
            if message["role"] == "user":
                st.markdown(f'''
                <div class="message-bubble user-message">
                    <strong>💬 You:</strong><br>{message["content"]}
                </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                <div class="message-bubble bot-message">
                    <strong>🤖 Support Bot:</strong><br>{message["content"]}
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.markdown('''
        <div class="message-bubble bot-message">
            <strong>🤖 Support Bot:</strong><br>
            Hello! I'm here to provide emotional support and listen to you. 
            How are you feeling today? This is a safe space to share your thoughts and feelings.
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    user_input = st.text_input(
        "Your message:",
        placeholder="Type your message here... I'm here to listen 💙",
        key="chat_input"
    )
    
    if st.button("📤 Send Message") and user_input:
        st.session_state.conversation_history.append({"role": "user", "content": user_input})
        
        with st.spinner("🤔 Thinking about your message..."):
            response = call_gemini(user_input, st.session_state.conversation_history)
        
        st.session_state.conversation_history.append({"role": "assistant", "content": response})
        
        st.experimental_rerun()

    st.markdown("---")
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("🗑️ Clear Chat"):
            st.session_state.conversation_history = []
            st.success("Chat cleared!")
            time.sleep(1)
            st.experimental_rerun()
    
    with col_btn2:
        if st.button("🔄 Refresh"):
            st.experimental_rerun()
    
    with col_btn3:
        if st.button("📊 Stats"):
            total = len(st.session_state.conversation_history)
            user_msgs = len([m for m in st.session_state.conversation_history if m["role"] == "user"])
            bot_msgs = len([m for m in st.session_state.conversation_history if m["role"] == "assistant"])
            st.info(f"Messages: {total} | You: {user_msgs} | Bot: {bot_msgs}")

    if st.session_state.conversation_history:
        chat_export = "Mental Health Support Chat Export\n"
        chat_export += f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        chat_export += "="*50 + "\n\n"
        
        for msg in st.session_state.conversation_history:
            role = "You" if msg["role"] == "user" else "Support Bot"
            chat_export += f"{role}: {msg['content']}\n\n"
        
        st.download_button(
            label="📝 Download Chat",
            data=chat_export,
            file_name=f"mental_health_chat_{time.strftime('%Y%m%d_%H%M%S')}.txt",
            mime="text/plain"
        )

    with st.expander("💡 Mental Health Tips", expanded=False):
        st.markdown("""
        **Getting Support:**
        - 🗣️ Be open and honest about your feelings
        - ⏰ Take your time to express yourself
        - 💪 Remember that seeking help shows strength
        - 👨‍⚕️ Consider professional therapy for ongoing support
        
        **Self-Care:**
        - 🌱 Practice mindfulness and breathing exercises
        - 💤 Prioritize good sleep habits
        - 🏃‍♀️ Stay physically active
        - 🤝 Connect with supportive people
        """)

    st.markdown("---")
    st.markdown(
        '''
        <div style="text-align: center; padding: 15px; 
             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
             color: white; border-radius: 10px; font-style: italic;">
        💙 This chatbot provides support but is not a substitute for professional mental health care 💙<br>
        <small>If you're experiencing a crisis, please contact emergency services immediately</small>
        </div>
        ''',
        unsafe_allow_html=True
    )