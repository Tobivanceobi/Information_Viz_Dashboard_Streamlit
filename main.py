import streamlit as st
from src.utils import add_custom_css
from src.components.sidebar_btn import sidebar_button
from src.pages import PAGE_MAP
import altair as alt


# Page configuration
st.set_page_config(
    page_title="Student Performance Factors",
    page_icon="puzzle.png",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")
config = {'displayModeBar': False}

add_custom_css()

def main():
    alt.themes.enable("dark")

    # Initialize session state to store the current page
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = list(PAGE_MAP.keys())[0]  # Default to the first page

    # Sidebar buttons for each page
    st.sidebar.title("Sections")
    for page_name in PAGE_MAP:
        if sidebar_button(page_name):
            st.session_state['current_page'] = page_name

    # Render the selected page
    current_page = st.session_state['current_page']
    PAGE_MAP[current_page]().write()

if __name__ == "__main__":
    main()
