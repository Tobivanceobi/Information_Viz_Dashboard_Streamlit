import pickle
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import toml

from src.utils import Page, h4_header, load_shap_values, flatten_array, compute_y_offsets, compute_plot_bounds


class Dashboard2(Page):
    NAME = "Dashboard 2"
    SHAP_SWARM_HEIGHT = 190
    SHAP_BAR_HEIGHT = 795
    LABELS_AXES = {
        "Passed_Exam": "Passed Exam",
        "Previous_Scores": "Previous Scores",
        "Exam_Score": "Exam Score",
        "Hours_Studied": "Hours Studied (h)",
        "Attendance": "Attendance (%)",
        "Parental_Involvement": "Parental Involvement",
        "Access_to_Resources": "Access to Resources",
        "Extracurricular_Activities": "Extracurricular Activities",
        "Sleep_Hours": "Sleep Hours (h)",
        "Motivation_Level": "Motivation Level",
        "Internet_Access": "Internet Access",
        "Tutoring_Sessions": "Tutoring Sessions",
        "Family_Income": "Family Income",
        "Teacher_Quality": "Teacher Quality",
        "School_Type": "School Type",
        "Peer_Influence": "Peer Influence",
        "Physical_Activity": "Physical Activity",
        "Learning_Disabilities": "Learning Disabilities",
        "Parental_Education_Level": "Parental Education Level",
        "Distance_from_Home": "Distance from Home",
    }

    def __init__(self):
        shap_data = load_shap_values()
        self.shap_values = shap_data['shap_values'].values
        self.X = shap_data['X_test']

    def get_feature_index(self, feature_name):
        """Get the index of the selected feature from the dataset."""
        return self.X.columns.get_loc(feature_name)

    def prepare_plot_data(self, feature_name):
        """
        Prepare the data needed for plotting SHAP values for a specific feature.

        :param feature_name: Name of the feature to plot SHAP values for
        :return: DataFrame with 'SHAP Value', 'Feature Value', and 'y_offset'
        """
        feature_index = self.get_feature_index(feature_name)
        shap_feature_values = flatten_array(self.shap_values[:, feature_index])
        feature_values = self.X[feature_name].values

        # Convert to numeric and round
        shap_feature_values = np.array(shap_feature_values, dtype=np.float32).round(2)
        feature_values = np.array(feature_values, dtype=np.float32).round(2)

        # Create DataFrame and sort by 'Feature Value'
        plot_data = pd.DataFrame({
            'SHAP Value': shap_feature_values,
            'Feature Value': feature_values
        }).sort_values(by='Feature Value')

        # Compute y-offset for better visualization
        plot_data['y_offset'] = compute_y_offsets(plot_data['Feature Value'])

        return plot_data

    def create_swarm_plot(self, plot_data, feature_name):
        """
        Create an Altair swarm plot for the given data.

        :param plot_data: DataFrame containing 'SHAP Value', 'Feature Value', and 'y_offset'
        :param feature_name: Name of the feature being plotted
        :return: Altair Chart object
        """
        bound_x, bound_y = compute_plot_bounds(plot_data['SHAP Value'], plot_data['y_offset'])

        # Create the swarm plot
        return (alt.Chart(plot_data)
            .mark_circle(size=60)
            .encode(
                x=alt.X('SHAP Value:Q', title='SHAP Value (impact on exam score prediction)', scale=alt.Scale(domain=(-bound_x, bound_x))),
                y=alt.Y('y_offset:Q', title=None, axis=None, scale=alt.Scale(domain=(-bound_y, bound_y)),
                        sort='descending'),
                color=alt.Color('Feature Value:Q',
                                scale=alt.Scale(range=['#008bfb', '#ff0051']),
                                title=None,
                                legend=alt.Legend(
                                    title="Feature Value",
                                    titleAlign='center',
                                    titleOrient='right',
                                    orient='right',
                                    labelExpr=f"datum.value === {plot_data['Feature Value'].max()} ? 'High' : datum.value === {plot_data['Feature Value'].min()} ? 'Low' : ''",
                                    labelAlign='left',
                                    labelOffset=10
                                )),
                tooltip=[
                    alt.Tooltip('Feature Value:Q', title=self.LABELS_AXES[feature_name] + ': ', format='.2f'),
                    alt.Tooltip('SHAP Value:Q', title='SHAP Value: ', format='.2f'),
                ]
            )
            .properties(height=self.SHAP_SWARM_HEIGHT)
            .configure_mark(opacity=0.6))

    def plot_shap_values(self, feature_name):
        """
        Main method to prepare data and display the SHAP values swarm plot.

        :param feature_name: Name of the feature to plot
        """
        plot_data = self.prepare_plot_data(feature_name)
        swarm_plot = self.create_swarm_plot(plot_data, feature_name)
        st.altair_chart(swarm_plot, use_container_width=True)

    def plot_shap_bar_chart(self):
        """
        Plot a bar chart for the average SHAP values for each feature.

        :return: Altair Chart object
        """
        # Compute mean SHAP values for each feature
        mean_shap_values = []
        for i, feature_name in enumerate(self.X.columns):
            feature_index = self.get_feature_index(feature_name)
            shap_feature_values = flatten_array(self.shap_values[:, feature_index])
            mean_shap_values.append(np.mean(np.abs(shap_feature_values)))
        feature_names = self.X.columns

        # Create a DataFrame for plotting
        bar_data = pd.DataFrame({
            'Feature': feature_names,
            'Mean SHAP Value': mean_shap_values
        }).sort_values(by='Mean SHAP Value', ascending=False)

        # Create the bar chart
        bar_chart = (alt.Chart(bar_data)
                     .mark_bar(color='#008bfb')
                     .encode(
            x=alt.X('Mean SHAP Value:Q', title='Mean SHAP Value',
                    scale=alt.Scale(domain=(0, bar_data['Mean SHAP Value'].max() * 1.1))),
            y=alt.Y('Feature:N', title='Feature', sort='-x'),
            tooltip=['Feature', 'Mean SHAP Value']
        )
                     .properties(height=self.SHAP_BAR_HEIGHT)
                     .configure_mark(opacity=0.6))

        # Display the bar chart
        st.altair_chart(bar_chart, use_container_width=True)

    def write(self):
        col = st.columns((1, 1, 1), gap='medium')
        with col[0]:
            with st.container(border=2):
                h4_header('Teacher Quality')
                self.plot_shap_bar_chart()
        with col[1]:
            with st.container(border=2):
                h4_header('Attendance')
                self.plot_shap_values('Attendance')
            with st.container(border=2):
                h4_header('Parental Involvement')
                self.plot_shap_values('Parental_Involvement')
            with st.container(border=2):
                h4_header('Hours Studied')
                self.plot_shap_values('Hours_Studied')
        with col[2]:
            with st.container(border=2):
                h4_header('Previous Scores')
                self.plot_shap_values('Previous_Scores')
            with st.container(border=2):
                h4_header('Tutoring Sessions')
                self.plot_shap_values('Tutoring_Sessions')
            with st.container(border=2):
                h4_header('Family Income')
                self.plot_shap_values('Family_Income')
