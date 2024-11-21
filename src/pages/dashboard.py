import random

import pandas as pd
import altair as alt
import streamlit as st

from ..components.gaussian_chart import plot_bell_chart
from ..components.grouped_bar_chart import plot_grouped_bar_chart
from ..components.pie_chart import plot_pie_chart
from ..components.violin_chart import plot_violine_chart
from ..utils import Page


class Dashboard(Page):
    NAME = "Dashboard"
    def __init__(self, data):
        # Generate random int between 20 and 60
        mean_age = random.randint(20, 60)
        mean_height = random.randint(150, 200)

        self.data = data

        pass

    def write(self):
        with st.container(border=True):
            st.markdown('<div class="st-t"> '
                        '<span class="st-t-h"> User Task: </span> '
                        'To which group is this person likely to belong to based on their attributes and distributions, and how confident are you? </div>',
                        unsafe_allow_html=True)
        cols = st.columns((1.8, 5, 5), gap='medium')

        with cols[0]:
            with st.container(border=True):
                st.markdown('<div class="st-chart-label" style="padding-bottom: 40px; padding-top: 20px; text-align: center;"> Person Profile </div>', unsafe_allow_html=True)

            for i, attr in enumerate(self.data['Profile']['Attribute']):
                with st.container(border=True):
                    st.markdown(
                        f'<div class="st-label"> {attr}</div>',
                        unsafe_allow_html=True)
                    st.markdown(f'<div class="st-value"> {self.data["Profile"]["Values"][i]} </div>', unsafe_allow_html=True)

            # with st.container(border=True):
            #     st.markdown('<div class="st-chart-label"> Questions to Answer: </div>', unsafe_allow_html=True)
            #     st.markdown('<div class="st-a-l"> To which group (1 or 2) dose the subject belong to? </div>',
            #                 unsafe_allow_html=True)

            #     st.markdown('<div class="st-a-l" style="padding-bottom: 100px"> '
            #                 'How confident from 0 (not confident) to 10 (very confident) are you in your answer? '
            #                 '</div>', unsafe_allow_html=True)

        with cols[1]:
            with st.container(border=True):
                st.markdown('<div class="st-chart-label"> Hobby Distribution</div>', unsafe_allow_html=True)
                plot_pie_chart(self.data["Hobby Distribution"], color_schema="category10")

            with st.container(border=True):
                st.markdown('<div class="st-chart-label">Job Distribution</div>', unsafe_allow_html=True)
                plot_grouped_bar_chart(self.data["Job Distribution"], color_schema="category10")

        with cols[2]:
            with st.container(border=True):
                st.markdown('<div class="st-chart-label"> Age Distribution </div>', unsafe_allow_html=True)
                plot_bell_chart(self.data["Group Statistics"], color_schema="category10")

            with st.container(border=True):
                st.markdown('<div class="st-chart-label"> Height Distribution </div>', unsafe_allow_html=True)
                data = pd.DataFrame({
                    "Height Mean": self.data["Group Statistics"]["Height Mean"],
                    "Height Variance": self.data["Group Statistics"]["Height Variance"]
                })
                plot_violine_chart(data, color_schema="category10")



