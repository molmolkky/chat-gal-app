# app.py
import streamlit as st
from config_manager import config_manager
from search_settings import render_search_settings

# アプリ全体のタブアイコン＆タイトル（おすすめ）
st.set_page_config(
    page_title="ChatGAL",
    page_icon="🎀",
    layout="wide"
)

# サイドバーで設定を表示
render_search_settings()
config_ready = config_manager.render_sidebar_config()

# Streamlitアプリのタイトル設定
st.title("🎀✨ ChatGAL ✨🎀")
# 各ページ読み込み
chat_page = st.Page("pages/1_chat_page.py", title="チャット", icon="💌")
upload_page = st.Page("pages/2_upload_page.py", title="資料アップ", icon="📤")
evaluation_page = st.Page("pages/3_evaluation_page.py", title="採点", icon="💯")

pg = st.navigation([
    chat_page,
    upload_page,
    evaluation_page
], position="sidebar")
pg.run()
