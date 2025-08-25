import streamlit as st
from ui.chat_ui import render_chat_with_processor
from backend.upload import document_processor

render_chat_with_processor(document_processor)