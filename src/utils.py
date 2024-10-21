import os
import pickle

import numpy as np
import streamlit as st
from abc import ABC, abstractmethod

import toml
from PIL import Image, ImageDraw
import random

from scipy.stats import gaussian_kde


class Page(ABC):
    @abstractmethod
    def write(self):
        pass


def add_custom_css():
    sidebar_button_style = """
            <style>
            /* Remove rounded corners from sidebar buttons */
            div[data-testid="stSidebarContent"] button[kind="secondary"] {
                border-radius: 0 !important;
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
            </style>
        """
    # Apply CSS style for square corners
    st.sidebar.markdown(sidebar_button_style, unsafe_allow_html=True)


def h4_header(text):
    st.markdown(f'<h4 style="text-align:left;">{text}</h3>', unsafe_allow_html=True)


def load_shap_values():
    config = toml.load("config.toml")
    shap_path = config["paths"]["shap_path"]
    if os.path.exists(shap_path):
        with open(shap_path, 'rb') as f:
            data = pickle.load(f)
        return data
    else:
        st.error("SHAP values not found. Please run the model training script.")
        st.stop()

def flatten_array(array):
    """
    Ensure the SHAP values are a 1D array.

    :param array: Array to be flattened if necessary
    :return: Flattened array
    """
    return array.flatten() if array.ndim > 1 else array


def compute_y_offsets(feature_values, spacing=0.4):
    """
    Compute the y-offsets symmetrically around the center for each unique feature value.

    :param feature_values: Series of feature values
    :param spacing: The spacing factor to control the spread of points
    :return: Array of y-offset values
    """
    # Group feature values to handle identical values
    grouped = feature_values.groupby(feature_values).cumcount()

    # Alternate offsets to spread symmetrically
    offsets = (grouped % 2) * 2 - 1  # Alternate between -1 and 1
    offsets *= (grouped // 2 + 1) * spacing  # Scale based on the group index

    return offsets


def compute_plot_bounds(shap_values, y_offsets):
    """
    Compute the bounds for the plot axes.

    :param shap_values: Array of SHAP values
    :param y_offsets: Array of y-offset values
    :param scale_factor: Factor to scale the plot bounds
    :return: Tuple of (bound_x, bound_y) for the plot
    """
    max_shap = max(abs(shap_values.min()), abs(shap_values.max()))
    max_offset = max(abs(y_offsets.min()), abs(y_offsets.max()))
    bound_x = max_shap * 1.1
    bound_y = max_offset * 1.75
    return bound_x, bound_y
