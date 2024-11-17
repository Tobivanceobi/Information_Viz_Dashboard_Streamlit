# Define the custom theme
def dark_theme():
    return {
        "config": {
            "view": {
                "continuousWidth": 400,
                "continuousHeight": 300,
                "stroke": "white"
            },
            "axis": {
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "white",  # Axis label color
                "titleColor": "white",  # Axis title color
                "gridColor": "white",  # Grid line color
                "domainColor": "white",  # Axis line color
                "tickColor": "white",  # Tick color
            },
            "header": {  # Row/column header settings
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "white",  # Row/column label color
                "titleColor": "white",  # Row/column title color
                "stroke": "white"
            },
            "legend": {  # Legend settings
                "labelFontSize": 16,
                "titleFontSize": 18,
                "labelColor": "white",  # Legend label color
                "titleColor": "white"  # Legend title color
            }
        }
    }


def light_theme():
    return {
        "config": {
            "view": {
                "continuousWidth": 400,
                "continuousHeight": 300,
                "stroke": "black"
            },
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
