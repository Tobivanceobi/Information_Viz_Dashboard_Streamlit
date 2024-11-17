import os
import pickle

import numpy as np
import pandas as pd
import streamlit as st
from abc import ABC, abstractmethod

import toml
from PIL import Image, ImageDraw
import random

from scipy.stats import gaussian_kde


class Page(ABC):

    # Abstract initialization method with data parameter
    @abstractmethod
    def __init__(self, data):
        pass

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
            
            .st-a-l {
                font-size: 14pt;
                font-weight: bold;
                padding-top: 19px;
                padding-bottom: 20px;
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
    st.sidebar.markdown(sidebar_button_style, unsafe_allow_html=True)


def h4_header(text):
    st.markdown(f'<h4 style="text-align:left;">{text}</h3>', unsafe_allow_html=True)


def plot_normal_distribution(mean, variance, label):
    # Calculate the standard deviation
    std_dev = np.sqrt(variance)

    # Generate x values within ±4 standard deviations of the mean
    start = mean - 3 * std_dev
    end = mean + 3 * std_dev
    x_values = np.linspace(start, end, 1000)

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
