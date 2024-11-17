import numpy as np
import streamlit as st
import altair as alt
import pandas as pd


def plot_bell_chart(data, color_schema="category10"):

    std_dev_1 = np.sqrt(data["Age Variance"][0])
    std_dev_2 = np.sqrt(data["Age Variance"][1])

    start = min(data["Age Mean"]) - 3 * max(std_dev_1, std_dev_2)
    end = max(data["Age Mean"]) + 3 * max(std_dev_1, std_dev_2)

    x_values = np.linspace(start, end, 1000)

    y_values_1 = (1 / (std_dev_1 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values - data["Age Mean"][0]) / std_dev_1) ** 2)
    y_values_2 = (1 / (std_dev_2 * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values - data["Age Mean"][1]) / std_dev_2) ** 2)

    df1 = pd.DataFrame({
        "X": x_values,
        "Probability Density (%)": y_values_1 * 100,
        "Distribution": [data["Group"][0]] * len(x_values)
    })
    df2 = pd.DataFrame({
        "X": x_values,
        "Probability Density (%)": y_values_2 * 100,
        "Distribution": [data["Group"][1]] * len(x_values)
    })

    df = pd.concat([df1, df2])

    # Create the chart
    chart = alt.Chart(df).mark_line().encode(
        # set the x lim to the min and max of the data
        x=alt.X('X', title='Age', scale=alt.Scale(domain=(min(data["Age Mean"]) - 3 * max(std_dev_1, std_dev_2),
                                                           max(data["Age Mean"]) + 3 * max(std_dev_1, std_dev_2))),
                axis=alt.Axis(tickCount=18)),
        y=alt.Y('Probability Density (%)', title='People Count'),
        color=alt.Color('Distribution:N', title='Distribution',
                        scale=alt.Scale(scheme=color_schema),
                        legend=alt.Legend(title="Groups")
                        ),
        tooltip=[alt.Tooltip('X', title='Age', format='.0f'),
                 alt.Tooltip('Probability Density (%)', title='Count', format='.0f')]
    ).properties(height=250)
    st.altair_chart(chart, use_container_width=True)
