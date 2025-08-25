# chat_backend.py
from typing import List, Dict, Any, Optional
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from backend.evaluation import evaluation_service
from config import llm

class ChatService:
    def __init__(self, document_processor=None):
        self.document_processor = document_processor
        
    def format_messages_to_prompt(self, messages: List[Dict[str, str]]) -> ChatPromptTemplate:
        """メッセージリストをChatPromptTemplateに変換"""
        prompts = []
        for message in messages:
            if message["role"] in ("system", "user"):
                prompts.append(("human", message["content"]))
            elif message["role"] == "assistant":
                prompts.append(("ai", message["content"]))
        
        return ChatPromptTemplate(prompts)
    
    def create_rag_chain(self, retriever):
        """RAGチェーンを作成"""
        def format_docs(docs):
            return "\n\n".join(doc.page_content for doc in docs)
        
        rag_chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | llm
            | StrOutputParser()
        )
        
        return rag_chain
    
    def chat_with_rag(self, messages: List[Dict[str, str]], query: str) -> Dict[str, Any]:
        """RAGを使用してチャット応答を生成"""
        try:
            if not self.document_processor or not self.document_processor.retriever:
                return {
                    "success": False,
                    "message": "ベクトルストアが初期化されていません",
                    "response": None,
                    "context_docs": []
                }
            
            # 関連文書を検索
            context_docs = self.document_processor.search_documents(query, k=3)
            context = "\n\n".join([doc.page_content for doc in context_docs])
            
            # システムプロンプトを作成
            system_message = f"""あなたは質問応答のアシスタントで、質問に対して日本のギャルのように簡単な言葉を使って説明します。絵文字もたくさん使ってください。「ギャル風に答えるね」といった前置きは不要です。いきなりギャルの言葉遣いで回答してください。
            質問に応えるために以下の文脈の情報のみを使用して回答ください。答えがわからない場合はわからないと答えてください。

質問: {query}
文脈: {context}

応答:"""
            
            # メッセージリストにシステムメッセージを追加
            chat_messages = [{"role": "system", "content": system_message}]
            # システムメッセージ以外の過去のメッセージを追加
            chat_messages.extend([msg for msg in messages if msg["role"] != "system"])
            
            # プロンプトを作成
            prompt = self.format_messages_to_prompt(chat_messages)
            
            # LLMで応答生成
            response = llm.invoke(prompt.format_messages())
            ai_response = response.content if hasattr(response, 'content') else str(response)

            # 評価用データを自動収集
            contexts = [doc.page_content for doc in context_docs]
            source_files = list(set([doc.metadata.get('source_file', '不明') for doc in context_docs]))
            
            evaluation_service.add_chat_for_evaluation(
                question=query,
                answer=ai_response,
                contexts=contexts,
                source_files=source_files
            )
            
            return {
                "success": True,
                "message": "応答を正常に生成しました",
                "response": response.content if hasattr(response, 'content') else str(response),
                "context_docs": context_docs,
                "context": context
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"チャット処理中にエラーが発生しました: {str(e)}",
                "response": None,
                "context_docs": []
            }
    
    def chat_without_rag(self, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """RAGを使用せずにチャット応答を生成"""
        try:
            # プロンプトを作成
            # システムプロンプトを作成
            system_message = f"あなたは質問応答のアシスタントで、質問に対して日本のギャルのように簡単な言葉を使って説明します。絵文字もたくさん使ってください。「ギャル風に答えるね」といった前置きは不要です。いきなりギャルの言葉遣いで回答してください。"
            
            # メッセージリストにシステムメッセージを追加
            chat_messages = [{"role": "system", "content": system_message}]
            # システムメッセージ以外の過去のメッセージを追加
            chat_messages.extend([msg for msg in messages if msg["role"] != "system"])
            
            # プロンプトを作成
            prompt = self.format_messages_to_prompt(chat_messages)
            
            # LLMで応答生成
            response = llm.invoke(prompt.format_messages())
            
            return {
                "success": True,
                "message": "応答を正常に生成しました",
                "response": response.content if hasattr(response, 'content') else str(response),
                "context_docs": [],
                "context": ""
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"チャット処理中にエラーが発生しました: {str(e)}",
                "response": None,
                "context_docs": []
            }
    
    def generate_response(self, messages: List[Dict[str, str]], query: str, use_rag: bool = True) -> Dict[str, Any]:
        """統合されたレスポンス生成メソッド"""
        if use_rag and self.document_processor and self.document_processor.get_stats()['has_vectorstore']:
            return self.chat_with_rag(messages, query)
        else:
            return self.chat_without_rag(messages)

# 後方互換性のための関数（既存のchat関数を置き換え）
def chat(messages: List[Dict[str, str]], document_processor=None) -> Dict[str, Any]:
    """後方互換性のためのラッパー関数"""
    chat_service = ChatService(document_processor)
    
    # 最後のユーザーメッセージを取得
    user_messages = [msg for msg in messages if msg["role"] == "user"]
    if not user_messages:
        return {
            "success": False,
            "message": "ユーザーメッセージが見つかりません",
            "response": None
        }
    
    last_query = user_messages[-1]["content"]
    
    return chat_service.generate_response(messages, last_query, use_rag=True)