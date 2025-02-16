import streamlit as st
import requests
from MagicConvert import MagicConvert
import re

def clean_text_for_markdown(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&nbsp;', ' ')
    text = text.replace('&quot;', '"')
    text = text.replace('&amp;', '&')
    text = text.replace('\n', '\n\n')
    return text

def create_streamlit_ppt_chat():
    
    st.set_page_config(
        page_title="PPT Chat Assistant",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    st.markdown("""
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] {
            min-width: 600px;
            max-width: 800px;
        }
        [data-testid="stSidebar"][aria-expanded="false"] {
            min-width: 0px;
            max-width: 0px;
        }
        [data-testid="stSidebar"] {
            transition: all 0.3s ease-in-out;
        }
        .main {
            padding: 2rem;
        }
        .message-container {
            display: flex;
            flex-direction: column;
            margin-bottom: 15px;
            max-width: 90%;
            }
        .message-bubble {
            padding: 12px 18px;
            border-radius: 12px;
            margin: 5px;
            line-height: 1.5;
            border: 1px solid var(--st-color-border-light);
        }
        .user-message {
            align-self: flex-end;
            background-color: #4A90E2;
            color: #FFFFFF;
            border-radius: 12px;
            padding: 10px 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1); 
            max-width: 80%; 
            font-size: 14px; 
            line-height: 1.4; 
        }
        .bot-message {
            align-self: flex-start;
            background-color: var(--st-color-secondary-light);
            color: var(--st-color-text);
        }
        .input-container {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            padding: 1rem;
            border-top: 1px solid var(--st-color-border-light);
            z-index: 1000;
            transition: all 0.3s ease-in-out;
        }
        .upload-section {
            background-color: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .stTextInput {
            border-radius: 8px;
            margin-bottom: 1rem;
            margin-left: 2rem;
        }
        .sidebar .stSelectbox {
            margin-bottom: 1rem;
        }
        div[data-testid="stHorizontalBlock"]:last-of-type {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background-color: var(--st-color-background);
            padding: 10px 2rem;
            z-index: 1000;
            box-shadow: 0px -2px 5px rgba(0,0,0,0.1);
            transition: none; /* Remove transition */
        }     
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main div[data-testid="stHorizontalBlock"]:last-of-type {
            left: 600px;
        }       
        .main .block-container {
            max-width: 100%;
            padding-left: 2rem;
            padding-right: 2rem;
            padding-top: 4rem;
            padding-bottom: 120px;
            transition: all 0.3s ease-in-out;
        }        
        .stTextInput input {
            border-radius: 4px;
            border: 1px solid #e5e7eb;
        }
        div[data-testid="stHorizontalBlock"]:last-of-type {
            background-color: var(--st-color-background);
            box-shadow: 0px -2px 5px var(--st-color-shadow);
        }
        .stTitle {
            font-size: 2rem;
            font-weight: 600;
            text-align: center;
            position: fixed !important;
            top: 0;
            left: 0;
            right: 0;
            background-color: rgb(0, 92, 222) !important;
            color: white;    
            padding-top: 3rem;
            margin: 0;
            z-index: 1000;
            border-bottom: 1px solid var(--border-color);
        }
        .stTitle h1 {
            color: var(--heading-color) !important;
            padding-bottom: 0.5rem;
        }
        [data-testid="stSidebar"][aria-expanded="true"] ~ .main .stTitle {
            left: 600px;
        }
        .stButton {
            display: inline-flex;
            justify-content: center;
        }
        .stButton button {
            margin-left: 0.5rem;
            margin-right: 0.5rem;
            margin-top: 3.70rem;
            border-radius: 8px;
            margin-bottom: 1rem;
            margin-left: 2rem;
            background-color: #0ea5e9;
            color: white;
        }
        .stTextArea textarea {
            resize: vertical !important;
            min-height: 80px !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('''
    <div class="stTitle">
        <h1>🎯 PowerPoint Chat Assistant Using MagicConvert</h1>
    </div>''', unsafe_allow_html=True)

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'slides_dict' not in st.session_state:
        st.session_state.slides_dict = {}
    if 'selected_slide' not in st.session_state:
        st.session_state.selected_slide = None
    if 'send_button_clicked' not in st.session_state:
        st.session_state.send_button_clicked = False
    if 'user_question' not in st.session_state:
        st.session_state.user_question = ""

    with st.sidebar:
        st.markdown("### 📤 Upload Presentation")
        uploaded_file = st.file_uploader("Upload your PowerPoint presentation", type=['pptx'])
        
        if uploaded_file:
            with open("temp.pptx", "wb") as f:
                f.write(uploaded_file.getvalue())
            
            converter = MagicConvert()
            result = converter.magic("temp.pptx")
            
            slides_dict = {}
            slide_content = result.get_text.split("\n\n")
            for slide in slide_content:
                if slide.startswith("<!-- Slide number:"):
                    slide_number = slide.split(":")[1].split("-->")[0].strip()
                    slide_text = slide.split("\n", 1)[1]
                    slides_dict[f"{slide_number}"] = clean_text_for_markdown(slide_text.strip())
            
            st.session_state.slides_dict = slides_dict
        
        st.markdown("### 📑 Slide Navigator")
        if st.session_state.slides_dict:
            st.session_state.selected_slide = st.selectbox(
                "Select Slide Number",
                options=list(st.session_state.slides_dict.keys()),
                format_func=lambda x: f"Slide {x}"
            )
            
            st.markdown("#### Current Slide Content")
            st.markdown(st.session_state.slides_dict[st.session_state.selected_slide])
    chat_container = st.container()
    with chat_container:
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for chat in st.session_state.chat_history:
            st.markdown(f"""
                <div class="message-container">
                    <div class="message-bubble user-message">{chat["question"]}</div>
                    <div class="message-bubble bot-message">{chat["answer"]}</div>
                </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    spinner_container = st.container()    
    footer_cols = st.columns([6, 0.6, 0.6])

    def send_message():
        if st.session_state.slides_dict and st.session_state.selected_slide:
            with spinner_container:
                with st.spinner("Processing..."):
                    response = send_message_openrouter(
                        prompt=st.session_state.user_question,
                        source=st.session_state.slides_dict[st.session_state.selected_slide]
                    )
                    st.session_state.chat_history.append({
                        "question": st.session_state.user_question,
                        "answer": response
                    })
        st.session_state.user_question = ""
        
    with footer_cols[0]:
        user_question = st.text_area(
            label="",
            placeholder="Type your message here... (Press Enter to send)",
            key="user_question",
            height=80,
            max_chars=1000,
            value=st.session_state.user_question,
        )
    with footer_cols[1]:
        send_button = st.button("Send", key="send_button", on_click=send_message) 
    with footer_cols[2]:
        clear_button = st.button("Clear", key="clear_button")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()

key = "9f6e5a29-025a-4160-9324-0f4bfb1ec328"

def send_message_openrouter(prompt, source):
    endpoint = "https://api.sambanova.ai/v1/chat/completions"
    data = {
        "stream": False,
        "model": "Meta-Llama-3.3-70B-Instruct",
        "messages": [
            {
                "role": "system",
                "content": source
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    headers = {
        "Authorization": f"Bearer {st.secrets['SAMBANOVA_API_KEY']}",
        "Content-Type": "application/json"
    }
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content']
    else:
        return f"Error: {response.status_code} - {response.text}"

if __name__ == "__main__":
    create_streamlit_ppt_chat()