import streamlit as st
import altair as alt
import pandas as pd


def plot_grouped_bar_chart(data, color_schema="category10"):
    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Melt the data to make it suitable for Altair
    df_melted = df.melt(id_vars=["Job"], value_vars=["Group 1", "Group 2"],
                        var_name="Group", value_name="Fraction")

    # Create a bar plot with Altair
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X('Group:O', axis=alt.Axis(labels=False), title=None),
        y=alt.Y('Fraction:Q', title='Fraction'),
        color=alt.Color('Group:N', scale=alt.Scale(scheme=color_schema),
                        legend=alt.Legend(title="Groups")),
        column=alt.Column('Job:N',
                          header=alt.Header(
                              labelAngle=-90, labelAlign='right', orient='bottom', title=None),
                          )
    ).properties(width=30, height=170)
    st.altair_chart(chart, use_container_width=False)
