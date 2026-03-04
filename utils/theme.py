import streamlit as st

def toggle_theme():
    """Toggle between day and night mode"""
    # Initialize if not exists, then toggle
    if 'theme_mode' not in st.session_state:
        st.session_state.theme_mode = 'night'
    else:
        st.session_state.theme_mode = 'day' if st.session_state.theme_mode == 'night' else 'night'
