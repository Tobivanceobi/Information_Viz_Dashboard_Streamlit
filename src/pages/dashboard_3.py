import streamlit as st
from ..utils import Page


class Dashboard3(Page):
    NAME = "Dashboard 3"
    def __init__(self):
        pass

    def write(self):
        st.title(self.NAME)