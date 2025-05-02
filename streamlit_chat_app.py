import streamlit as st
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, AIMessage

from langchain_community.tools.tavily_search import TavilySearchResults
import os

st.title("Qwen3:1.7b Chat App ＋ Web検索")

# 環境変数から Tavily APIキー取得
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    st.error("❌ 環境変数 TAVILY_API_KEY が設定されていません。")
    st.stop()

search = TavilySearchResults(api_key=TAVILY_API_KEY)

# チャットモデル初期化
if "chat" not in st.session_state:
    st.session_state.chat = ChatOllama(model="qwen3:1.7b")

# メッセージ履歴初期化
if "messages" not in st.session_state:
    st.session_state.messages = []

# 🔘 Web検索モードのチェックボックス
web_mode = st.checkbox("🌐 Web検索モード（AIが要約）", value=False)

# メッセージ履歴の表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            with st.expander("Response Details"):
                st.markdown(msg["content"])
        else:
            st.markdown(msg["content"])

# チャット入力
if prompt := st.chat_input("メッセージを入力..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # --- Web検索モードの場合 ---
    if web_mode:
        # ① Tavilyで検索
        search_result = search.run(prompt)

        # ② 検索結果をQwen3に要約依頼
        summarization_prompt = f"次のWeb検索結果をユーザー向けにわかりやすく簡潔に要約してください：\n\n{search_result}"
        message_placeholder = st.empty()
        full_summary = ""

        for chunk in st.session_state.chat.stream([HumanMessage(content=summarization_prompt)]):
            full_summary += chunk.content
            message_placeholder.markdown(full_summary + "▌")

        import re
        cleaned_summary = re.sub(r'<think>.*?</think>', '', full_summary, flags=re.DOTALL)
        message_placeholder.markdown(cleaned_summary)

        st.session_state.messages.append({"role": "assistant", "content": cleaned_summary})

    else:
        # --- 通常のAIチャット処理 ---
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""

            for chunk in st.session_state.chat.stream([HumanMessage(content=prompt)]):
                full_response += chunk.content
                message_placeholder.markdown(full_response + "▌")

            import re
            cleaned_response = re.sub(r'<think>.*?</think>', '', full_response, flags=re.DOTALL)
            message_placeholder.markdown(cleaned_response)

            st.session_state.messages.append({"role": "assistant", "content": cleaned_response})
