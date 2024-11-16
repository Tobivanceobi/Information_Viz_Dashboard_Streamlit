import numpy as np
import matplotlib.pyplot as plt
import altair as alt

# write a function tha samples n values from a normal distribution with mean mu and standard deviation sigma
def sample_normal_distribution(n, mu, sigma):
    return np.random.normal(mu, sigma, n)

# write a function that bins the values of a given array into n bins
def bin_values(array, n):
    return np.histogram(array, bins=n)

import pandas as pd

# Load JSONL data into a DataFrame
# Load the dataset
file_path = 'data/gender_classification_v7.csv'
df = pd.read_csv(file_path)

print(df.columns)
print(df['lips_thin'].unique())
print(df['nose_long'].unique())
print(df['nose_wide'].unique())
print(df['nose_long'].unique())


# Filter data by gender
df_males = df[df['gender'] == 'Male']
df_females = df[df['gender'] == 'Female']

col_oi = 'long_hair'
# Calculate mean and variance for male and female 'forehead_width_cm'
male_mean = df_males[col_oi].mean()
male_variance = df_males[col_oi].var()

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Given data
data = {
    "Job": [
        "Vehicle technicians", "Farmers", "Waste managers", "Caretakers",
        "Estate agents", "Paramedics", "Bar staff", "Nursery nurses",
        "Beauticians", "Educational professionals"
    ],
    "Female": [1519, 25282, 4550, 27010, 25132, 15199, 122825, 223804, 86782, 173467],
    "Male": [189127, 116311, 12145, 65476, 33068, 17626, 117602, 5042, 15839, 64629]
}

# Convert to DataFrame
df = pd.DataFrame(data)

# Set position of bars on x-axis
bar_width = 0.35
index = np.arange(len(df))

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Create bars for Female and Male
ax.barh(index, df['Female'], bar_width, label='Female', color='blue')
ax.barh(index + bar_width, df['Male'], bar_width, label='Male', color='orange')

# Labeling the axes and title
ax.set_xlabel('Job', fontsize=12)
ax.set_ylabel('Count', fontsize=12)
ax.set_title('Gender Distribution by Job', fontsize=14)

# Set x-ticks to be the job names, and rotate only those labels
ax.set_xticks(index + bar_width / 2)  # Position the labels in between the bars
ax.set_xticklabels(df['Job'], rotation=90, ha='center', fontsize=10)

# Add legend
ax.legend()

# Display the plot
plt.tight_layout()
plt.show()

