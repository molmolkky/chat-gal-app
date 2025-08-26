# upload.py
import time
import tempfile
import os
import uuid
import streamlit as st
from typing import List, Optional
from datetime import datetime, timedelta
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.schema import Document

from config_manager import config_manager

class DocumentProcessor:
    def __init__(self):
        # セッションIDを生成（より確実な分離のため）
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        
        # セッション開始時刻を記録（タイムアウト管理用）
        if 'session_start' not in st.session_state:
            st.session_state.session_start = datetime.now()
        
        # ベクトルストアをセッション状態で管理
        if 'vectorstore' not in st.session_state:
            st.session_state.vectorstore = None
        if 'retriever' not in st.session_state:
            st.session_state.retriever = None
        if 'processed_files' not in st.session_state:
            st.session_state.processed_files = []
        
        # セッションタイムアウトチェック（オプション）
        self._check_session_timeout()
    
    def _check_session_timeout(self, timeout_hours=2):
        """セッションタイムアウトをチェック"""
        if st.session_state.session_start:
            elapsed = datetime.now() - st.session_state.session_start
            if elapsed > timedelta(hours=timeout_hours):
                # タイムアウト時にデータをクリア
                self.clear_vectorstore()
                st.session_state.session_start = datetime.now()
                st.warning("⏰ セッションがタイムアウトしました。セキュリティのためデータをクリアしたよ〜")
    
    def get_session_info(self):
        """セッション情報を取得（デバッグ用）"""
        return {
            'session_id': st.session_state.get('session_id', 'Unknown'),
            'session_start': st.session_state.get('session_start'),
            'has_data': st.session_state.vectorstore is not None,
            'file_count': len(st.session_state.processed_files)
        }
        
    def initialize_vectorstore(self):
        """ベクトルストアを初期化"""
        embedding = config_manager.get_embedding()
        if not embedding:
            raise ValueError("Embedding model is not configured")
        
        st.session_state.vectorstore = InMemoryVectorStore(embedding)
        st.session_state.retriever = st.session_state.vectorstore.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": 10,
                "score_threshold": 0.3
            }
        )
    
    def load_pdf(self, uploaded_file) -> List[Document]:
        """PDFファイルを読み込んでDocumentオブジェクトのリストを返す"""
        # 一時ファイルとして保存
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        try:
            # PDFを読み込み
            loader = PyPDFLoader(tmp_file_path)
            documents = loader.load()
            
            # ドキュメントにメタデータを追加
            for doc in documents:
                doc.metadata['source_file'] = uploaded_file.name
                doc.metadata['file_size'] = uploaded_file.size
                doc.metadata['session_id'] = st.session_state.session_id  # セッションIDを追加
            
            return documents
            
        finally:
            # 一時ファイルを削除
            os.unlink(tmp_file_path)
    
    def split_documents(self, documents: List[Document]) -> List[Document]:
        """ドキュメントを分割"""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        return text_splitter.split_documents(documents)
    
    def add_documents_to_vectorstore(self, split_docs: List[Document], progress_callback=None):
        """ドキュメントをベクトルストアに追加（バッチ処理）"""
        if not st.session_state.retriever:
            self.initialize_vectorstore()
        
        tmp_list = []
        c = 0
        limit_c = 100000
        total_docs = len(split_docs)
        
        for i, doc in enumerate(split_docs):
            c += len(doc.page_content)
            tmp_list.append(doc)
            
            if c > limit_c or i + 1 == total_docs:
                if progress_callback:
                    progress_callback(f"Adding {i+1} documents of {total_docs} to retriever")
                
                try:
                    st.session_state.retriever.add_documents(tmp_list)
                except Exception as e:
                    if '429' in str(e):
                        if progress_callback:
                            progress_callback("Rate limit exceeded, waiting 60 seconds...")
                        time.sleep(60)
                        st.session_state.retriever.add_documents(tmp_list)
                    else:
                        raise e
                
                tmp_list = []
                c = 0
    
    def process_uploaded_files(self, uploaded_files, progress_callback=None) -> dict:
        """アップロードされたファイルを処理"""
        try:
            all_documents = []
            file_info = []
            
            # 各PDFファイルを処理
            for i, uploaded_file in enumerate(uploaded_files):
                if progress_callback:
                    progress_callback(f"Processing: {uploaded_file.name}")
                
                # PDFを読み込み
                documents = self.load_pdf(uploaded_file)
                all_documents.extend(documents)
                
                file_info.append({
                    'name': uploaded_file.name,
                    'size': uploaded_file.size,
                    'pages': len(documents)
                })
            
            if all_documents:
                # テキストを分割
                if progress_callback:
                    progress_callback("Splitting documents...")
                
                splits = self.split_documents(all_documents)
                
                # ベクトルDBに格納
                if progress_callback:
                    progress_callback("Adding to vector database...")
                
                self.add_documents_to_vectorstore(splits, progress_callback)
                
                # 処理済みファイル情報をセッション状態に保存
                st.session_state.processed_files.extend(file_info)
                
                return {
                    'success': True,
                    'message': f'Successfully processed {len(uploaded_files)} PDF files',
                    'file_count': len(uploaded_files),
                    'chunk_count': len(splits),
                    'file_info': file_info
                }
            else:
                return {
                    'success': False,
                    'message': 'No documents found in uploaded files'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Error processing files: {str(e)}'
            }
    
    def search_documents(self, query: str, k: int = 3) -> List[Document]:
        """ドキュメントを検索"""
        if not st.session_state.retriever:
            return []
        
        try:
            return st.session_state.retriever.invoke(query)
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def get_context_from_search(self, query: str, k: int = 3) -> str:
        """検索結果から文脈を取得"""
        docs = self.search_documents(query, k)
        return "\n".join([doc.page_content for doc in docs])
    
    def clear_vectorstore(self):
        """ベクトルストアをクリア"""
        st.session_state.vectorstore = None
        st.session_state.retriever = None
        st.session_state.processed_files = []
    
    def get_stats(self) -> dict:
        """統計情報を取得"""
        return {
            'has_vectorstore': st.session_state.vectorstore is not None,
            'processed_files': st.session_state.processed_files,
            'total_files': len(st.session_state.processed_files)
        }

# グローバルインスタンス
document_processor = DocumentProcessor()