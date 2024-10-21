import pickle
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st

from src.utils import Page, h4_header


class Dashboard2(Page):
    NAME = "Dashboard 2"

    def __init__(self):
        with open('shap_values.pkl', 'rb') as f:
            data = pickle.load(f)
        self.shap_values = data['shap_values'].values
        self.X = data['X_test']

    def plot_shap_values(self, feature_name):
        # Get the index of the selected feature
        feature_index = self.X.columns.get_loc(feature_name)

        # Ensure the SHAP values are a 2D array and get the values for the selected feature
        shap_feature_values = self.shap_values[:, feature_index]
        feature_values = self.X[feature_name].values

        # Check if shap_feature_values is a 1D array and convert if necessary
        if isinstance(shap_feature_values, np.ndarray) and shap_feature_values.ndim > 1:
            shap_feature_values = shap_feature_values.flatten()  # Ensure it's a 1D array

        # Ensure the SHAP values and feature values are numeric
        shap_feature_values = np.array(shap_feature_values, dtype=np.float64).round(2)
        feature_values = np.array(feature_values, dtype=np.float64)

        # Create a DataFrame
        plot_data = pd.DataFrame({
            'SHAP Value': shap_feature_values,
            'Feature Value': feature_values
        })

        # Sort by feature_value to maintain order in the plot
        plot_data.sort_values(by='Feature Value', inplace=True)

        # Compute the y-offset for each unique feature value
        plot_data['y_offset'] = plot_data.groupby('Feature Value').cumcount() + 0.5
        new_offset = []
        ss = 0
        for i in range(len(plot_data)):
            if ss == 0:
                new_offset.append(plot_data['y_offset'].iloc[i] * -1)
                ss = 1
            else:
                ss = 0
                new_offset.append(plot_data['y_offset'].iloc[i])
        plot_data['y_offset'] = new_offset

        min_shap = plot_data['SHAP Value'].min()
        max_shap = plot_data['SHAP Value'].max()
        bound_x = max(abs(min_shap), abs(max_shap)) * 1.1
        min_offset = plot_data['y_offset'].min()
        max_offset = plot_data['y_offset'].max()
        bound_y = max(abs(min_offset), abs(max_offset)) * 1.1

        # Create the swarm plot
        swarm_plot = (alt.Chart(plot_data)
                      .mark_circle(size=60)
                      .encode(
            x=alt.X('SHAP Value:Q', title='SHAP Value', scale=alt.Scale(domain=(-1*bound_x, bound_x))),
            y=alt.Y('y_offset:Q', title=None, axis=None, scale=alt.Scale(domain=(-1*bound_y, bound_y)),
                    sort='descending'),
            color=alt.Color('Feature Value:Q',
                            scale=alt.Scale(scheme='blues'),
                            title=feature_name),
            tooltip=['SHAP Value', 'Feature Value']
        )
                      .properties(height=200)
                      .configure_mark(opacity=0.6))

        # Display the swarm plot
        st.altair_chart(swarm_plot, use_container_width=True)

    def write(self):
        col = st.columns((5, 3, 5), gap='medium')
        with col[0]:
            with st.container(border=2):
                h4_header('Attendance')
                self.plot_shap_values('Attendance')