import numpy as np
import streamlit as st
import altair as alt
import pandas as pd
from streamlit_javascript import st_javascript


# Page configuration
st.set_page_config(
    page_title="InfoViz - Dashboard",
    page_icon="puzzle.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Define the custom theme
def dark_theme():
    return {
        "config": {
            "view": {"continuousWidth": 400, "continuousHeight": 300},
            "axis": {
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "white",      # Axis label color
                "titleColor": "white",      # Axis title color
                "gridColor": "white",       # Grid line color
                "domainColor": "white",     # Axis line color
                "tickColor": "white",       # Tick color
            },
            "header": {                    # Row/column header settings
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "white",      # Row/column label color
                "titleColor": "white"       # Row/column title color
            },
            "legend": {                    # Legend settings
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "white",      # Legend label color
                "titleColor": "white"       # Legend title color
            }
        }
    }

def light_theme():
    return {
        "config": {
            "view": {"continuousWidth": 400, "continuousHeight": 300},
            "axis": {
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "black",  # Axis label color
                "titleColor": "black",  # Axis title color
                "gridColor": "black",  # Grid line color
                "domainColor": "black",  # Axis line color
                "tickColor": "black",  # Tick color
            },
            "header": {  # Row/column header settings
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "black",  # Row/column label color
                "titleColor": "black"  # Row/column title color
            },
            "legend": {  # Legend settings
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "black",  # Legend label color
                "titleColor": "black"  # Legend title color
            }
        }
    }

# Register the themes
alt.themes.register('dark_theme', dark_theme)
alt.themes.register('light_theme', light_theme)

st_theme = st_javascript("""window.getComputedStyle(window.parent.document.getElementsByClassName("stApp")[0]).getPropertyValue("color-scheme")""")

if st_theme == 'dark':
    alt.themes.enable("dark_theme")
else:
    alt.themes.enable("light_theme")

config = {'displayModeBar': False}

c_style = """
    <style>
    .st-a-l {
        font-size: 14pt;
        font-weight: bold;
        padding-top: 16px;
        padding-bottom: 16px;
    }
    
    .st-t {
        font-size: 22pt;
        padding-bottom: 10px;
        text-align: center;
    }
    
    .st-t-h {
        font-size: 22pt;
        font-weight: bold;
    }
    
    .st-label {
        font-size: 22pt;
        font-weight: bold;
        padding-bottom: 22px;
    }
    
    .st-chart-label {
        font-size: 22pt;
        font-weight: bold;
        padding-bottom: 30px;
    }
    
    .st-value {
        font-size: 22pt;
        padding-bottom: 22px;
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
    
    [data-testid="collapsedControl"] {
        display: none
    }
    
    section.main > div:has(~ footer ) {
        padding-bottom: 0px;
        margin-bottom: -100px;
    }
    </style>
"""
# Apply CSS style for square corners
st.sidebar.markdown(c_style, unsafe_allow_html=True)


def plot_normal_distribution(mean, variance, label):
    # Calculate the standard deviation
    std_dev = np.sqrt(variance)

    # Generate x values within ±4 standard deviations of the mean
    x_values = np.linspace(15, 65, 1000)

    # Calculate the normal distribution for each x value
    y_values = (1 / (std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x_values - mean) / std_dev) ** 2)

    # Convert to percentage
    y_values = y_values * 100

    # Create a DataFrame for Altair with the label for the legend
    df = pd.DataFrame({
        'X': x_values,
        'Probability Density (%)': [round(i, 4) for i in y_values],
        'Distribution': [label] * len(x_values)  # Add label for legend
    })

    return df


def main():
    with st.container(border=2):
        st.markdown('<div class="st-t"> '
                    '<span class="st-t-h"> User Task: </span> '
                    'Determine whether the subject belongs to Group 1 or Group 2 based on their profile and the '
                    'attribute distributions shown. </div>',
                    unsafe_allow_html=True)
    cols = st.columns((3, 5, 5), gap='medium')
    color_schema = 'category10'
    with cols[0]:
        with st.container(border=2):
            st.markdown('<div class="st-chart-label"> Subject Profile </div>', unsafe_allow_html=True)
            row = st.columns((1, 1.5), gap='medium')
            with row[0]:
                st.markdown('<div class="st-label"> Age: </div>', unsafe_allow_html=True)
                st.markdown('<div class="st-label"> Job: </div>', unsafe_allow_html=True)
                st.markdown('<div class="st-label"> Hobby: </div>', unsafe_allow_html=True)
                st.markdown('<div class="st-label"> Height: </div>', unsafe_allow_html=True)
            with row[1]:
                st.markdown('<div class="st-value"> 37 </div>', unsafe_allow_html=True)
                st.markdown('<div class="st-value"> Teacher </div>', unsafe_allow_html=True)
                st.markdown('<div class="st-value"> Hiking </div>', unsafe_allow_html=True)
                st.markdown('<div class="st-value"> 176 cm </div>', unsafe_allow_html=True)

        with st.container(border=2):
            st.markdown('<div class="st-a-l"> To which group dose the subject belong? </div>', unsafe_allow_html=True)
            st.selectbox('Group', ['Group 1', 'Group 2'], key='answer', index=None, label_visibility='collapsed')
            st.markdown('<div class="st-a-l"> How confident are you in your answer? </div>', unsafe_allow_html=True)
            st.markdown('Not Confident (0.0) to Very Confident (1.0)', unsafe_allow_html=True)
            st.slider(
                "Not Confident (0.0) to Very Confident (1.0)",
                0.0, 1.0, key='confidence', value=0.5, label_visibility='collapsed')
            st.button('Submit')

    with cols[1]:
        with st.container(border=2):
            st.markdown('<div class="st-chart-label"> Hobby Distribution</div>', unsafe_allow_html=True)
            data = {
                "Hobby": [
                    "Gardening", "Painting", "Cooking",
                    "Swimming", "Hiking", "Reading"
                ],
                "Group 1": [0.07, 0.19, 0.68, 0.95, 0.83, 0.74],
                "Group 2": [0.93, 0.81, 0.32, 0.05, 0.17, 0.26]
            }
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
                tooltip=["Hobby:N", "Percentage:Q"]
            ).properties(width=220, height=205)
            st.altair_chart(chart, use_container_width=False)
            # plot_pie_chart(data['Group1'], data['Hobby'], labels=['Portion', 'Hobby'])

        with st.container(border=2):
            st.markdown('<div class="st-chart-label">Job Distribution</div>', unsafe_allow_html=True)
            # Create the dataset with raw counts
            data = {
                "Job": [
                    "Mechanics", "Farmers", "IT Support", "Secretaries",
                    "Baker", "Paramedics", "Bar Tender", "Nurses",
                    "Beauticians", "Teachers"
                ],
                "Group 1": [0.01, 0.18, 0.24, 0.7, 0.47, 0.46, 0.51, 0.98, 0.85, 0.73],
                "Group 2": [0.99, 0.82, 0.76, 0.3, 0.53, 0.54, 0.49, 0.02, 0.15, 0.27]
            }

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
            ).properties(width=25, height=140)
            st.altair_chart(chart, use_container_width=False)

    with cols[2]:
        with st.container(border=2):
            st.markdown('<div class="st-chart-label"> Age Distribution </div>', unsafe_allow_html=True)
            # Generate data for two normal distributions
            # Generate data for two normal distributions with labels
            df1 = plot_normal_distribution(42, 20, 'Group 1')  # Distribution 1: mean = 42, variance = 2
            df2 = plot_normal_distribution(28, 10, 'Group 2')

            # Combine both distributions into one DataFrame
            df = pd.concat([df1, df2])

            # Create the chart
            chart = alt.Chart(df).mark_line().encode(
                x=alt.X('X', title='Age'),
                y=alt.Y('Probability Density (%)', title='Number of People'),
                color=alt.Color('Distribution:N', title='Distribution',
                                scale=alt.Scale(scheme=color_schema),
                                legend=alt.Legend(title="Groups")
                                ),
                tooltip=[alt.Tooltip('X', title='Age'),
                         alt.Tooltip('Probability Density (%)', title='Number of People')]
            ).properties(height=250)
            st.altair_chart(chart, use_container_width=True)

        with st.container(border=2):
            st.markdown('<div class="st-chart-label"> Height Distribution </div>', unsafe_allow_html=True)

            # Step 1: Generate random heights for Group1 and Group2
            np.random.seed(42)

            # Group 1 (mean = 180, std = 20)
            group1_heights = np.random.normal(180, 20, 1000)

            # Group 2 (mean = 160, std = 15)
            group2_heights = np.random.normal(160, 15, 1000)

            # Step 2: Combine the data into a DataFrame
            df = pd.DataFrame({
                'Height': np.concatenate([group1_heights, group2_heights]),
                'Group': ['Group 1'] * 1000 + ['Group 2'] * 1000
            })

            # Step 3: Create the Violin Plot using Altair
            chart = alt.Chart(df).transform_density(
                'Height',
                as_=['Height', 'density'],
                groupby=['Group'],
                extent=[120, 210]  # Adjust to fit the range of generated heights
            ).mark_area(orient='vertical').encode(
                alt.X('Height:Q', title='Height in cm'),
                alt.Y('density:Q', stack='center', title=None, axis=alt.Axis(labels=False)),
                alt.Color('Group:N', scale=alt.Scale(scheme=color_schema),
                          legend=alt.Legend(title="Groups")
                          ),
                alt.Row('Group:N', spacing=0)
            ).configure_view(
                stroke=None
            ).properties(width=450, height=80)
            st.altair_chart(chart, use_container_width=False)


if __name__ == "__main__":
    main()
