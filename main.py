import streamlit as st
from streamlit_javascript import st_javascript
import altair as alt
from src.theme import dark_theme, light_theme
from src.utils import add_custom_css
from src.pages import PAGE_MAP



# Page configuration
st.set_page_config(
    page_title="Student Performance Factors",
    page_icon="puzzle.png",
    layout="wide",
    initial_sidebar_state="expanded",
)

alt.themes.enable("dark")

add_custom_css()

data_dark = {
    "Profile": {
        "Attribute": ["Hobby", "Age", "Job", "Height"],
        "Values": ["Cooking", 42, "Nurses", 180]
    },
    "Group Statistics": {
        "Group": ["Group 1", "Group 2"],
        "Age Mean": [28, 41],
        "Age Variance": [15, 20],
        "Height Mean": [180, 160],
        "Height Variance": [20, 15]  # Variance = std^2
    },
    "Hobby Distribution": {
        "Hobby": ["Gardening", "Painting", "Cooking", "Swimming", "Hiking", "Reading"],
        "Group 1": [0.1, 0.3, 0.4, 0.55, 0.8, 0.9],
        "Group 2": [0.9, 0.7, 0.6, 0.45, 0.2, 0.1]
    },
    "Job Distribution": {
        "Job": ["Mechanics", "Farmers", "IT Support", "Secretaries", "Baker",
                "Paramedics", "Bar Tender", "Nurses", "Beauticians", "Teachers"],
        "Group 1": [0.01, 0.18, 0.24, 0.7, 0.47, 0.46, 0.51, 0.98, 0.85, 0.55],
        "Group 2": [0.99, 0.82, 0.76, 0.3, 0.53, 0.54, 0.49, 0.02, 0.15, 0.45]
    }
}

data_light = {
    "Profile": {
        "Attribute": ["Hobby", "Age", "Job", "Height"],
        "Values": ["Cooking", 42, "Nurses", 180]
    },
    "Group Statistics": {
        "Group": ["Group 1", "Group 2"],
        "Age Mean": [35, 48],
        "Age Variance": [15, 20],
        "Height Mean": [175, 195],
        "Height Variance": [20, 15]  # Variance = std^2
    },
    "Hobby Distribution": {
        "Hobby": ["Painting",  "Hiking", "Reading", "Cooking", "Gardening", "Swimming"],
        "Group 1": [0.1, 0.3, 0.4, 0.55, 0.8, 0.9],
        "Group 2": [0.9, 0.7, 0.6, 0.45, 0.2, 0.1]
    },
    "Job Distribution": {
        "Job": ["Secretaries", "Baker", "Paramedics", "Bar Tender", "Mechanics",
                "Nurses", "Beauticians", "Farmers", "IT Support", "Teachers"],
        "Group 1": [0.01, 0.18, 0.24, 0.7, 0.47, 0.46, 0.51, 0.98, 0.85, 0.73],
        "Group 2": [0.99, 0.82, 0.76, 0.3, 0.53, 0.54, 0.49, 0.02, 0.15, 0.27]
    }
}

def main():
    # Register the themes
    alt.themes.register('dark_theme', dark_theme)
    alt.themes.register('light_theme', light_theme)
    st.sidebar.title("Theme Options")
    st_toggle_theme = st.sidebar.toggle(label="Dark Mode", value=False)
    if st_toggle_theme:
        alt.themes.enable("dark_theme")
        data = data_dark
    else:
        alt.themes.enable("light_theme")
        data = data_light

    # Initialize session state to store the current page
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = list(PAGE_MAP.keys())[0]  # Default to the first page

    # Sidebar buttons for each page
    st.sidebar.title("Profile Attributes:")
    age = st.sidebar.number_input("Age", 0, 100, 20)
    height = st.sidebar.number_input("Height", 0, 250, 150)
    hobby = st.sidebar.selectbox("Hobby", data["Hobby Distribution"]["Hobby"])
    job = st.sidebar.selectbox("Job", data["Job Distribution"]["Job"])

    data["Profile"]["Values"] = [hobby, age, job, height]

    st.session_state['current_page'] = "Dashboard"

    current_page = st.session_state['current_page']
    PAGE_MAP[current_page](data).write()

if __name__ == "__main__":
    main()
