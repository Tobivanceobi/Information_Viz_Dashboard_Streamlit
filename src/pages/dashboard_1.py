import pandas as pd
import streamlit as st
import toml

from ..utils import Page, h4_header
import altair as alt


class Dashboard1(Page):
    NAME = "Dashboard 1"
    RANKS_2 = ["Yes", "No"]
    RANKS_3 = ["High", "Medium", "Low"]
    COLORS_2 = ['green', 'red']
    COLORS_3 = ['green', 'orange', 'red']
    PASSED_TR = 63
    DONUT_HEIGHT = 90
    BAR_HEIGHT = 158
    BAR_COLOR = '#F39C12'
    SCATTER_HEIGHT = 295
    SCATTER_COLOR = '#27AE60'
    DONUT_COLORS = {
        'red': ['#E74C3C', '#781F16'],
        'orange': ['#F39C12', '#875A12'],
        'green': ['#27AE60', '#12783D'],
        'blue': ['#29b5e8', '#155F7A']
    }
    LABELS_AXES = {
        "Passed_Exam": "Passed Exam",
        "Previous_Scores": "Previous Scores",
        "Exam_Score": "Exam Score",
        # ['Hours_Studied', 'Attendance', 'Parental_Involvement',
        #        'Access_to_Resources', 'Extracurricular_Activities', 'Sleep_Hours',
        #        'Previous_Scores', 'Motivation_Level', 'Internet_Access',
        #        'Tutoring_Sessions', 'Family_Income', 'Teacher_Quality', 'School_Type',
        #        'Peer_Influence', 'Physical_Activity', 'Learning_Disabilities',
        #        'Parental_Education_Level', 'Distance_from_Home', 'Gender',
        #        'Exam_Score']
        "Hours_Studied": "Hours Studied",
        "Attendance": "Attendance",
        "Parental_Involvement": "Parental Involvement",
        "Access_to_Resources": "Access to Resources",
        "Extracurricular_Activities": "Extracurricular Activities",
        "Sleep_Hours": "Sleep Hours",
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
        config = toml.load("config.toml")
        data_path = config["paths"]["data_path"]
        self.data = pd.read_csv(data_path)
        self.data = self.data.dropna()
        self.data['Passed_Exam'] = self.data['Exam_Score'].apply(lambda x: 1 if x > self.PASSED_TR else 0)

    def create_scatter_plot(self, x_col, y_col, labels):
        min_x = self.data[x_col].min()
        max_x = self.data[x_col].max()
        min_y = self.data[y_col].min()
        max_y = self.data[y_col].max()

        # Create the scatter plot
        scatter_plot = (alt.Chart(self.data)
                        .mark_circle(color=self.SCATTER_COLOR)
                        .encode(
            x=alt.X(x_col, title=labels[0], scale=alt.Scale(domain=(min_x, max_x))),
            y=alt.Y(y_col, title=labels[1], scale=alt.Scale(domain=(min_y, max_y))),
            tooltip=[
                alt.Tooltip(x_col, title=labels[0]),
                alt.Tooltip(y_col, title=labels[1]),
            ]
        ).properties(height=self.SCATTER_HEIGHT))

        return scatter_plot

    def create_bar_chart(self, x_col, y_col='Exam_Score', padding=0.05):
        x = self.data[x_col].unique()
        y = []
        for att in x:
            y.append(self.data[self.data[x_col] == att][y_col].mean())

        # Create a DataFrame from the input data
        data = pd.DataFrame({
            'Category': x,
            'Value': y
        })

        # Calculate the y-axis limits with padding based on the data range
        min_value = min(y)
        max_value = max(y)
        data_range = max_value - min_value
        padding = data_range * padding

        # Create the bar chart
        bar_chart = (alt.Chart(data)
                     .mark_bar(color=self.BAR_COLOR)
                     .encode(
            x=alt.X('Category:N', title=self.LABELS_AXES[x_col]),
            y=alt.Y('Value:Q', title=self.LABELS_AXES[y_col],
                    scale=alt.Scale(domain=[min_value - padding, max_value + padding], clamp=True)),
            tooltip=['Category:N', 'Value:Q']
        ).properties(height=self.BAR_HEIGHT))

        return bar_chart

    def make_donut(self, values, group, color, tooltip):
        chart_color = self.DONUT_COLORS[color]

        source = pd.DataFrame({
            "Topic": ['', group],
            "% value": [100 - values, values],
            "valueName": [str(pc) + " %" for pc in [100 - values, values]]
        })
        source_bg = pd.DataFrame({
            "Topic": ['', group],
            "% value": [100, 0]
        })

        plot = (alt.Chart(source).mark_arc(innerRadius=25, cornerRadius=25).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                domain=[group, ''],
                                range=chart_color),
                            legend=None),
            tooltip=[
                alt.Tooltip("Topic:N", title=tooltip[0]),
                alt.Tooltip("valueName:N", title=tooltip[1])
            ]
        ).properties(width=self.DONUT_HEIGHT, height=self.DONUT_HEIGHT))

        text = plot.mark_text(align='center', color="#29b5e8", fontSize=18, fontWeight=700, #fontStyle="italic", font="Lato",
                              ).encode(text=alt.value(f'{values} %'))
        plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=25, cornerRadius=20).encode(
            theta="% value",
            color=alt.Color("Topic:N",
                            scale=alt.Scale(
                                # domain=['A', 'B'],
                                domain=[group, ''],
                                range=chart_color),  # 31333F
                            legend=None),
        ).properties(width=self.DONUT_HEIGHT, height=self.DONUT_HEIGHT)
        return plot_bg + plot + text


    def write(self):
        col = st.columns((3, 5, 5), gap='medium')

        with col[0]:

            with st.container(border=2):
                h4_header('Teacher Quality')
                tq_cols = st.columns((1, 1, 1))
                for i, tq in enumerate(self.RANKS_3):
                    passed_count = self.data[self.data['Teacher_Quality'] == tq]['Passed_Exam'].sum()
                    percent_passed = int(passed_count / len(self.data) * 100)
                    donut_chart = self.make_donut(percent_passed, tq, self.COLORS_3[i],
                                             ['Teacher Quality:', 'Passed Exam:'])
                    with tq_cols[i]:
                        tq_cols[i].write(donut_chart)
            with st.container(border=2):
                h4_header('Family Income')
                fi_cols = st.columns((1, 1, 1))
                for i, fi in enumerate(self.RANKS_3):
                    passed_count = self.data[self.data['Family_Income'] == fi]['Passed_Exam'].sum()
                    percent_passed = int(passed_count / len(self.data) * 100)
                    donut_chart = self.make_donut(percent_passed, fi, self.COLORS_3[i],
                                                  ['Family Income', 'Passed Exam %'])
                    with fi_cols[i]:
                        fi_cols[i].write(donut_chart)
            with st.container(border=2):
                h4_header('Access to Resources')
                ar_cols = st.columns((1, 1, 1))
                for i, ar in enumerate(self.RANKS_3):
                    passed_count = self.data[self.data['Access_to_Resources'] == ar]['Passed_Exam'].sum()
                    percent_passed = int(passed_count / len(self.data) * 100)
                    donut_chart = self.make_donut(percent_passed, ar, self.COLORS_3[i],
                                             ['Access to Resources', 'Passed Exam %'])
                    with ar_cols[i]:
                        ar_cols[i].write(donut_chart)
            with st.container(border=2):
                h4_header('Internet Access')
                ia_cols = st.columns((0.5, 1, 1, 0.5))
                for i, ia in enumerate(self.RANKS_2):
                    passed_count = self.data[self.data['Internet_Access'] == ia]['Passed_Exam'].sum()
                    percent_passed = int(passed_count / len(self.data) * 100)
                    donut_chart = self.make_donut(percent_passed, ia, self.COLORS_3[i],
                                             ['Internet Access', 'Passed Exam %'])
                    with ia_cols[i + 1]:
                        ia_cols[i + 1].write(donut_chart)

        with col[1]:
            with st.container(border=2):
                h4_header('Attendance vs Mean Exam Score')
                bar_chart = self.create_bar_chart('Attendance', 'Exam_Score', padding=0.05)
                st.altair_chart(bar_chart, use_container_width=True)

            with st.container(border=2):
                h4_header('Hours Studied vs Mean Exam Score')
                bar_chart = self.create_bar_chart('Hours_Studied', 'Exam_Score', padding=0.05)
                st.altair_chart(bar_chart, use_container_width=True)

            with st.container(border=2):
                h4_header('Previous Scores vs Mean Exam Score')
                bar_chart = self.create_bar_chart('Previous_Scores', 'Exam_Score', padding=0.05)
                st.altair_chart(bar_chart, use_container_width=True)

        with col[2]:
            with st.container(border=2):
                h4_header('Attendance vs Exam Score')
                scatter_plot = self.create_scatter_plot('Exam_Score', 'Attendance', 'Exam_Score')
                st.altair_chart(scatter_plot, use_container_width=True)

            with st.container(border=2):
                h4_header('Hours Studied vs Exam Score')
                scatter_plot = self.create_scatter_plot('Exam_Score', 'Hours_Studied', 'Exam_Score')
                st.altair_chart(scatter_plot, use_container_width=True)