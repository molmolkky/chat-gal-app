# upload_ui.py
import streamlit as st
from backend.upload import document_processor

def render_upload():
    """アップロードタブのUIをレンダリング"""
    st.header("📚 資料アップしちゃお〜🧚‍♀️")
    
    # 既存の資料表示
    show_existing_documents()
    
    st.divider()
    
    # PDFアップロード機能
    upload_pdf_section()
    
    st.divider()
    
    # データベース管理
    database_management_section()

def show_existing_documents():
    """既存のドキュメント一覧を表示"""
    st.subheader("💎 今持ってる資料たち")
    
    stats = document_processor.get_stats()
    
    if stats['has_vectorstore'] and stats['total_files'] > 0:
        st.success(f"✨ {stats['total_files']}個のファイルがあるよ〜")
        
        # ファイル詳細を表示
        with st.expander("📄 詳しい情報見る？💅"):
            for file_info in stats['processed_files']:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    st.write(f"📄 **{file_info['name']}**")
                with col2:
                    st.write(f"{file_info['pages']} ページ")
                with col3:
                    st.write(f"{file_info['size']:,} bytes")
        
        st.info("💬 チャットで質問してみて〜")
    else:
        st.info("📝 まだ資料がないよ〜。アップしてみて💕")

def upload_pdf_section():
    """PDFアップロードセクション"""
    st.subheader("📄 PDF資料をアップロード✨")
    
    # ファイルアップローダー
    uploaded_files = st.file_uploader(
        "PDFファイルを選んでね〜",
        type=['pdf'],
        accept_multiple_files=True,
        help="複数のPDFを一度にアップできるよ💖"
    )
    
    if uploaded_files:
        st.write(f"選んだファイル: {len(uploaded_files)}個 🎉")
        
        # アップロードされたファイルの一覧表示
        for file in uploaded_files:
            st.write(f"- {file.name} ({file.size:,} bytes)")
        
        # 処理ボタン
        if st.button("🚀 アップロード開始！", type="primary"):
            process_uploaded_files(uploaded_files)

def process_uploaded_files(uploaded_files):
    """アップロードされたファイルを処理"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    def progress_callback(message):
        status_text.text(message)
    
    try:
        # ファイル処理
        result = document_processor.process_uploaded_files(
            uploaded_files, 
            progress_callback
        )
        
        progress_bar.progress(1.0)
        
        if result['success']:
            status_text.text("✅ 完了〜！")
            st.success(f"🎉 {result['message']}")
            st.info(f"📊 全部で{result['chunk_count']}個のチャンクに分けたよ〜")
            
            # 処理されたファイルの詳細表示
            with st.expander("📋 処理の詳細💅"):
                for file_info in result['file_info']:
                    st.write(f"**{file_info['name']}**: {file_info['pages']} ページ")
            
            # セッション状態を更新してチャットで使用できるようにする
            st.session_state.vectorstore_ready = True
            
        else:
            status_text.text("❌ あれれ〜エラーだよ")
            st.error(f"❌ {result['message']}")
            
    except Exception as e:
        st.error(f"❌ なんか変なエラーが起きちゃった💦: {str(e)}")
        status_text.text("エラーが発生しました")

def database_management_section():
    """データベース管理セクション"""
    st.subheader("🗑️ 資料の管理")
    
    stats = document_processor.get_stats()
    
    if stats['has_vectorstore']:
        st.warning("⚠️ 下のボタンを押すと、全部の資料が消えちゃうよ〜")
        
        if st.button("🚨 全部削除しちゃう", type="secondary"):
            if st.checkbox("本当に消しちゃう？元に戻せないよ〜💦"):
                try:
                    document_processor.clear_vectorstore()
                    
                    # セッション状態も更新
                    if "vectorstore_ready" in st.session_state:
                        del st.session_state.vectorstore_ready
                    
                    st.success("✅ 全部消したよ〜")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ 削除できなかった💦: {str(e)}")
    else:
        st.info("消す資料がないよ〜")