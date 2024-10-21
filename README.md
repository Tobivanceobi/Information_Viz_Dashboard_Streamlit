# Streamlit Dashboard for Information Visualization

This project was created on behalf of the course Information Visualization at the 
University of St. Gallen. The dashboard is used in a eye-tracking study to evaluate
the gaze behavior of users when interacting with different visualizations.

## Installation
To run the dashboard, you need to install the required packages. You can do this by running the following command:
```bash
pip install -r requirements.txt
```

## Usage
To run the dashboard, you can use the following command in the root directory of the project:
```bash
streamlit run app.py
```

## File Structure
The project is structured as follows:
- [`main.py`](main.py): Main file to run the Streamlit dashboard
- [`ML_Models.ipynb`](ML_Models.ipynb): Jupyter notebook containing the ML model used to compute the shap values
- `data/`: Folder containing the data used in the dashboard and the shap values of the ML model
- `src/pages`: Folder containing the different pages of each dashboard
- `src/components`: Folder containing the different components used in the dashboard
- `src/utils`: Folder containing utility functions used in the dashboard
- `src/assets`: Folder containing the assets used in the dashboard
- [`requirements.txt`](requirements.txt): File containing the required packages for the dashboard

