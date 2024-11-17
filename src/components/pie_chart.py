import streamlit as st
import altair as alt
import pandas as pd

def plot_pie_chart(data, color_schema="category10"):
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Step 2: Transform data into long format
    df_melted = df.melt(id_vars=["Hobby"], value_vars=["Group 1", "Group 2"],
                        var_name="Group", value_name="Percentage")

    # Step 3: Create the pie chart using Altair
    chart = alt.Chart(df_melted).mark_arc().encode(
        theta=alt.Theta(field="Percentage", type="quantitative"),
        color=alt.Color(field="Hobby", type="nominal", legend=alt.Legend(title="Hobbies"),
                        scale=alt.Scale(scheme=color_schema)),
        column=alt.Column(field="Group", type="nominal", header=alt.Header(title=None)),
        tooltip=[
            alt.Tooltip("Hobby", title="Hobby"),
            alt.Tooltip("Percentage", title="Portion", format=".2f")
        ]
    ).properties(width=220, height=205)
    st.altair_chart(chart, use_container_width=False)