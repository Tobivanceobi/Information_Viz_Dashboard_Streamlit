import numpy as np
import streamlit as st
import altair as alt
import pandas as pd


def plot_violine_chart(data, color_schema="category10", sample_size=1000):
    # Set random seed for reproducibility
    np.random.seed(43)

    # Generate height distributions
    group_heights = []
    for i in range(data.shape[0]):
        heights = np.random.normal(
            loc=data["Height Mean"][i],
            scale=data["Height Variance"][i],
            size=sample_size
        )
        group_heights.append(heights)

    # Combine data into a DataFrame
    df = pd.DataFrame({
        "Height": np.concatenate(group_heights),
        "Group": np.repeat([f"Group {i + 1}" for i in range(len(group_heights))], sample_size)
    })

    # Dynamically determine the density extent
    height_min = df["Height"].min()
    height_max = df["Height"].max()

    # Create the Violin Plot using Altair
    chart = (
        alt.Chart(df)
        .transform_density(
            "Height",
            as_=["Height", "density"],
            groupby=["Group"],
            extent=[height_min, height_max],
            counts=True
        )
        .mark_area(orient="vertical")
        .encode(
            alt.X("Height:Q",
                  title="Height in cm",
                  axis=alt.Axis(tickSize=10, grid=True),
                  scale=alt.Scale(domain=(height_min, height_max))
                  ),
            alt.Y("density:Q",
                  stack="center",
                  title=None,
                  axis=alt.Axis(labels=False, tickCount=2, tickBand="center")),
            alt.Color(
                "Group:N",
                scale=alt.Scale(scheme=color_schema),
                legend=alt.Legend(title="Groups")
            ),
            alt.Row("Group:N", spacing=10, title="People Count"),
            [alt.Tooltip("Height:Q", title="Height in cm", format=".0f"),
                alt.Tooltip("density:Q", title="Count", format=".0f")]
        )
        .properties(width=450, height=80)
    )

    # Render the chart in Streamlit
    st.altair_chart(chart, use_container_width=False)
