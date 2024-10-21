import streamlit as st
from abc import ABC, abstractmethod
from PIL import Image, ImageDraw
import random

class Page(ABC):
    @abstractmethod
    def write(self):
        pass


def add_custom_css():
    sidebar_button_style = """
            <style>
            /* Remove rounded corners from sidebar buttons */
            div[data-testid="stSidebarContent"] button[kind="secondary"] {
                border-radius: 0 !important;
            }
            .vg-tooltip {
                font-size: 14px !important;
            }
            button[title="View fullscreen"] {
                visibility: hidden;
            }
            details[title="Click to view actions"] {
                visibility: hidden;
            }
            </style>
        """
    # Apply CSS style for square corners
    st.sidebar.markdown(sidebar_button_style, unsafe_allow_html=True)

def h4_header(text):
    st.markdown(f'<h4 style="text-align:left;">{text}</h3>', unsafe_allow_html=True)