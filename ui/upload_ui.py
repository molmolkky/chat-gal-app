# upload_ui.py
import streamlit as st
from backend.upload import document_processor

def render_upload():
    """アップロードタブのUIをレンダリング"""
    st.header("📚 資料アップしちゃお〜🧚‍♀️")

    info_col, upload_col = st.columns(2)
    with info_col:
        # プライバシー情報を表示
        show_privacy_info()
        show_usage_guidelines()
    
    with upload_col:
        # PDFアップロード機能
        upload_pdf_section()
    
    st.divider()
    exist_col, manage_col = st.columns(2)

    with exist_col:
        # 既存の資料表示
        show_existing_documents()
    
    with manage_col:
        # データベース管理
        database_management_section()

def show_privacy_info():
    """プライバシー情報を表示"""
    with st.expander("🔒 プライバシーとセキュリティについて"):
        st.write("""
        **あなたの資料は安全だよ〜💕**
        
        ✅ **完全にプライベート**
        - アップロードした資料は、あなたのブラウザセッションでのみ利用
        - 他のユーザーからは絶対に見えません
        
        ✅ **サーバーに保存されない**
        - ファイルはメモリ内でのみ処理され、ディスクに保存されません
        - ブラウザを閉じると自動的に削除されます
        
        ✅ **一時的な利用**
        - データは永続化されないため、長期間残ることはありません
        - セッション終了と同時に完全に消去されます
        
        ⚠️ **注意事項**
        - 同じブラウザの複数タブでは同じデータが共有されます
        - 公共のPCでは使用後にブラウザを完全に閉じてください
        - 機密性の高い文書は、信頼できる環境でのみご利用ください
        """)

def show_usage_guidelines():
    """使用ガイドラインを表示"""
    st.info("""
    📋 **安全な使い方のコツ**
    
    1. **個人デバイスでの利用推奨** 📱
    
        自分のPC・スマホからアクセスしてね
    
    2. **使用後はブラウザを閉じる** 🚪
    
        データが確実に削除されるよ
    
    3. **大切な資料の取り扱い** 💎
    
        超機密文書は避けて、一般的な資料で試してみて

    """)

def show_existing_documents():
    """既存のドキュメント一覧を表示"""
    st.subheader("💎 今持ってる資料たち")
    
    stats = document_processor.get_stats()
    
    if stats['processed_files'] and stats['total_files'] > 0:
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
    
    if stats['processed_files']:
        st.warning("⚠️ 下のボタンを押すと、全部の資料が消えちゃうよ〜")

        # セッション状態で削除確認フラグを管理
        if "show_delete_confirmation" not in st.session_state:
            st.session_state.show_delete_confirmation = False
        
        # 削除ボタン
        if st.button("🚨 全部削除しちゃう", type="secondary"):
            st.session_state.show_delete_confirmation = True
            st.rerun()
        # 確認が表示されている場合
        if st.session_state.show_delete_confirmation:
            st.error("⚠️ 本当に全ての資料を削除しますか？この操作は取り消せません！")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ はい、削除します", type="primary", key="confirm_delete"):
                    try:
                        document_processor.clear_vectorstore()
                        
                        # セッション状態も更新
                        if "vectorstore_ready" in st.session_state:
                            del st.session_state.vectorstore_ready
                        
                        # 確認フラグをリセット
                        st.session_state.show_delete_confirmation = False
                        
                        st.success("✅ 全部消したよ〜")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ 削除できなかった💦: {str(e)}")
                        st.session_state.show_delete_confirmation = False
            
            with col2:
                if st.button("❌ やっぱりやめる", key="cancel_delete"):
                    st.session_state.show_delete_confirmation = False
                    st.rerun()
    else:
        st.info("消す資料がないよ〜")