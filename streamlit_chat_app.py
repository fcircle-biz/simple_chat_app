import streamlit as st
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, AIMessage

st.title("Qwen3:1.7b Chat App")

# Initialize chat model
if "chat" not in st.session_state:
    st.session_state.chat = ChatOllama(model="qwen3:1.7b")

# Initialize messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            with st.expander("Response Details"):
                st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get and stream AI response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # Stream the response
        for chunk in st.session_state.chat.stream([HumanMessage(content=prompt)]):
            full_response += chunk.content
            message_placeholder.markdown(full_response + "▌")
        
        # Remove <think> sections after full response is received
        import re
        cleaned_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL)
        message_placeholder.markdown(cleaned_response)
        st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
    