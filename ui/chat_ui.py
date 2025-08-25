# chat_ui.py
import streamlit as st
from typing import List, Dict, Any
from backend.chat import ChatService

class ChatUI:
    def __init__(self, document_processor=None):
        self.chat_service = ChatService(document_processor)
        self.document_processor = document_processor
    
    def initialize_session_state(self):
        """セッション状態を初期化"""
        if "messages" not in st.session_state:
            st.session_state.messages = []
        if "show_context" not in st.session_state:
            st.session_state.show_context = False
    
    def display_chat_messages(self):
        """過去のチャットメッセージを表示"""
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
    
    def display_context_documents(self, context_docs: List, context: str):
        """参照した文書を表示"""
        if context_docs and st.session_state.get("show_context", False):
            with st.expander("📚 参考にした資料だよ〜", expanded=False):
                for i, doc in enumerate(context_docs):
                    st.write(f"**資料 {i+1}** (出典: {doc.metadata.get('source_file', '不明')})")
                    # 文書の内容を表示（長すぎる場合は切り詰める）
                    content = doc.page_content
                    if len(content) > 500:
                        content = content[:500] + "..."
                    st.write(content)
                    if i < len(context_docs) - 1:
                        st.divider()
    
    def handle_user_input(self, prompt: str):
        """ユーザー入力を処理"""
        # ユーザーメッセージをチャット履歴に追加
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # AIの応答を生成
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            
            try:
                # チャットサービスで応答を生成
                result = self.chat_service.generate_response(
                    st.session_state.messages, 
                    prompt, 
                    use_rag=True
                )
                
                if result["success"]:
                    ai_response = result["response"]
                    
                    # 応答を表示
                    message_placeholder.markdown(ai_response)
                    
                    # AIの応答をチャット履歴に追加
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": ai_response
                    })
                    
                    # 参照文書を表示
                    self.display_context_documents(
                        result.get("context_docs", []), 
                        result.get("context", "")
                    )
                    
                else:
                    error_message = f"あれれ〜エラーが起きちゃった💦: {result['message']}"
                    message_placeholder.error(error_message)
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": error_message
                    })
                    
            except Exception as e:
                error_message = f"うーん、なんか変だよ〜😅: {str(e)}"
                message_placeholder.error(error_message)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": error_message
                })
    
    def render_chat_controls(self):
        """チャット制御UI"""
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col1:
            if st.button("🗑️ 履歴リセット♪", help="チャット履歴をリセットするよ〜"):
                st.session_state.messages = []
                st.rerun()
        
        with col2:
            st.session_state.show_context = st.checkbox(
                "📚 参考資料も見る？", 
                value=st.session_state.get("show_context", False),
                help="AIが参考にした資料も一緒に表示するよ💕"
            )
    
    def render_chat_status(self):
        """チャットの状態を表示"""
        if self.document_processor:
            stats = self.document_processor.get_stats()
            if stats['has_vectorstore']:
                st.success(f"✨ スマートモード: {stats['total_files']}個のファイルを参照中💎")
            else:
                st.warning("💭 ノーマルモード: 資料なしでお話し中")
        else:
            st.warning("💭 ノーマルモード: 資料なしでお話し中")
    
    def render_chat(self):
        """チャットタブ全体をレンダリング"""
        st.header("💬 おしゃべりしよ〜🦄")
        
        # セッション状態を初期化
        self.initialize_session_state()
        
        # チャット状態を表示
        self.render_chat_status()
        
        # チャット制御
        self.render_chat_controls()
        
        st.divider()
        
        # 過去のメッセージを表示
        if not st.session_state.messages:
            st.info("💕 なんでも聞いてね〜！資料をアップしてたらそれも参考にするよ✨")
        
        self.display_chat_messages()
        
        # ユーザー入力を処理
        if prompt := st.chat_input("なんでも聞いて〜💖"):
            self.handle_user_input(prompt)

def render_chat_with_processor(document_processor=None):
    """ドキュメントプロセッサーを使用してチャットタブをレンダリング"""
    chat_ui = ChatUI(document_processor)
    chat_ui.render_chat()