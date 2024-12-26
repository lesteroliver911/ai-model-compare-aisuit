import streamlit as st
import aisuite as ai
import os
import groq
from dotenv import load_dotenv

# Initialize clients
@st.cache_resource
def get_clients():
    ai_client = ai.Client()
    groq_client = groq.Client()
    return ai_client, groq_client

# Load environment variables
load_dotenv()

# Page config - Remove title from main area
st.set_page_config(
    page_title="AI Model Comparison",
    page_icon="🤖",
    layout="wide"
)

# Add custom CSS with improved styling
st.markdown("""
    <style>
    .stTextArea textarea {min-height: 150px;}
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.8rem;
        margin-bottom: 1rem;
        border: 1px solid #ddd;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #f0f2f6;
        color: #000000;
        margin-left: 20px;
        margin-right: 20px;
    }
    .openai-message {
        background-color: #e7f7e7;
        color: #000000;
    }
    .anthropic-message {
        background-color: #e6f3ff;
        color: #000000;
    }
    .groq-message {
        background-color: #fff3e6;
        color: #000000;
    }
    .model-name {
        font-size: 1.1em;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    .divider {
        margin: 1.5rem 0;
        border-bottom: 1px solid #eee;
    }
    .settings-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Sidebar with title and all controls
with st.sidebar:
    # Move main title to sidebar
    st.title("🤖 AI Model Comparison")
    st.markdown("Compare responses from different AI models")
    
    # Add attribution
    st.markdown("""
        <div style='font-size: 0.8em; color: #666;'>
        Powered by <a href='https://github.com/andrewyng/aisuite' target='_blank'>AISuite</a> library by Andrew Ng
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")  # Divider
    
    st.header("⚙️ Settings")
    
    with st.expander("Model Configuration", expanded=True):
        # Temperature slider with better formatting
        st.markdown("##### Temperature Control")
        temperature = st.slider(
            "Adjust randomness",
            min_value=0.0,
            max_value=1.0,
            value=0.75,
            step=0.01,
            help="Higher values make the output more random, lower values make it more focused"
        )
        
        # System message input with better formatting
        st.markdown("##### System Message")
        system_message = st.text_area(
            "Set AI behavior",
            value="Respond in Pirate English.",
            help="Define how the AI models should behave"
        )
    
    # Clear chat button with confirmation
    st.markdown("##### Chat Management")
    if st.button("🗑️ Clear Chat History", type="secondary"):
        if st.session_state.messages:
            if st.button("⚠️ Confirm Clear"):
                st.session_state.messages = []
                st.rerun()
    
    # Move footer to sidebar bottom
    st.markdown("---")
    st.caption("AI Model Comparison Tool v1.0")

# Main chat interface - Now only contains chat and results
chat_container = st.container()

# User input with placeholder
user_input = st.chat_input("Ask something to compare AI responses...")

# Initialize clients
ai_client, groq_client = get_clients()

# Models including Groq
models = [
    "openai:gpt-4o",
    "anthropic:claude-3-5-sonnet-20240620",
    "llama3-8b-8192"  # Groq model
]

# Process user input
if user_input:
    # Add user message to state
    st.session_state.messages.append({
        "role": "user", 
        "content": user_input,
        "responses": {}
    })
    
    # Prepare messages for API
    api_messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": user_input}
    ]
    
    # Get responses from all models
    for model in models:
        try:
            with st.spinner(f"Getting response from {model.split(':')[0].title()}..."):
                if "llama" in model:  # Groq model
                    response = groq_client.chat.completions.create(
                        model=model,
                        messages=api_messages,
                        temperature=temperature
                    )
                else:  # OpenAI or Anthropic models
                    response = ai_client.chat.completions.create(
                        model=model,
                        messages=api_messages,
                        temperature=temperature
                    )
                st.session_state.messages[-1]["responses"][model] = response.choices[0].message.content
                
        except Exception as e:
            st.error(f"Error with {model}: {str(e)}")
            st.session_state.messages[-1]["responses"][model] = f"Error: {str(e)}"

# Display chat history with improved formatting
with chat_container:
    for message in st.session_state.messages:
        # User message
        st.markdown(f"""
            <div class="chat-message user-message">
                <div class="model-name">👤 You</div>
                {message["content"]}
            </div>
            """, unsafe_allow_html=True)
        
        # Model responses in columns
        cols = st.columns(3)
        for col, (model, response) in zip(cols, message["responses"].items()):
            model_name = model.split(':')[0].title() if ':' in model else 'Groq'
            with col:
                st.markdown(f"""
                    <div class="chat-message {model_name.lower()}-message">
                        <div class="model-name">🤖 {model_name}</div>
                        {response}
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
