# config_manager.py
import streamlit as st
from langchain_openai import AzureOpenAIEmbeddings, AzureChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()

class ConfigManager:
    def __init__(self):
        self.embedding = None
        self.llm = None
    
    def render_sidebar_config(self):
        """サイドバーに設定UIを表示"""
        st.sidebar.header("🔧 Azure OpenAI設定")
        
        # 設定方法の選択
        config_method = st.sidebar.radio(
            "設定方法を選んでね〜💕",
            ["環境変数から読み込み", "手動で入力"],
            help="環境変数(.env)があれば自動で読み込むよ〜"
        )
        
        if config_method == "環境変数から読み込み":
            return self._load_from_env()
        else:
            return self._load_from_sidebar()
    
    def _load_from_env(self):
        """環境変数から設定を読み込み"""
        try:
            required_vars = [
                "AZURE_OPENAI_EMBEDDING_ENDPOINT",
                "AZURE_OPENAI_EMBEDDING_API_KEY",
                "AZURE_OPENAI_EMBEDDING_API_VERSION",
                "AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME",
                "AZURE_OPENAI_CHAT_ENDPOINT",
                "AZURE_OPENAI_CHAT_API_KEY",
                "AZURE_OPENAI_CHAT_API_VERSION",
                "AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"
            ]
            
            missing_vars = [var for var in required_vars if not os.environ.get(var)]
            
            if missing_vars:
                st.sidebar.error(f"❌ 環境変数が足りないよ〜: {', '.join(missing_vars)}")
                return False
            
            self.embedding = AzureOpenAIEmbeddings(
                azure_endpoint=os.environ["AZURE_OPENAI_EMBEDDING_ENDPOINT"],
                api_key=os.environ["AZURE_OPENAI_EMBEDDING_API_KEY"],
                api_version=os.environ["AZURE_OPENAI_EMBEDDING_API_VERSION"],
                azure_deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"],
                model=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME"]
            )
            
            self.llm = AzureChatOpenAI(
                azure_endpoint=os.environ["AZURE_OPENAI_CHAT_ENDPOINT"],
                api_key=os.environ["AZURE_OPENAI_CHAT_API_KEY"],
                api_version=os.environ["AZURE_OPENAI_CHAT_API_VERSION"],
                azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
                model=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
                temperature=0
            )
            
            st.sidebar.success("✅ 環境変数から読み込み完了〜")
            return True
            
        except Exception as e:
            st.sidebar.error(f"❌ 環境変数の読み込みエラー: {str(e)}")
            return False
    
    def _load_from_sidebar(self):
        """サイドバーから手動入力で設定"""
        st.sidebar.subheader("📝 Embedding設定")
        
        # セッション状態で入力値を保持
        if "azure_config" not in st.session_state:
            st.session_state.azure_config = {}
        
        # Embedding設定
        embedding_endpoint = st.sidebar.text_input(
            "Embedding Endpoint",
            value=st.session_state.azure_config.get("embedding_endpoint", ""),
            type="password",
            help="Azure OpenAI Embeddingのエンドポイント"
        )
        
        embedding_api_key = st.sidebar.text_input(
            "Embedding API Key",
            value=st.session_state.azure_config.get("embedding_api_key", ""),
            type="password",
            help="Azure OpenAI EmbeddingのAPIキー"
        )
        
        embedding_api_version = st.sidebar.text_input(
            "Embedding API Version",
            value=st.session_state.azure_config.get("embedding_api_version", ""),
            help="APIバージョン（例: 2024-02-01）"
        )
        
        embedding_deployment = st.sidebar.text_input(
            "Embedding Deployment Name",
            value=st.session_state.azure_config.get("embedding_deployment", ""),
            help="Embeddingモデルのデプロイメント名"
        )
        
        st.sidebar.subheader("💬 Chat設定")
        
        # Chat設定
        chat_endpoint = st.sidebar.text_input(
            "Chat Endpoint",
            value=st.session_state.azure_config.get("chat_endpoint", ""),
            type="password",
            help="Azure OpenAI Chatのエンドポイント"
        )
        
        chat_api_key = st.sidebar.text_input(
            "Chat API Key",
            value=st.session_state.azure_config.get("chat_api_key", ""),
            type="password",
            help="Azure OpenAI ChatのAPIキー"
        )
        
        chat_api_version = st.sidebar.text_input(
            "Chat API Version",
            value=st.session_state.azure_config.get("chat_api_version", ""),
            help="APIバージョン（例: 2024-02-01）"
        )
        
        chat_deployment = st.sidebar.text_input(
            "Chat Deployment Name",
            value=st.session_state.azure_config.get("chat_deployment", ""),
            help="Chatモデルのデプロイメント名"
        )
        
        # 設定を保存
        st.session_state.azure_config.update({
            "embedding_endpoint": embedding_endpoint,
            "embedding_api_key": embedding_api_key,
            "embedding_api_version": embedding_api_version,
            "embedding_deployment": embedding_deployment,
            "chat_endpoint": chat_endpoint,
            "chat_api_key": chat_api_key,
            "chat_api_version": chat_api_version,
            "chat_deployment": chat_deployment
        })
        
        # 接続テストボタン
        if all(var for var in st.session_state.azure_config.values()):
            if st.sidebar.button("🔌 接続テスト", type="primary"):
                return self._test_connection()
        
        # 全ての必須フィールドが入力されているかチェック
        required_fields = [
            embedding_endpoint, embedding_api_key, embedding_deployment,
            chat_endpoint, chat_api_key, chat_deployment
        ]
        
        if all(field.strip() for field in required_fields):
            try:
                self.embedding = AzureOpenAIEmbeddings(
                    azure_endpoint=embedding_endpoint,
                    api_key=embedding_api_key,
                    api_version=embedding_api_version,
                    azure_deployment=embedding_deployment,
                    model=embedding_deployment
                )
                
                self.llm = AzureChatOpenAI(
                    azure_endpoint=chat_endpoint,
                    api_key=chat_api_key,
                    api_version=chat_api_version,
                    azure_deployment=chat_deployment,
                    model=chat_deployment,
                    temperature=0
                )
                
                st.sidebar.success("✅ テストしてみて〜")
                return True
                
            except Exception as e:
                st.sidebar.error(f"❌ 設定エラー: {str(e)}")
                return False
        else:
            st.sidebar.warning("⚠️ 全ての項目を入力してね〜")
            return False
    
    def _test_connection(self):
        """接続テスト"""
        try:
            config = st.session_state.azure_config
            
            # Embeddingテスト
            test_embedding = AzureOpenAIEmbeddings(
                azure_endpoint=config["embedding_endpoint"],
                api_key=config["embedding_api_key"],
                api_version=config["embedding_api_version"],
                azure_deployment=config["embedding_deployment"],
                model=config["embedding_deployment"]
            )
            
            # LLMテスト
            test_llm = AzureChatOpenAI(
                azure_endpoint=config["chat_endpoint"],
                api_key=config["chat_api_key"],
                api_version=config["chat_api_version"],
                azure_deployment=config["chat_deployment"],
                model=config["chat_deployment"],
                temperature=0
            )
            
            # 簡単なテスト実行
            with st.spinner("接続テスト中..."):
                # Embeddingテスト
                test_embedding.embed_query("test")
                
                # LLMテスト
                test_llm.invoke("Hello")
            
            st.sidebar.success("🎉 接続テスト成功〜！")
            
            # 成功したら設定を保存
            self.embedding = test_embedding
            self.llm = test_llm
            
            return True
            
        except Exception as e:
            st.sidebar.error(f"❌ 接続テスト失敗: {str(e)}")
            return False
    
    def is_configured(self):
        """設定が完了しているかチェック"""
        return self.embedding is not None and self.llm is not None
    
    def get_embedding(self):
        """Embeddingインスタンスを取得"""
        return self.embedding
    
    def get_llm(self):
        """LLMインスタンスを取得"""
        return self.llm

# グローバルインスタンス
config_manager = ConfigManager()