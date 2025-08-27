import streamlit as st
from backend.upload import document_processor
from config_manager import config_manager

def render_search_settings():
    st.sidebar.header("🔍 検索設定")

    if 'search_params' not in st.session_state:
        st.session_state.search_params = {'k': 10}

    current_params = st.session_state['search_params']

    # 検索結果数の設定
    k_value = st.sidebar.slider(
        "📊 検索結果数",
        min_value=1,
        max_value=20,
        value=current_params['k'],
        help="一度に取得する関連文書の数だよ〜。多いほど詳しく答えられるけど、処理が重くなるかも💦"
    )

    # 変更があるかチェック
    has_changes = (k_value != current_params['k'])

    if st.sidebar.button("✅ 設定を適用", type="primary", disabled=not has_changes):
        if config_manager.is_configured():
            apply_search_settings(k_value)
            st.session_state.search_params = {'k': k_value}
        else:
            st.sidebar.error("⚠️ Azure OpenAI設定を先に行ってね")

def apply_search_settings(k, silent=False):
    """検索設定を適用"""
    try:
        if not st.session_state.retriever:
            document_processor.initialize_vectorstore()

        document_processor.update_retriever_params(k=k)
        
        if not silent:
            st.sidebar.success("✅ 設定を更新したよ〜💕")
            # st.rerun()
        
    except Exception as e:
        st.sidebar.error(f"❌ 設定の更新に失敗しちゃった💦: {str(e)}")
